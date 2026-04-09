import { exampleEmailThread, exampleUnreadThreads } from "../../../../packages/shared-types/src";
import { normalizeMockThread } from "./normalize";
import type { OutlookAdapter } from "./types";

function wait(ms: number) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

export function createMockOutlookAdapter(): OutlookAdapter {
  return {
    kind: "mock",
    async getCurrentThread() {
      await wait(80);
      return normalizeMockThread(exampleEmailThread);
    },
    async getUnreadThreads() {
      await wait(80);
      return exampleUnreadThreads.map(normalizeMockThread);
    }
  };
}
