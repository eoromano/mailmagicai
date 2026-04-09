import type { EmailMessage, EmailThread } from "../../../../packages/shared-types/src";
import type {
  NormalizedAttachmentMetadata,
  NormalizedMessage,
  NormalizedRecipient,
  NormalizedThread
} from "./types";

function toRecipientLabel(recipient: NormalizedRecipient) {
  return recipient.name?.trim() || recipient.email;
}

function uniqueStrings(values: string[]) {
  return [...new Set(values.filter(Boolean))];
}

function buildPreviewText(bodyText: string) {
  const collapsed = bodyText.replace(/\s+/g, " ").trim();
  if (!collapsed) {
    return "";
  }

  return collapsed.slice(0, 180);
}

function toSafeEmailMessage(message: NormalizedMessage): EmailMessage {
  return {
    id: message.messageId,
    fromName: message.from.name?.trim() || message.from.email,
    fromEmail: message.from.email,
    toRecipients: message.toRecipients.map((recipient) => recipient.email),
    ccRecipients: message.ccRecipients.map((recipient) => recipient.email),
    sentAt: message.sentAt,
    bodyText: message.bodyText,
    isUnread: message.isUnread ?? false
  };
}

export function normalizeMockThread(thread: EmailThread): NormalizedThread {
  return {
    threadId: thread.id,
    subject: thread.subject,
    messages: thread.messages.map((message) => ({
      messageId: message.id,
      threadId: thread.id,
      subject: thread.subject,
      from: {
        name: message.fromName,
        email: message.fromEmail
      },
      toRecipients: (message.toRecipients ?? []).map((email) => ({ email })),
      ccRecipients: (message.ccRecipients ?? []).map((email) => ({ email })),
      sentAt: message.sentAt,
      previewText: buildPreviewText(message.bodyText),
      bodyText: message.bodyText,
      attachments: [],
      isUnread: message.isUnread
    }))
  };
}

export function normalizedThreadToEmailThread(thread: NormalizedThread): EmailThread {
  const messages = [...thread.messages].sort((left, right) => left.sentAt.localeCompare(right.sentAt));
  const fallbackId = messages[0]?.messageId ?? "thread-unknown";
  const messageCount = messages.length;
  const unreadCount = messages.filter((message) => message.isUnread).length;
  const lastMessageAt = messages[messageCount - 1]?.sentAt ?? "";
  const participants = uniqueStrings(
    messages.flatMap((message) => [
      toRecipientLabel(message.from),
      ...message.toRecipients.map(toRecipientLabel),
      ...message.ccRecipients.map(toRecipientLabel)
    ])
  );

  return {
    id: thread.threadId || fallbackId,
    subject: thread.subject,
    participants,
    messageCount,
    unreadCount,
    lastMessageAt,
    messages: messages.map(toSafeEmailMessage)
  };
}

export function normalizedThreadsToEmailThreads(threads: NormalizedThread[]): EmailThread[] {
  return threads.map(normalizedThreadToEmailThread);
}

export function makeNormalizedAttachmentMetadata(
  attachment: Partial<NormalizedAttachmentMetadata> & Pick<NormalizedAttachmentMetadata, "name">
): NormalizedAttachmentMetadata {
  return {
    attachmentId: attachment.attachmentId,
    name: attachment.name,
    contentType: attachment.contentType,
    sizeBytes: attachment.sizeBytes,
    isInline: attachment.isInline
  };
}
