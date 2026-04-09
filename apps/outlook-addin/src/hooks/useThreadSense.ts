import { useCallback, useEffect, useMemo, useState } from "react";
import type {
  AskExtractionResult,
  CatchUpOverview,
  DraftReplySet,
  EmailThread,
  ThoughtPartnerResult,
  ThreadSummary,
  TriageResult,
  UserSettings
} from "../../../../packages/shared-types/src";
import { exampleUserSettings } from "../../../../packages/shared-types/src";
import { normalizedThreadToEmailThread, normalizedThreadsToEmailThreads } from "../adapters";
import {
  createThreadSenseClient,
  createOutlookDataAdapter,
  defaultMockMode,
  resolveAdapterMode,
  resolveDataMode
} from "../lib/dataSource";
import { createLocalSettingsStorage, type StoredHistoryEntry } from "../lib/settingsStorage";

export type InboxAction = "scan" | "catchup" | "refresh";
export type InboxView = "thread" | "catchup";

export type InboxPaneData = {
  thread: EmailThread;
  triage: TriageResult;
  summary: ThreadSummary;
  askExtraction: AskExtractionResult;
  draftReplySet: DraftReplySet;
  catchUpOverview: CatchUpOverview;
  thoughtPartner: ThoughtPartnerResult;
};

const FALLBACK_ERROR = "Unable to load ThreadSense. Check that the local API is running or switch back to mock mode.";
const settingsStorage = createLocalSettingsStorage();

export function useThreadSense() {
  const [data, setData] = useState<InboxPaneData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastAction, setLastAction] = useState<InboxAction | null>(null);
  const [view, setView] = useState<InboxView>("thread");
  const [settings, setSettings] = useState<UserSettings>(() => {
    const loaded = settingsStorage.loadSettings();
    return {
      ...loaded,
      mockMode: loaded.mockMode ?? defaultMockMode
    };
  });
  const [history, setHistory] = useState<StoredHistoryEntry[]>(() => settingsStorage.loadHistory());
  const mode = useMemo(() => resolveDataMode(settings.mockMode), [settings.mockMode]);
  const adapterMode = useMemo(() => resolveAdapterMode(settings.mockMode), [settings.mockMode]);
  const threadSenseClient = useMemo(() => createThreadSenseClient(mode), [mode]);
  const outlookAdapter = useMemo(() => createOutlookDataAdapter(adapterMode), [adapterMode]);

  useEffect(() => {
    settingsStorage.saveSettings(settings);
    if (!settings.saveHistory) {
      settingsStorage.clearHistory();
      setHistory([]);
    }
  }, [settings]);

  const runAction = useCallback(
    async (action: InboxAction) => {
      setIsLoading(true);
      setError(null);
      setLastAction(action);

      try {
        const normalizedThread = await outlookAdapter.getCurrentThread();
        const normalizedUnreadThreads = await outlookAdapter.getUnreadThreads();
        const thread = normalizedThread ? normalizedThreadToEmailThread(normalizedThread) : null;
        const unreadThreads = normalizedThreadsToEmailThreads(normalizedUnreadThreads);

        if (action === "catchup") {
          if (unreadThreads.length === 0) {
            setData(null);
            setView("catchup");
            return;
          }

          const catchUpOverview = await threadSenseClient.catchUp({
            threads: unreadThreads,
            userSettings: settings
          });
          setData((current) => {
            const resolvedThread = current?.thread ?? thread ?? unreadThreads[0];
            if (!resolvedThread) {
              return null;
            }

            return {
              thread: resolvedThread,
              triage: current?.triage ?? exampleEmptyTriageResult(resolvedThread.id),
              summary: current?.summary ?? exampleEmptySummary(),
              askExtraction: current?.askExtraction ?? exampleEmptyAskExtraction(),
              draftReplySet: current?.draftReplySet ?? exampleEmptyDraftReplySet(),
              catchUpOverview,
              thoughtPartner: current?.thoughtPartner ?? exampleEmptyThoughtPartner()
            };
          });
          setView("catchup");
          const storedHistory = settingsStorage.appendHistory(
            {
              action,
              at: new Date().toISOString(),
              subject: thread?.subject ?? "Catch me up briefing"
            },
            settings
          );
          setHistory(storedHistory);

          return;
        }

        if (!thread) {
          setData(null);
          setView("thread");
          return;
        }

        const requestPayload = {
          thread,
          userSettings: settings
        };
        const catchUpPayload = {
          threads: unreadThreads.length > 0 ? unreadThreads : [thread],
          userSettings: settings
        };
        const [triage, summary, askExtraction, draftReplySet, catchUpOverview, thoughtPartner] =
          await Promise.all([
            threadSenseClient.triageThread(requestPayload),
            threadSenseClient.summarizeThread(requestPayload),
            threadSenseClient.extractAsks(requestPayload),
            threadSenseClient.draftReply(requestPayload),
            threadSenseClient.catchUp(catchUpPayload),
            threadSenseClient.thoughtPartner(requestPayload)
          ]);

        setData({
          thread,
          triage,
          summary,
          askExtraction,
          draftReplySet,
          catchUpOverview,
          thoughtPartner
        });
        setView("thread");

        const storedHistory = settingsStorage.appendHistory(
          {
            action,
            at: new Date().toISOString(),
            subject: thread.subject
          },
          settings
        );
        setHistory(storedHistory);
      } catch (caughtError) {
        const message = caughtError instanceof Error ? caughtError.message : FALLBACK_ERROR;
        setError(message || FALLBACK_ERROR);
      } finally {
        setIsLoading(false);
      }
    },
    [adapterMode, outlookAdapter, settings, threadSenseClient]
  );

  return {
    data,
    error,
    history,
    isLoading,
    lastAction,
    adapterMode,
    mode,
    settings,
    view,
    runAction,
    setSettings,
    clearHistory: () => {
      settingsStorage.clearHistory();
      setHistory([]);
    }
  };
}

function exampleEmptySummary(): ThreadSummary {
  return {
    summary: "No summary is available yet.",
    latestChange: "No message is currently loaded.",
    unresolvedItems: [],
    whoIsWaitingOnWhom: [],
    deadlines: [],
    importantContext: []
  };
}

function exampleEmptyAskExtraction(): AskExtractionResult {
  return {
    asks: [],
    inferredMissingReplies: [],
    inferredBlockers: []
  };
}

function exampleEmptyDraftReplySet(): DraftReplySet {
  return {
    shortReply: "",
    strategicReply: "",
    clarifyingReply: "",
    notesOnWhenToUseEach: {
      shortReply: "",
      strategicReply: "",
      clarifyingReply: ""
    }
  };
}

function exampleEmptyThoughtPartner(): ThoughtPartnerResult {
  return {
    issue: {
      evidence: [],
      inference: ""
    },
    explicitAsks: [],
    implicitDynamics: {
      evidence: [],
      inference: ""
    },
    risks: [],
    options: [],
    recommendedMove: "",
    confidenceNotes: ""
  };
}

function exampleEmptyTriageResult(threadId: string): TriageResult {
  return {
    threadId,
    bucket: "important_fyi",
    confidence: 0,
    verdict: "Catch-up view only",
    topReasons: [],
    summary: exampleEmptySummary(),
    extractedAsks: [],
    detectedDeadlines: [],
    suggestedNextMove: "",
    draftReplySet: exampleEmptyDraftReplySet(),
    catchUpOverview: {
      overview: {
        totalItems: 0,
        needsActionNowCount: 0,
        likelyNeedsReplyCount: 0,
        importantFyiCount: 0,
        copiedOnlyCount: 0,
        lowSignalNoiseCount: 0,
        atRiskCount: 0
      },
      topActionItems: [],
      importantFyiItems: [],
      copiedOnlyItems: [],
      riskItems: [],
      themes: [],
      suggestedFirst10ToRead: []
    },
    thoughtPartner: exampleEmptyThoughtPartner()
  };
}
