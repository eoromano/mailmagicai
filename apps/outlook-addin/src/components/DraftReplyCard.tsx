import { sampleTriageResponse } from "../data/mockData";
import { PanelSection } from "./PanelSection";

export function DraftReplyCard() {
  return (
    <PanelSection title="Draft Reply">
      <div className="draft-reply">
        {sampleTriageResponse.draftReply.split("\n").map((line) => (
          <p key={line}>{line}</p>
        ))}
      </div>
    </PanelSection>
  );
}
