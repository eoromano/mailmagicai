import type { DraftReplySet } from "../../../../packages/shared-types/src";
import { SectionCard } from "./SectionCard";

type DraftReplySectionProps = {
  draftReplySet: DraftReplySet;
};

export function DraftReplySection({ draftReplySet }: DraftReplySectionProps) {
  return (
    <SectionCard
      title="Draft Reply"
      subtitle="Editable starting point for a response"
      aside={<span className="section-note">3 options</span>}
    >
      <div className="draft-stack">
        {[
          ["Short reply", draftReplySet.shortReply, draftReplySet.notesOnWhenToUseEach.shortReply],
          ["Strategic reply", draftReplySet.strategicReply, draftReplySet.notesOnWhenToUseEach.strategicReply],
          ["Clarifying reply", draftReplySet.clarifyingReply, draftReplySet.notesOnWhenToUseEach.clarifyingReply]
        ].map(([label, body, note]) => (
          <div key={label} className="draft-option">
            <p className="detail-list__title">{label}</p>
            <p className="detail-list__detail">{note}</p>
            <div className="draft-reply">
              {(body as string).split("\n").map((line, index) => (
                <p key={`${label}-${line}-${index}`}>{line || "\u00A0"}</p>
              ))}
            </div>
          </div>
        ))}
      </div>
    </SectionCard>
  );
}
