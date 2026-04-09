import { SectionCard } from "./SectionCard";

type VerdictCardProps = {
  bucket: string;
  confidence: number;
  verdict: string;
};

export function VerdictCard({ bucket, confidence, verdict }: VerdictCardProps) {
  return (
    <SectionCard
      title="Verdict"
      subtitle="How urgent this thread looks right now"
      tone="accent"
      aside={<span className="section-note">{Math.round(confidence * 100)}% confidence</span>}
    >
      <p className="verdict-card__value">{verdict}</p>
      <p className="body-copy">Bucket: {bucket.split("_").join(" ")}</p>
    </SectionCard>
  );
}
