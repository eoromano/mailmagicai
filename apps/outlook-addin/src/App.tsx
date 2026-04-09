import { useEffect } from "react";
import { CatchUpBriefing } from "./components/CatchUpBriefing";
import { LoadingPane } from "./components/LoadingPane";
import { SettingsSection } from "./components/SettingsSection";
import { StateView } from "./components/StateView";
import { TaskPaneContent } from "./components/TaskPaneContent";
import { useThreadSense } from "./hooks/useThreadSense";

export function App() {
  const { adapterMode, clearHistory, data, error, history, isLoading, lastAction, mode, settings, setSettings, view, runAction } =
    useThreadSense();

  useEffect(() => {
    void runAction("scan");
  }, [runAction]);

  return (
    <div className="app-frame">
      <aside className="app-shell">
        <div className="dev-toolbar" aria-label="Connection state">
          <span className="dev-toolbar__status">{mode === "api" ? "Local API" : "Mock data"}</span>
          <span className="dev-toolbar__status muted">{adapterMode === "outlook" ? "Outlook source" : "Mock source"}</span>
          {lastAction ? <span className="dev-toolbar__status muted">Last action: {lastAction}</span> : null}
        </div>

        {isLoading && !data ? <LoadingPane /> : null}
        {!isLoading && !data && !error ? (
          <>
            <StateView
              title={adapterMode === "outlook" ? "No Outlook message available" : "No thread selected"}
              description={
                adapterMode === "outlook"
                  ? "The Outlook adapter stub can only read the current message context. Open a message in reading mode, or switch to mock source for local fixtures."
                  : "Open an email thread to see a summary, direct asks, and a draft reply in this panel."
              }
              actionLabel="Scan this thread"
              onAction={() => void runAction("scan")}
            />
            <div className="task-pane__stack">
              <SettingsSection
                settings={settings}
                history={history}
                onChange={setSettings}
                onClearHistory={clearHistory}
              />
            </div>
          </>
        ) : null}
        {error && !data ? (
          <>
            <StateView
              title="Unable to load ThreadSense"
              description={error}
              actionLabel="Refresh"
              onAction={() => void runAction("refresh")}
            />
            <div className="task-pane__stack">
              <SettingsSection
                settings={settings}
                history={history}
                onChange={setSettings}
                onClearHistory={clearHistory}
              />
            </div>
          </>
        ) : null}
        {data && view === "thread" ? (
          <TaskPaneContent
            thread={data.thread}
            mode={mode}
            isBusy={isLoading}
            error={error}
            onScanThread={() => void runAction("scan")}
            onCatchMeUp={() => void runAction("catchup")}
            onRefresh={() => void runAction("refresh")}
            settings={settings}
            history={history}
            onSettingsChange={setSettings}
            onClearHistory={clearHistory}
            triage={data.triage}
            summary={data.summary}
            askExtraction={data.askExtraction}
            draftReplySet={data.draftReplySet}
            catchUpOverview={data.catchUpOverview}
            thoughtPartner={data.thoughtPartner}
          />
        ) : null}
        {data && view === "catchup" ? (
          <CatchUpBriefing
            overview={data.catchUpOverview}
            mode={mode}
            isBusy={isLoading}
            threadSubject={data.thread.subject}
            unreadCount={data.thread.unreadCount}
            error={error}
            onScanThread={() => void runAction("scan")}
            onCatchMeUp={() => void runAction("catchup")}
            onRefresh={() => void runAction("refresh")}
            settings={settings}
            history={history}
            onSettingsChange={setSettings}
            onClearHistory={clearHistory}
          />
        ) : null}
      </aside>
    </div>
  );
}
