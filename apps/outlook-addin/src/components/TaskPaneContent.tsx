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
import { CatchUpListSection } from "./CatchUpListSection";
import { DirectAsksSection } from "./DirectAsksSection";
import { DraftReplySection } from "./DraftReplySection";
import { FlagReasonsSection } from "./FlagReasonsSection";
import { HeaderSection } from "./HeaderSection";
import { SettingsSection } from "./SettingsSection";
import { SuggestedNextMoveSection } from "./SuggestedNextMoveSection";
import { ThoughtPartnerSection } from "./ThoughtPartnerSection";
import { ThreadSummarySection } from "./ThreadSummarySection";
import { VerdictCard } from "./VerdictCard";
import type { StoredHistoryEntry } from "../lib/settingsStorage";

type TaskPaneContentProps = {
  thread: EmailThread;
  mode: "mock" | "api";
  isBusy: boolean;
  error?: string | null;
  onScanThread: () => void;
  onCatchMeUp: () => void;
  onRefresh: () => void;
  settings: UserSettings;
  history: StoredHistoryEntry[];
  onSettingsChange: (settings: UserSettings) => void;
  onClearHistory: () => void;
  triage: TriageResult;
  summary: ThreadSummary;
  askExtraction: AskExtractionResult;
  draftReplySet: DraftReplySet;
  catchUpOverview: CatchUpOverview;
  thoughtPartner: ThoughtPartnerResult;
};

export function TaskPaneContent({
  thread,
  mode,
  isBusy,
  error,
  onScanThread,
  onCatchMeUp,
  onRefresh,
  settings,
  history,
  onSettingsChange,
  onClearHistory,
  triage,
  summary,
  askExtraction,
  draftReplySet,
  catchUpOverview,
  thoughtPartner
}: TaskPaneContentProps) {
  return (
    <main className="task-pane">
      <HeaderSection
        thread={thread}
        mode={mode}
        isBusy={isBusy}
        onScanThread={onScanThread}
        onCatchMeUp={onCatchMeUp}
        onRefresh={onRefresh}
      />
      {error ? <p className="inline-status">Latest action failed: {error}</p> : null}
      <div className="task-pane__stack">
        <SettingsSection
          settings={settings}
          history={history}
          onChange={onSettingsChange}
          onClearHistory={onClearHistory}
        />
        <VerdictCard bucket={triage.bucket} confidence={triage.confidence} verdict={triage.verdict} />
        <FlagReasonsSection reasons={triage.topReasons} />
        <ThreadSummarySection summary={summary} />
        <DirectAsksSection asks={askExtraction.asks} />
        <SuggestedNextMoveSection nextMove={triage.suggestedNextMove} />
        <DraftReplySection draftReplySet={draftReplySet} />
        <CatchUpListSection overview={catchUpOverview} />
        <ThoughtPartnerSection result={thoughtPartner} />
      </div>
    </main>
  );
}
