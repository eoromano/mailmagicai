import type { ExtractedAsk } from "../../../../packages/shared-types/src";
import { SectionCard } from "./SectionCard";

type DirectAsksSectionProps = {
  asks: ExtractedAsk[];
};

export function DirectAsksSection({ asks }: DirectAsksSectionProps) {
  return (
    <SectionCard title="Direct Asks" subtitle="Requests that appear to need an owner">
      <ul className="detail-list">
        {asks.map((ask) => (
          <li key={ask.id} className="detail-list__item">
            <p className="detail-list__title">{ask.text}</p>
            <p className="detail-list__detail">
              Type: {ask.askType.replace("_", " ")} • Owner: {ask.owner}
              {ask.targetPerson ? ` • From: ${ask.targetPerson}` : ""}
              {ask.dueDate ? ` • Due: ${ask.dueDate}` : ""}
              {` • Urgency: ${ask.urgency}`}
            </p>
            <p className="detail-list__detail">Source: {ask.sourceSnippet}</p>
          </li>
        ))}
      </ul>
    </SectionCard>
  );
}
