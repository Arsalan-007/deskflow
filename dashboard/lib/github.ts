export async function dispatchDigestWorkflow(): Promise<void> {
  const token = process.env.GITHUB_DISPATCH_TOKEN;
  const repo = process.env.GITHUB_REPO; // "owner/deskflow"
  if (!token || !repo) {
    throw new Error("GITHUB_DISPATCH_TOKEN / GITHUB_REPO not configured");
  }
  const res = await fetch(`https://api.github.com/repos/${repo}/actions/workflows/digest.yml/dispatches`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
    },
    body: JSON.stringify({ ref: "main" }),
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`GitHub dispatch failed: ${res.status} ${body}`);
  }
}
