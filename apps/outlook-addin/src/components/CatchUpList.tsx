import { sampleTriageResponse } from "../data/mockData";

export function CatchUpList() {
  return (
    <ol className="catch-up-list">
      {sampleTriageResponse.catchUpList.map((item) => (
        <li key={item.id}>
          <p className="catch-up-title">{item.title}</p>
          <p>{item.detail}</p>
        </li>
      ))}
    </ol>
  );
}
