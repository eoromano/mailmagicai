import { SectionCard } from "./SectionCard";

type FlagReasonsSectionProps = {
  reasons: string[];
};

export function FlagReasonsSection({ reasons }: FlagReasonsSectionProps) {
  return (
    <SectionCard title="Why this was flagged" subtitle="Signals that made this worth attention">
      <ul className="detail-list">
        {reasons.map((reason) => (
          <li key={reason} className="detail-list__item">
            <p className="detail-list__title">{reason}</p>
          </li>
        ))}
      </ul>
    </SectionCard>
  );
}
