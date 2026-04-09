export type NormalizedRecipient = {
  name?: string;
  email: string;
};

export type NormalizedAttachmentMetadata = {
  attachmentId?: string;
  name: string;
  contentType?: string;
  sizeBytes?: number;
  isInline?: boolean;
};

export type NormalizedMessage = {
  messageId: string;
  threadId?: string;
  subject: string;
  from: NormalizedRecipient;
  toRecipients: NormalizedRecipient[];
  ccRecipients: NormalizedRecipient[];
  sentAt: string;
  previewText: string;
  bodyText: string;
  bodyHtml?: string;
  attachments: NormalizedAttachmentMetadata[];
  isUnread?: boolean;
};

export type NormalizedThread = {
  threadId?: string;
  subject: string;
  messages: NormalizedMessage[];
};

export type OutlookAdapterKind = "mock" | "outlook";

export type OutlookAdapter = {
  kind: OutlookAdapterKind;
  getCurrentThread(): Promise<NormalizedThread | null>;
  getUnreadThreads(): Promise<NormalizedThread[]>;
};
