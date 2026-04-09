import { PropsWithChildren, ReactNode } from "react";

type SectionCardProps = PropsWithChildren<{
  title: string;
  subtitle?: string;
  tone?: "default" | "accent";
  aside?: ReactNode;
}>;

export function SectionCard({
  title,
  subtitle,
  tone = "default",
  aside,
  children
}: SectionCardProps) {
  return (
    <section className={`section-card section-card--${tone}`}>
      <div className="section-card__header">
        <div>
          <h3>{title}</h3>
          {subtitle ? <p className="section-card__subtitle">{subtitle}</p> : null}
        </div>
        {aside ? <div className="section-card__aside">{aside}</div> : null}
      </div>
      <div className="section-card__body">{children}</div>
    </section>
  );
}
