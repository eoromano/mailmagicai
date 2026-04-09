import { makeNormalizedAttachmentMetadata } from "./normalize";
import type {
  NormalizedAttachmentMetadata,
  NormalizedRecipient,
  NormalizedThread
} from "./types";

type OutlookMessageReadItem = NonNullable<NonNullable<NonNullable<OfficeGlobal["context"]>["mailbox"]>["item"]>;

function getOfficeGlobal() {
  if (typeof window === "undefined") {
    return undefined;
  }

  return window.Office;
}

async function waitForOfficeReady() {
  const office = getOfficeGlobal();
  if (!office?.onReady) {
    return null;
  }

  try {
    return await office.onReady();
  } catch {
    return null;
  }
}

function getMessageItem(): OutlookMessageReadItem | null {
  const office = getOfficeGlobal();
  const item = office?.context?.mailbox?.item;
  if (!item) {
    return null;
  }

  const messageType = office?.MailboxEnums?.ItemType?.Message;
  if (item.itemType && messageType && item.itemType !== messageType) {
    return null;
  }

  return item;
}

function normalizeRecipient(recipient?: OfficeEmailAddressDetails | null): NormalizedRecipient | null {
  const email = recipient?.emailAddress?.trim();
  if (!email) {
    return null;
  }

  return {
    name: recipient?.displayName?.trim(),
    email
  };
}

function normalizeRecipients(recipients?: OfficeEmailAddressDetails[] | null): NormalizedRecipient[] {
  return (recipients ?? [])
    .map((recipient) => normalizeRecipient(recipient))
    .filter((recipient): recipient is NormalizedRecipient => recipient !== null);
}

function normalizeAttachments(attachments?: OfficeAttachmentDetails[] | null): NormalizedAttachmentMetadata[] {
  return (attachments ?? [])
    .filter((attachment): attachment is OfficeAttachmentDetails & { name: string } => Boolean(attachment?.name))
    .map((attachment) =>
      makeNormalizedAttachmentMetadata({
        attachmentId: attachment.id,
        name: attachment.name,
        contentType: attachment.contentType,
        sizeBytes: attachment.size,
        isInline: attachment.isInline
      })
    );
}

function getAsyncText(
  executor: (callback: (result: OfficeAsyncResult<string>) => void) => void,
  fallback = ""
) {
  return new Promise<string>((resolve, reject) => {
    executor((result) => {
      const failedStatus = getOfficeGlobal()?.AsyncResultStatus?.Failed ?? "failed";
      if (result.status === failedStatus) {
        if (fallback !== "") {
          resolve(fallback);
          return;
        }

        reject(new Error(result.error?.message || "Outlook returned an unknown async error."));
        return;
      }

      resolve(result.value ?? fallback);
    });
  });
}

async function readBodyText(item: OutlookMessageReadItem) {
  const office = getOfficeGlobal();
  const coercionType = office?.CoercionType?.Text ?? "text";
  const bodyMode = office?.MailboxEnums?.BodyMode?.HostConfig;

  return getAsyncText((callback) => {
    if (bodyMode) {
      item.body.getAsync(coercionType, { bodyMode }, callback);
      return;
    }

    item.body.getAsync(coercionType, callback);
  });
}

async function readBodyHtml(item: OutlookMessageReadItem) {
  const office = getOfficeGlobal();
  const coercionType = office?.CoercionType?.Html ?? "html";
  const bodyMode = office?.MailboxEnums?.BodyMode?.HostConfig;

  return getAsyncText(
    (callback) => {
      if (bodyMode) {
        item.body.getAsync(coercionType, { bodyMode }, callback);
        return;
      }

      item.body.getAsync(coercionType, callback);
    },
    ""
  );
}

async function readInternetHeaders(item: OutlookMessageReadItem) {
  if (!item.getAllInternetHeadersAsync) {
    return "";
  }

  return getAsyncText((callback) => item.getAllInternetHeadersAsync?.(callback), "");
}

function extractDateHeader(rawHeaders: string) {
  const match = rawHeaders.match(/^date:\s*(.+)$/im);
  if (!match?.[1]) {
    return "";
  }

  const parsed = new Date(match[1]);
  return Number.isNaN(parsed.getTime()) ? "" : parsed.toISOString();
}

function buildPreviewText(bodyText: string) {
  const collapsed = bodyText.replace(/\s+/g, " ").trim();
  return collapsed.slice(0, 180);
}

export async function readCurrentOutlookMessage(): Promise<NormalizedThread | null> {
  const readyInfo = await waitForOfficeReady();
  if (readyInfo?.host && readyInfo.host !== "Outlook") {
    return null;
  }

  const item = getMessageItem();
  if (!item) {
    return null;
  }

  const [bodyText, bodyHtml, rawHeaders] = await Promise.all([
    readBodyText(item),
    readBodyHtml(item),
    readInternetHeaders(item)
  ]);

  const from = normalizeRecipient(item.sender ?? item.from) ?? { email: "" };
  const sentAt = extractDateHeader(rawHeaders) || item.dateTimeCreated?.toISOString() || "";
  const subject = item.subject?.trim() || "Untitled thread";

  return {
    threadId: item.conversationId,
    subject,
    messages: [
      {
        messageId: item.itemId || item.conversationId || "outlook-item",
        threadId: item.conversationId,
        subject,
        from,
        toRecipients: normalizeRecipients(item.to),
        ccRecipients: normalizeRecipients(item.cc),
        sentAt,
        previewText: buildPreviewText(bodyText),
        bodyText,
        bodyHtml: bodyHtml || undefined,
        attachments: normalizeAttachments(item.attachments),
        isUnread: false
      }
    ]
  };
}
