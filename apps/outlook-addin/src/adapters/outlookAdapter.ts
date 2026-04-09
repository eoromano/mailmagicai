import { readCurrentOutlookMessage } from "./readCurrentMessage";
import type { OutlookAdapter } from "./types";

export function createOutlookAdapter(): OutlookAdapter {
  return {
    kind: "outlook",
    async getCurrentThread() {
      return readCurrentOutlookMessage();
    },
    async getUnreadThreads() {
      return [];
    }
  };
}
