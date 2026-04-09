import { SectionCard } from "./SectionCard";

type SuggestedNextMoveSectionProps = {
  nextMove: string;
};

export function SuggestedNextMoveSection({ nextMove }: SuggestedNextMoveSectionProps) {
  return (
    <SectionCard title="Suggested Next Move" subtitle="A low-risk action to keep momentum">
      <p className="body-copy">{nextMove}</p>
    </SectionCard>
  );
}
