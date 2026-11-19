import RunNowButton from "../components/RunNowButton";
import { listPapers, type PaperRow } from "../lib/notion";

const RELEVANCE_OPTIONS = ["High", "Medium", "Low", "Needs Review"];
const STATUS_OPTIONS = ["Unread", "Read"];

export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ relevance?: string; status?: string }>;
}) {
  const { relevance, status } = await searchParams;

  let papers: PaperRow[] = [];
  let loadError: string | null = null;
  try {
    papers = await listPapers({ relevance, status });
  } catch (e) {
    loadError = (e as Error).message;
  }

  function filterHref(key: "relevance" | "status", value?: string): string {
    const params = new URLSearchParams();
    const nextRelevance = key === "relevance" ? value : relevance;
    const nextStatus = key === "status" ? value : status;
    if (nextRelevance) params.set("relevance", nextRelevance);
    if (nextStatus) params.set("status", nextStatus);
    const qs = params.toString();
    return qs ? `/?${qs}` : "/";
  }

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: 24, maxWidth: 960, margin: "0 auto" }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <h1 style={{ fontSize: 22 }}>DeskFlow — Papers</h1>
        <RunNowButton />
      </header>

      <nav style={{ marginBottom: 16, fontSize: 13 }}>
        <span>Relevance: </span>
        <a href={filterHref("relevance", undefined)} style={{ fontWeight: !relevance ? 700 : 400 }}>
          All
        </a>
        {RELEVANCE_OPTIONS.map((r) => (
          <span key={r}>
            {" | "}
            <a href={filterHref("relevance", r)} style={{ fontWeight: relevance === r ? 700 : 400 }}>
              {r}
            </a>
          </span>
        ))}
        <span style={{ marginLeft: 16 }}>Status: </span>
        <a href={filterHref("status", undefined)} style={{ fontWeight: !status ? 700 : 400 }}>
          All
        </a>
        {STATUS_OPTIONS.map((s) => (
          <span key={s}>
            {" | "}
            <a href={filterHref("status", s)} style={{ fontWeight: status === s ? 700 : 400 }}>
              {s}
            </a>
          </span>
        ))}
      </nav>

      {loadError && <p style={{ color: "crimson" }}>Failed to load papers: {loadError}</p>}

      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "1px solid #ddd" }}>
            <th style={{ padding: "6px 4px" }}>Relevance</th>
            <th style={{ padding: "6px 4px" }}>Title</th>
            <th style={{ padding: "6px 4px" }}>Summary</th>
            <th style={{ padding: "6px 4px" }}>Datasets</th>
            <th style={{ padding: "6px 4px" }}>Result</th>
          </tr>
        </thead>
        <tbody>
          {papers.map((p) => (
            <tr key={p.arxivId} style={{ borderBottom: "1px solid #eee", verticalAlign: "top" }}>
              <td style={{ padding: "6px 4px" }}>{p.relevance}</td>
              <td style={{ padding: "6px 4px" }}>
                <a href={p.link} target="_blank" rel="noreferrer">
                  {p.title}
                </a>
              </td>
              <td style={{ padding: "6px 4px" }}>{p.summary}</td>
              <td style={{ padding: "6px 4px" }}>{p.datasets}</td>
              <td style={{ padding: "6px 4px" }}>{p.result}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {!loadError && papers.length === 0 && <p>No papers yet.</p>}
    </main>
  );
}
