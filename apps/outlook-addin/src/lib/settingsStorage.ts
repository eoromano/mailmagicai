import { exampleUserSettings } from "../../../../packages/shared-types/src";
import type { UserSettings } from "../../../../packages/shared-types/src";

const SETTINGS_STORAGE_KEY = "threadsense.settings";
const HISTORY_STORAGE_KEY = "threadsense.history";
const MAX_HISTORY_ITEMS = 20;

export type StoredHistoryEntry = {
  action: "scan" | "catchup" | "refresh";
  at: string;
  subject: string;
};

export type SettingsStorage = {
  loadSettings(): UserSettings;
  saveSettings(settings: UserSettings): void;
  loadHistory(): StoredHistoryEntry[];
  appendHistory(entry: StoredHistoryEntry, settings: UserSettings): StoredHistoryEntry[];
  clearHistory(): void;
};

function canUseStorage() {
  return typeof window !== "undefined" && typeof window.localStorage !== "undefined";
}

function parseStoredValue<T>(key: string, fallback: T): T {
  if (!canUseStorage()) {
    return fallback;
  }

  const rawValue = window.localStorage.getItem(key);
  if (!rawValue) {
    return fallback;
  }

  try {
    return JSON.parse(rawValue) as T;
  } catch {
    return fallback;
  }
}

function writeStoredValue<T>(key: string, value: T) {
  if (!canUseStorage()) {
    return;
  }

  window.localStorage.setItem(key, JSON.stringify(value));
}

function sanitizeSettings(candidate?: Partial<UserSettings> | null): UserSettings {
  return {
    ...exampleUserSettings,
    ...candidate,
    vipSenders: candidate?.vipSenders ?? exampleUserSettings.vipSenders,
    priorityDomains: candidate?.priorityDomains ?? exampleUserSettings.priorityDomains,
    urgencyKeywords: candidate?.urgencyKeywords ?? exampleUserSettings.urgencyKeywords,
    copiedOnlyKeywords: candidate?.copiedOnlyKeywords ?? exampleUserSettings.copiedOnlyKeywords,
    draftVoicePreferences: candidate?.draftVoicePreferences ?? exampleUserSettings.draftVoicePreferences
  };
}

export function createLocalSettingsStorage(): SettingsStorage {
  return {
    loadSettings() {
      return sanitizeSettings(parseStoredValue<Partial<UserSettings>>(SETTINGS_STORAGE_KEY, exampleUserSettings));
    },
    saveSettings(settings) {
      writeStoredValue(SETTINGS_STORAGE_KEY, sanitizeSettings(settings));
    },
    loadHistory() {
      return parseStoredValue<StoredHistoryEntry[]>(HISTORY_STORAGE_KEY, []);
    },
    appendHistory(entry, settings) {
      if (!settings.saveHistory) {
        this.clearHistory();
        return [];
      }

      const updatedHistory = [entry, ...this.loadHistory()].slice(0, MAX_HISTORY_ITEMS);
      writeStoredValue(HISTORY_STORAGE_KEY, updatedHistory);
      return updatedHistory;
    },
    clearHistory() {
      if (!canUseStorage()) {
        return;
      }

      window.localStorage.removeItem(HISTORY_STORAGE_KEY);
    }
  };
}
