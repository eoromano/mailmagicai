import { useMemo, useState } from "react";
import type { UserSettings } from "../../../../packages/shared-types/src";
import type { StoredHistoryEntry } from "../lib/settingsStorage";
import { SectionCard } from "./SectionCard";

type SettingsSectionProps = {
  settings: UserSettings;
  history: StoredHistoryEntry[];
  onChange: (settings: UserSettings) => void;
  onClearHistory: () => void;
};

function listToTextarea(values: string[]) {
  return values.join("\n");
}

function textareaToList(value: string) {
  return value
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
}

export function SettingsSection({ settings, history, onChange, onClearHistory }: SettingsSectionProps) {
  const [isOpen, setIsOpen] = useState(false);
  const historySummary = useMemo(() => {
    if (!settings.saveHistory) {
      return "History is off. No local activity is retained.";
    }

    if (history.length === 0) {
      return "History is on, but nothing has been saved locally yet.";
    }

    return `${history.length} recent actions are stored only on this device.`;
  }, [history.length, settings.saveHistory]);

  return (
    <SectionCard
      title="Settings"
      subtitle="Local preferences for ranking, drafting, and privacy."
      aside={
        <button className="action-button action-button--secondary action-button--small" type="button" onClick={() => setIsOpen((value) => !value)}>
          {isOpen ? "Hide" : "Edit"}
        </button>
      }
    >
      <p className="detail-list__detail">
        These preferences are stored locally first. Nothing here is synced to a backend yet.
      </p>
      <p className="detail-list__detail">{historySummary}</p>

      {isOpen ? (
        <div className="settings-form">
          <label className="settings-field">
            <span className="settings-field__label">VIP senders</span>
            <textarea
              className="settings-input settings-textarea"
              value={listToTextarea(settings.vipSenders)}
              onChange={(event) => onChange({ ...settings, vipSenders: textareaToList(event.target.value) })}
              rows={3}
            />
          </label>

          <label className="settings-field">
            <span className="settings-field__label">Priority domains</span>
            <textarea
              className="settings-input settings-textarea"
              value={listToTextarea(settings.priorityDomains)}
              onChange={(event) => onChange({ ...settings, priorityDomains: textareaToList(event.target.value) })}
              rows={3}
            />
          </label>

          <label className="settings-field">
            <span className="settings-field__label">Urgency keywords</span>
            <textarea
              className="settings-input settings-textarea"
              value={listToTextarea(settings.urgencyKeywords)}
              onChange={(event) => onChange({ ...settings, urgencyKeywords: textareaToList(event.target.value) })}
              rows={3}
            />
          </label>

          <label className="settings-field">
            <span className="settings-field__label">Copied-only keywords</span>
            <textarea
              className="settings-input settings-textarea"
              value={listToTextarea(settings.copiedOnlyKeywords)}
              onChange={(event) => onChange({ ...settings, copiedOnlyKeywords: textareaToList(event.target.value) })}
              rows={3}
            />
          </label>

          <label className="settings-field">
            <span className="settings-field__label">Draft voice preferences</span>
            <textarea
              className="settings-input settings-textarea"
              value={listToTextarea(settings.draftVoicePreferences)}
              onChange={(event) => onChange({ ...settings, draftVoicePreferences: textareaToList(event.target.value) })}
              rows={3}
            />
          </label>

          <label className="settings-field">
            <span className="settings-field__label">Reply tone</span>
            <select
              className="settings-input"
              value={settings.replyTone}
              onChange={(event) => onChange({ ...settings, replyTone: event.target.value as UserSettings["replyTone"] })}
            >
              <option value="neutral">Neutral</option>
              <option value="warm">Warm</option>
              <option value="direct">Direct</option>
            </select>
          </label>

          <label className="settings-toggle">
            <input
              type="checkbox"
              checked={settings.saveHistory}
              onChange={(event) => onChange({ ...settings, saveHistory: event.target.checked })}
            />
            <span>Save action history on this device</span>
          </label>

          <label className="settings-toggle">
            <input
              type="checkbox"
              checked={settings.mockMode}
              onChange={(event) => onChange({ ...settings, mockMode: event.target.checked })}
            />
            <span>Use mock mode for the add-in</span>
          </label>

          {history.length > 0 ? (
            <div className="settings-history">
              <div className="settings-history__header">
                <p className="settings-field__label">Recent local activity</p>
                <button className="action-button action-button--secondary action-button--small" type="button" onClick={onClearHistory}>
                  Clear
                </button>
              </div>
              <ul className="detail-list">
                {history.slice(0, 5).map((entry) => (
                  <li key={`${entry.at}-${entry.action}`} className="detail-list__item">
                    <p className="detail-list__detail">
                      {entry.action} • {entry.subject} • {new Date(entry.at).toLocaleString()}
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </div>
      ) : null}
    </SectionCard>
  );
}
