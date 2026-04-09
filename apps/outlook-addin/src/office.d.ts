declare global {
  type OfficeHostType = "Outlook" | string;

  type OfficeReadyInfo = {
    host: OfficeHostType | null;
    platform?: string | null;
  };

  type OfficeAsyncResultStatus = "succeeded" | "failed";

  type OfficeAsyncResult<T> = {
    status: OfficeAsyncResultStatus;
    value: T;
    error?: {
      code?: number | string;
      message: string;
    };
  };

  type OfficeEmailAddressDetails = {
    displayName?: string;
    emailAddress?: string;
  };

  type OfficeAttachmentDetails = {
    id?: string;
    name?: string;
    contentType?: string;
    size?: number;
    isInline?: boolean;
  };

  type OfficeBody = {
    getAsync(
      coercionType: string,
      callback: (result: OfficeAsyncResult<string>) => void
    ): void;
    getAsync(
      coercionType: string,
      options: { bodyMode?: string },
      callback: (result: OfficeAsyncResult<string>) => void
    ): void;
  };

  type OfficeMessageReadItem = {
    itemId?: string;
    conversationId?: string;
    itemType?: string;
    subject?: string;
    from?: OfficeEmailAddressDetails;
    sender?: OfficeEmailAddressDetails;
    to?: OfficeEmailAddressDetails[];
    cc?: OfficeEmailAddressDetails[];
    attachments: OfficeAttachmentDetails[];
    dateTimeCreated?: Date;
    body: OfficeBody;
    getAllInternetHeadersAsync?: (callback: (result: OfficeAsyncResult<string>) => void) => void;
  };

  type OfficeMailbox = {
    item?: OfficeMessageReadItem | null;
  };

  type OfficeContext = {
    mailbox?: OfficeMailbox;
  };

  type OfficeGlobal = {
    context?: OfficeContext;
    onReady?: () => Promise<OfficeReadyInfo>;
    AsyncResultStatus?: {
      Succeeded: OfficeAsyncResultStatus;
      Failed: OfficeAsyncResultStatus;
    };
    CoercionType?: {
      Html: string;
      Text: string;
    };
    MailboxEnums?: {
      ItemType?: {
        Message: string;
      };
      BodyMode?: {
        HostConfig: string;
        FullBody: string;
      };
    };
  };

  interface Window {
    Office?: OfficeGlobal;
  }

  const Office: OfficeGlobal | undefined;
}

export {};
