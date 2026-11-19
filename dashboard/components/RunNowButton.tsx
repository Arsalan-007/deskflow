"use client";

import { useState } from "react";

export default function RunNowButton() {
  const [state, setState] = useState<"idle" | "running" | "done" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  async function onClick() {
    setState("running");
    setError(null);
    const res = await fetch("/api/run-now", { method: "POST" });
    const data = await res.json().catch(() => ({ ok: false, error: "bad response" }));
    if (data.ok) {
      setState("done");
    } else {
      setState("error");
      setError(data.error ?? "run failed");
    }
  }

  return (
    <div style={{ display: "inline-flex", alignItems: "center", gap: 8 }}>
      <button onClick={onClick} disabled={state === "running"} style={{ padding: "6px 12px", cursor: "pointer" }}>
        {state === "running" ? "Starting…" : "Run now"}
      </button>
      {state === "done" && <span style={{ color: "seagreen", fontSize: 13 }}>Triggered — check GitHub Actions.</span>}
      {state === "error" && <span style={{ color: "crimson", fontSize: 13 }}>{error}</span>}
    </div>
  );
}
