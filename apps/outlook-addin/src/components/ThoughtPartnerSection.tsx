import type { ThoughtPartnerResult } from "../../../../packages/shared-types/src";
import { SectionCard } from "./SectionCard";

type ThoughtPartnerSectionProps = {
  result: ThoughtPartnerResult;
};

export function ThoughtPartnerSection({ result }: ThoughtPartnerSectionProps) {
  return (
    <SectionCard title="Thought Partner" subtitle="Grounded analysis for what is really happening">
      <div className="summary-block">
        <p className="detail-list__title">What is the real issue here</p>
        <ul className="bullet-list">
          {result.issue.evidence.map((item) => (
            <li key={item}>Evidence: {item}</li>
          ))}
        </ul>
        <p className="detail-list__detail">Inference: {result.issue.inference}</p>
      </div>

      <div className="summary-block">
        <p className="detail-list__title">What is being asked of me explicitly and implicitly</p>
        <ul className="bullet-list">
          {result.explicitAsks.map((ask) => (
            <li key={ask}>{ask}</li>
          ))}
        </ul>
      </div>

      <div className="summary-block">
        <p className="detail-list__title">What are the stakeholder dynamics</p>
        <ul className="bullet-list">
          {result.implicitDynamics.evidence.map((item) => (
            <li key={item}>Evidence: {item}</li>
          ))}
        </ul>
        <p className="detail-list__detail">Inference: {result.implicitDynamics.inference}</p>
      </div>

      <div className="summary-block">
        <p className="detail-list__title">What is the risk if I do nothing</p>
        <ul className="bullet-list">
          {result.risks.map((risk) => (
            <li key={risk}>{risk}</li>
          ))}
        </ul>
      </div>

      <div className="summary-block">
        <p className="detail-list__title">What is the smartest next move</p>
        <ul className="bullet-list">
          {result.options.map((option) => (
            <li key={option}>{option}</li>
          ))}
        </ul>
        <p className="detail-list__detail">Recommended: {result.recommendedMove}</p>
      </div>

      <div className="summary-block">
        <p className="detail-list__title">Confidence notes</p>
        <p className="detail-list__detail">{result.confidenceNotes}</p>
      </div>
    </SectionCard>
  );
}
