import type { EmailThread } from "../../../../packages/shared-types/src";

type HeaderSectionProps = {
  thread: EmailThread;
  mode: "mock" | "api";
  isBusy: boolean;
  onScanThread: () => void;
  onCatchMeUp: () => void;
  onRefresh: () => void;
};

export function HeaderSection({
  thread,
  mode,
  isBusy,
  onScanThread,
  onCatchMeUp,
  onRefresh
}: HeaderSectionProps) {
  return (
    <header className="task-pane-header">
      <div>
        <p className="eyebrow">ThreadSense</p>
        <h1>Email thread copilot</h1>
        <p className="task-pane-header__subtitle">
          Compact support for catching up on unread mail in {mode === "api" ? "local API mode" : "mock mode"}.
        </p>
      </div>
      <span className="mode-badge">{mode === "api" ? "Local API mode" : "Mock mode"}</span>

      <div className="action-row">
        <button className="action-button" type="button" onClick={onScanThread} disabled={isBusy}>
          Scan this thread
        </button>
        <button className="action-button action-button--secondary" type="button" onClick={onCatchMeUp} disabled={isBusy}>
          Catch me up
        </button>
        <button className="action-button action-button--secondary" type="button" onClick={onRefresh} disabled={isBusy}>
          Refresh
        </button>
      </div>

      <section className="thread-strip" aria-label="Current thread">
        <p className="thread-strip__label">Current thread</p>
        <h2>{thread.subject}</h2>
        <p className="thread-strip__meta">
          {thread.participants.join(", ")} • {thread.messageCount} messages • {thread.unreadCount} unread
        </p>
      </section>
    </header>
  );
}
