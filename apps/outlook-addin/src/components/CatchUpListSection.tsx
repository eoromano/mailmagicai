import type { CatchUpOverview } from "../../../../packages/shared-types/src";
import { SectionCard } from "./SectionCard";

type CatchUpListSectionProps = {
  overview: CatchUpOverview;
};

export function CatchUpListSection({ overview }: CatchUpListSectionProps) {
  return (
    <SectionCard
      title="Catch Up List"
      subtitle={`Top action items: ${overview.overview.needsActionNowCount + overview.overview.likelyNeedsReplyCount}`}
    >
      <ol className="catch-up-list">
        {overview.topActionItems.length > 0 ? (
          overview.topActionItems.map((item) => (
            <li key={item.id}>
              <p className="detail-list__title">{item.subject}</p>
              <p className="detail-list__detail">{item.whyItMatters}</p>
            </li>
          ))
        ) : (
          overview.suggestedFirst10ToRead.slice(0, 3).map((item) => (
            <li key={item.id}>
              <p className="detail-list__title">{item.subject}</p>
              <p className="detail-list__detail">{item.whyItMatters}</p>
            </li>
          ))
        )}
      </ol>
    </SectionCard>
  );
}
