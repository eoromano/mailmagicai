export type EmailMessage = {
  id: string;
  from: string;
  sentAt: string;
  body: string;
};

export type EmailThread = {
  id: string;
  subject: string;
  participants: string[];
  messageCount: number;
  unreadCount: number;
  lastMessageAt: string;
  messages: EmailMessage[];
};

export type AskItem = {
  id: string;
  owner: string;
  request: string;
};

export type CatchUpItem = {
  id: string;
  title: string;
  detail: string;
};

export type Summary = {
  overview: string;
  bullets: string[];
};

export type TriageResponse = {
  threadId: string;
  verdict: string;
  rationale: string;
  summary: Summary;
  directAsks: AskItem[];
  draftReply: string;
  catchUpList: CatchUpItem[];
};
