"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [passphrase, setPassphrase] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ passphrase }),
    });
    setSubmitting(false);
    if (res.ok) {
      router.push("/");
      router.refresh();
    } else {
      const data = await res.json().catch(() => ({ error: "login failed" }));
      setError(data.error ?? "login failed");
    }
  }

  return (
    <main style={{ maxWidth: 360, margin: "20vh auto", fontFamily: "system-ui, sans-serif" }}>
      <h1 style={{ fontSize: 20, marginBottom: 16 }}>DeskFlow</h1>
      <form onSubmit={onSubmit}>
        <input
          type="password"
          value={passphrase}
          onChange={(e) => setPassphrase(e.target.value)}
          placeholder="Access passphrase"
          autoFocus
          style={{ width: "100%", padding: 8, fontSize: 14, boxSizing: "border-box" }}
        />
        <button
          type="submit"
          disabled={submitting}
          style={{ width: "100%", padding: 8, marginTop: 8, fontSize: 14, cursor: "pointer" }}
        >
          {submitting ? "Checking…" : "Enter"}
        </button>
        {error && <p style={{ color: "crimson", fontSize: 13, marginTop: 8 }}>{error}</p>}
      </form>
    </main>
  );
}
