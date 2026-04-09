export function LoadingPane() {
  return (
    <section className="loading-pane" aria-live="polite" aria-busy="true">
      <div className="loading-pane__header">
        <div className="skeleton skeleton--eyebrow" />
        <div className="skeleton skeleton--title" />
        <div className="skeleton skeleton--line" />
      </div>
      {Array.from({ length: 6 }).map((_, index) => (
        <div key={index} className="loading-card">
          <div className="skeleton skeleton--section-title" />
          <div className="skeleton skeleton--line" />
          <div className="skeleton skeleton--line short" />
        </div>
      ))}
    </section>
  );
}
