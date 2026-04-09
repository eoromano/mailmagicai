import { PropsWithChildren } from "react";

type PanelSectionProps = PropsWithChildren<{
  title: string;
}>;

export function PanelSection({ title, children }: PanelSectionProps) {
  return (
    <section className="panel-section">
      <div className="section-heading">
        <h3>{title}</h3>
      </div>
      <div className="section-body">{children}</div>
    </section>
  );
}
