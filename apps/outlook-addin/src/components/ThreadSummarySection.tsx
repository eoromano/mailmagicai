import type { ThreadSummary } from "../../../../packages/shared-types/src";
import { SectionCard } from "./SectionCard";

type ThreadSummarySectionProps = {
  summary: ThreadSummary;
};

export function ThreadSummarySection({ summary }: ThreadSummarySectionProps) {
  return (
    <SectionCard title="Thread Summary" subtitle="Quick read before replying">
      <p className="body-copy">{summary.summary}</p>
      <div className="summary-block">
        <p className="detail-list__title">Latest change</p>
        <p className="detail-list__detail">{summary.latestChange}</p>
      </div>
      <div className="summary-block">
        <p className="detail-list__title">Unresolved items</p>
        <ul className="bullet-list">
          {summary.unresolvedItems.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
      <div className="summary-block">
        <p className="detail-list__title">Who is waiting on whom</p>
        <ul className="bullet-list">
          {summary.whoIsWaitingOnWhom.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
      <div className="summary-grid">
        <div className="summary-block">
          <p className="detail-list__title">Deadlines</p>
          <ul className="bullet-list">
            {summary.deadlines.length > 0 ? (
              summary.deadlines.map((deadline) => <li key={deadline}>{deadline}</li>)
            ) : (
              <li>No explicit deadline detected.</li>
            )}
          </ul>
        </div>
        <div className="summary-block">
          <p className="detail-list__title">Important context</p>
          <ul className="bullet-list">
            {summary.importantContext.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </SectionCard>
  );
}
