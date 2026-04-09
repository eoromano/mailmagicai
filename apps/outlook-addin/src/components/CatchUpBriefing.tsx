import type { CatchUpBriefingItem, CatchUpOverview, UserSettings } from "../../../../packages/shared-types/src";
import { HeaderSection } from "./HeaderSection";
import { SettingsSection } from "./SettingsSection";
import { SectionCard } from "./SectionCard";
import type { StoredHistoryEntry } from "../lib/settingsStorage";

type CatchUpBriefingProps = {
  overview: CatchUpOverview;
  mode: "mock" | "api";
  isBusy: boolean;
  threadSubject: string;
  unreadCount: number;
  onScanThread: () => void;
  onCatchMeUp: () => void;
  onRefresh: () => void;
  settings: UserSettings;
  history: StoredHistoryEntry[];
  onSettingsChange: (settings: UserSettings) => void;
  onClearHistory: () => void;
  error?: string | null;
};

function BriefingList({
  title,
  subtitle,
  items
}: {
  title: string;
  subtitle: string;
  items: CatchUpBriefingItem[];
}) {
  return (
    <SectionCard title={title} subtitle={subtitle}>
      <ul className="detail-list">
        {items.length > 0 ? (
          items.map((item) => (
            <li key={item.id} className="detail-list__item">
              <p className="detail-list__title">{item.subject}</p>
              <p className="detail-list__detail">{item.whyItMatters}</p>
              <p className="detail-list__detail">Latest: {item.latestChange}</p>
              <p className="detail-list__detail">Next: {item.suggestedNextMove}</p>
            </li>
          ))
        ) : (
          <li className="detail-list__item">
            <p className="detail-list__detail">Nothing surfaced for this category right now.</p>
          </li>
        )}
      </ul>
    </SectionCard>
  );
}

export function CatchUpBriefing({
  overview,
  mode,
  isBusy,
  threadSubject,
  unreadCount,
  onScanThread,
  onCatchMeUp,
  onRefresh,
  settings,
  history,
  onSettingsChange,
  onClearHistory,
  error
}: CatchUpBriefingProps) {
  return (
    <main className="task-pane">
      <HeaderSection
        thread={{
          id: "catchup-mode",
          subject: `Catch me up briefing for ${threadSubject}`,
          participants: ["Unread threads"],
          messageCount: overview.overview.totalItems,
          unreadCount,
          lastMessageAt: new Date().toISOString(),
          messages: []
        }}
        mode={mode}
        isBusy={isBusy}
        onScanThread={onScanThread}
        onCatchMeUp={onCatchMeUp}
        onRefresh={onRefresh}
      />
      {error ? <p className="inline-status">Latest action failed: {error}</p> : null}
      <div className="task-pane__stack">
        <SettingsSection
          settings={settings}
          history={history}
          onChange={onSettingsChange}
          onClearHistory={onClearHistory}
        />
        <SectionCard title="Overview" subtitle="Unread thread briefing ranked by practical importance" tone="accent">
          <div className="overview-grid">
            <p className="detail-list__detail">Total items: {overview.overview.totalItems}</p>
            <p className="detail-list__detail">Needs action now: {overview.overview.needsActionNowCount}</p>
            <p className="detail-list__detail">Likely needs reply: {overview.overview.likelyNeedsReplyCount}</p>
            <p className="detail-list__detail">Important FYI: {overview.overview.importantFyiCount}</p>
            <p className="detail-list__detail">Copied only: {overview.overview.copiedOnlyCount}</p>
            <p className="detail-list__detail">Low-signal noise: {overview.overview.lowSignalNoiseCount}</p>
            <p className="detail-list__detail">At risk: {overview.overview.atRiskCount}</p>
          </div>
        </SectionCard>

        <BriefingList
          title="Top Action Items"
          subtitle="Threads most likely waiting on you"
          items={overview.topActionItems}
        />
        <BriefingList
          title="Important FYI"
          subtitle="Worth scanning for context"
          items={overview.importantFyiItems}
        />
        <BriefingList
          title="Copied Only"
          subtitle="Visible, but not clearly owned by you"
          items={overview.copiedOnlyItems}
        />
        <BriefingList
          title="Risk Items"
          subtitle="Urgent or at-risk threads that could be missed"
          items={overview.riskItems}
        />

        <SectionCard title="Themes" subtitle="Patterns across the unread queue">
          <ul className="bullet-list">
            {overview.themes.map((theme) => (
              <li key={theme}>{theme}</li>
            ))}
          </ul>
        </SectionCard>

        <BriefingList
          title="Suggested First 10 To Read"
          subtitle="Recommended reading order"
          items={overview.suggestedFirst10ToRead}
        />
      </div>
    </main>
  );
}
