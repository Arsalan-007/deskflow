import { Client } from "@notionhq/client";

export interface PaperRow {
  arxivId: string;
  title: string;
  link: string;
  summary: string;
  datasets: string;
  result: string;
  relevance: string;
  status: string;
}

function text(prop: unknown): string {
  const arr = (prop as { rich_text?: { plain_text: string }[] })?.rich_text;
  return arr?.[0]?.plain_text ?? "";
}

function title(prop: unknown): string {
  const arr = (prop as { title?: { plain_text: string }[] })?.title;
  return arr?.[0]?.plain_text ?? "";
}

function select(prop: unknown): string {
  return (prop as { select?: { name: string } })?.select?.name ?? "";
}

export interface PaperFilters {
  relevance?: string;
  status?: string;
}

export async function listPapers(filters: PaperFilters): Promise<PaperRow[]> {
  const token = process.env.NOTION_TOKEN;
  const databaseId = process.env.NOTION_DATABASE_ID;
  if (!token || !databaseId) {
    throw new Error("NOTION_TOKEN / NOTION_DATABASE_ID not configured");
  }
  const notion = new Client({ auth: token });

  const andFilters = [];
  if (filters.relevance) andFilters.push({ property: "Relevance", select: { equals: filters.relevance } });
  if (filters.status) andFilters.push({ property: "Status", select: { equals: filters.status } });

  const rows: PaperRow[] = [];
  let cursor: string | undefined;
  do {
    const resp = await notion.databases.query({
      database_id: databaseId,
      filter: andFilters.length ? { and: andFilters } : undefined,
      page_size: 50,
      start_cursor: cursor,
    });
    for (const page of resp.results) {
      if (!("properties" in page)) continue;
      const p = page.properties;
      rows.push({
        arxivId: text(p.ArxivID),
        title: title(p.Title),
        link: (p.Link as { url?: string })?.url ?? "",
        summary: text(p.Summary),
        datasets: text(p.Datasets),
        result: text(p.Result),
        relevance: select(p.Relevance),
        status: select(p.Status),
      });
    }
    cursor = resp.has_more ? resp.next_cursor ?? undefined : undefined;
  } while (cursor);

  return rows;
}
