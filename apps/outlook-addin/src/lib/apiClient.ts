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

export type ThreadRequestPayload = {
  thread: EmailThread;
  userSettings?: UserSettings;
};

export type CatchUpRequestPayload = {
  threads: EmailThread[];
  userSettings?: UserSettings;
};

type ApiClientOptions = {
  baseUrl: string;
};

async function postJson<TResponse>(url: string, payload: ThreadRequestPayload): Promise<TResponse> {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with status ${response.status}`);
  }

  return (await response.json()) as TResponse;
}

async function postCatchUpJson<TResponse>(url: string, payload: CatchUpRequestPayload): Promise<TResponse> {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with status ${response.status}`);
  }

  return (await response.json()) as TResponse;
}

export function createApiClient({ baseUrl }: ApiClientOptions) {
  return {
    async triageThread(payload: ThreadRequestPayload) {
      return postJson<TriageResult>(`${baseUrl}/triage/thread`, payload);
    },
    async summarizeThread(payload: ThreadRequestPayload) {
      return postJson<ThreadSummary>(`${baseUrl}/summarize/thread`, payload);
    },
    async extractAsks(payload: ThreadRequestPayload) {
      return postJson<AskExtractionResult>(`${baseUrl}/extract/asks`, payload);
    },
    async draftReply(payload: ThreadRequestPayload) {
      return postJson<DraftReplySet>(`${baseUrl}/draft/reply`, payload);
    },
    async catchUp(payload: CatchUpRequestPayload) {
      return postCatchUpJson<CatchUpOverview>(`${baseUrl}/catchup`, payload);
    },
    async thoughtPartner(payload: ThreadRequestPayload) {
      return postJson<ThoughtPartnerResult>(`${baseUrl}/thoughtpartner`, payload);
    }
  };
}
