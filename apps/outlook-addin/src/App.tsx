import { CatchUpList } from "./components/CatchUpList";
import { DraftReplyCard } from "./components/DraftReplyCard";
import { PanelSection } from "./components/PanelSection";
import { sampleThread, sampleTriageResponse } from "./data/mockData";

export function App() {
  return (
    <main className="app-shell">
      <header className="panel-header">
        <div>
          <p className="eyebrow">Inbox Triage</p>
          <h1>Mock Outlook Task Pane</h1>
        </div>
        <span className="mode-badge">Mock mode only</span>
      </header>

      <section className="thread-context">
        <p className="thread-label">Current thread</p>
        <h2>{sampleThread.subject}</h2>
        <p>
          {sampleThread.participants.join(", ")} • {sampleThread.messageCount} messages
        </p>
      </section>

      <div className="panel-grid">
        <PanelSection title="Verdict">
          <p className="verdict">{sampleTriageResponse.verdict}</p>
          <p>{sampleTriageResponse.rationale}</p>
        </PanelSection>

        <PanelSection title="Summary">
          <p>{sampleTriageResponse.summary.overview}</p>
          <ul>
            {sampleTriageResponse.summary.bullets.map((bullet) => (
              <li key={bullet}>{bullet}</li>
            ))}
          </ul>
        </PanelSection>

        <PanelSection title="Direct Asks">
          <ul>
            {sampleTriageResponse.directAsks.map((ask) => (
              <li key={ask.id}>
                <strong>{ask.owner}</strong>: {ask.request}
              </li>
            ))}
          </ul>
        </PanelSection>

        <DraftReplyCard />

        <PanelSection title="Catch Up List">
          <CatchUpList />
        </PanelSection>
      </div>
    </main>
  );
}
