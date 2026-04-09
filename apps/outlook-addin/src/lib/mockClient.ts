import {
  exampleAskExtractionResult,
  exampleCatchUpOverview,
  exampleDraftReplySet,
  exampleThoughtPartnerResult,
  exampleThreadSummary,
  exampleTriageResult
} from "../../../../packages/shared-types/src";
import type { CatchUpRequestPayload, ThreadRequestPayload } from "./apiClient";

function wait(ms: number) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

export function createMockClient() {
  return {
    async triageThread(_: ThreadRequestPayload) {
      await wait(250);
      return exampleTriageResult;
    },
    async summarizeThread(_: ThreadRequestPayload) {
      await wait(180);
      return exampleThreadSummary;
    },
    async extractAsks(_: ThreadRequestPayload) {
      await wait(180);
      return exampleAskExtractionResult;
    },
    async draftReply(_: ThreadRequestPayload) {
      await wait(180);
      return exampleDraftReplySet;
    },
    async catchUp(_: CatchUpRequestPayload) {
      await wait(180);
      return exampleCatchUpOverview;
    },
    async thoughtPartner(_: ThreadRequestPayload) {
      await wait(180);
      return exampleThoughtPartnerResult;
    }
  };
}
