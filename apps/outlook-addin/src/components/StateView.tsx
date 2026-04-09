type StateViewProps = {
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
};

export function StateView({ title, description, actionLabel, onAction }: StateViewProps) {
  return (
    <section className="state-view">
      <p className="eyebrow">ThreadSense</p>
      <h2>{title}</h2>
      <p>{description}</p>
      {actionLabel ? (
        <button className="state-view__action" type="button" onClick={onAction}>
          {actionLabel}
        </button>
      ) : null}
    </section>
  );
}
