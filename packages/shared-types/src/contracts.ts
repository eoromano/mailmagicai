export type EmailMessage = {
  id: string;
  fromName: string;
  fromEmail: string;
  toRecipients?: string[];
  ccRecipients?: string[];
  sentAt: string;
  bodyText: string;
  isUnread: boolean;
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

export type TriageBucket =
  | "needs_action_now"
  | "likely_needs_reply"
  | "important_fyi"
  | "copied_only"
  | "low_signal_noise"
  | "at_risk_of_being_missed";

export type AskType =
  | "review"
  | "approve"
  | "decide"
  | "reply"
  | "confirm"
  | "attend"
  | "delegate"
  | "provide_input"
  | "no_action";

export type AskUrgency = "high" | "medium" | "low";

export type ExtractedAsk = {
  id: string;
  text: string;
  askType: AskType;
  owner: string;
  targetPerson?: string;
  dueDate?: string;
  urgency: AskUrgency;
  sourceSnippet: string;
};

export type AskExtractionResult = {
  asks: ExtractedAsk[];
  inferredMissingReplies: string[];
  inferredBlockers: string[];
};

export type ThreadSummary = {
  summary: string;
  latestChange: string;
  unresolvedItems: string[];
  whoIsWaitingOnWhom: string[];
  deadlines: string[];
  importantContext: string[];
};

export type DraftReplySet = {
  shortReply: string;
  strategicReply: string;
  clarifyingReply: string;
  notesOnWhenToUseEach: {
    shortReply: string;
    strategicReply: string;
    clarifyingReply: string;
  };
};

export type CatchUpItem = {
  id: string;
  title: string;
  detail: string;
};

export type CatchUpBriefingOverview = {
  totalItems: number;
  needsActionNowCount: number;
  likelyNeedsReplyCount: number;
  importantFyiCount: number;
  copiedOnlyCount: number;
  lowSignalNoiseCount: number;
  atRiskCount: number;
};

export type CatchUpBriefingItem = {
  id: string;
  threadId: string;
  subject: string;
  bucket: TriageBucket;
  whyItMatters: string;
  latestChange: string;
  suggestedNextMove: string;
  waitingOnUser: boolean;
};

export type CatchUpOverview = {
  overview: CatchUpBriefingOverview;
  topActionItems: CatchUpBriefingItem[];
  importantFyiItems: CatchUpBriefingItem[];
  copiedOnlyItems: CatchUpBriefingItem[];
  riskItems: CatchUpBriefingItem[];
  themes: string[];
  suggestedFirst10ToRead: CatchUpBriefingItem[];
};

export type ThoughtPartnerResult = {
  issue: {
    evidence: string[];
    inference: string;
  };
  explicitAsks: string[];
  implicitDynamics: {
    evidence: string[];
    inference: string;
  };
  risks: string[];
  options: string[];
  recommendedMove: string;
  confidenceNotes: string;
};

export type TriageReason = {
  id: string;
  title: string;
  detail: string;
};

export type TriageResult = {
  threadId: string;
  bucket: TriageBucket;
  confidence: number;
  verdict: string;
  topReasons: string[];
  summary: ThreadSummary;
  extractedAsks: ExtractedAsk[];
  detectedDeadlines: string[];
  suggestedNextMove: string;
  draftReplySet: DraftReplySet;
  catchUpOverview: CatchUpOverview;
  thoughtPartner: ThoughtPartnerResult;
};

export type UserSettings = {
  displayName: string;
  emailAddress?: string;
  signature: string;
  replyTone: "neutral" | "warm" | "direct";
  includeDraftReplies: boolean;
  showThoughtPartner: boolean;
  vipSenders: string[];
  priorityDomains: string[];
  urgencyKeywords: string[];
  copiedOnlyKeywords: string[];
  draftVoicePreferences: string[];
  saveHistory: boolean;
  mockMode: boolean;
};
