# DeskFlow

An agentic arXiv research tracker. Every week (or on demand), it fetches new papers in my research areas, extracts grounded facts from each abstract, scores relevance, logs everything to a personal Notion library, and sends me a ranked Telegram digest — replacing the chore of manually browsing arXiv and triaging papers by hand.

## Architecture

```
arXiv API ──► custom MCP server ◄── agent (MCP client)
                 │  arxiv_fetch           │  extract (LLM) → verify → retry
                 │  notion_add_paper      │  (grounded-or-"not stated",
                 │  notion_list_processed │   low-confidence → Needs Review)
                 │  telegram_send         ▼
                 ▼                   Notion "Papers" library
            Notion + Telegram APIs        ▲
                                           │ reads directly
                                 Next.js dashboard (Vercel)
                                   - passphrase-gated session
                                   - "Run now" → GitHub Actions workflow_dispatch
```

- **MCP server** (`src/mcp_server/`) exposes four typed, validated tools over the arXiv, Notion, and Telegram APIs. It's standalone — testable with the MCP Inspector, no agent logic inside it.
- **Agent** (`src/agent/`) is an MCP *client*: it spawns the server over stdio, pulls new papers, extracts structured fields per paper via an LLM, independently re-verifies the extraction before trusting it, and writes results to Notion / sends the Telegram digest.
- **No persistent backend.** This is a scheduled batch job, not a request/response service — `src/agent/run_digest.py` starts, does the work, and exits. GitHub Actions runs it weekly (`schedule`) and on-demand (`workflow_dispatch`, triggered by the dashboard).
- **Dashboard** (`dashboard/`) is a minimal Next.js app that reads the Notion library directly (server-side) and can trigger a real run via the GitHub API. It's read + trigger only — there's no approval gate, since the agent posts automatically once an extraction is verified.

## Verification — the part that matters most

The agent never invents a dataset or result. If an abstract doesn't state one, the extraction must contain the literal string `"not stated"`, not a plausible guess. Every extraction is independently re-checked before being trusted (`src/agent/verify.py`):

- An explicit `"not stated"` always passes — abstaining is a correct answer, not a failure.
- Any other value for `datasets`/`result` must have most of its significant words actually present in the abstract (token-overlap grounding), or it's rejected as likely invented.
- A `confidence: "low"` extraction is forced to `Needs Review` in Notion, regardless of what relevance label the model proposed — low-confidence calls get flagged for me, never silently trusted.
- On a failed check, the pipeline retries the extraction (up to twice) with the specific verification errors fed back into the prompt; on exhaustion it still logs the paper, marked `Needs Review`, rather than dropping it.

This design deliberately avoids three bugs diagnosed in an earlier project of mine (`langgraph-verify-agent`), whose citation-verification step this one is modeled on:
1. That project forces "unverified" whenever there's nothing to check — so a model correctly abstaining looks identical to a failed check. Here, `"not stated"` is explicitly treated as valid.
2. That project regex-extracts JSON from free-form model text (`\[.*\]`), which breaks on ordinary trailing chatter containing a stray bracket. Here, extraction uses **constrained structured output** at the SDK level instead — Ollama's `format` (JSON schema) for the local default, Anthropic's forced tool-use for the hosted swap — so there's no prose to parse.
3. That project requires an exact verbatim substring match for grounding, which flags correct-but-reworded claims as unsupported. Here, grounding is token-overlap against the abstract — strict enough to catch invention, lenient enough not to punish normal paraphrasing.

## Setup

1. **arXiv**: nothing to do — public API, no key.
2. **Notion**: create a database with properties `Title` (title), `ArxivID` (text), `Link` (url), `Summary`/`Datasets`/`Result` (text), `Relevance` (select: High/Medium/Low/Needs Review), `Status` (select: Unread/Read). Create an internal integration at `notion.so/my-integrations`, then **open the database → ••• → Connections → add the integration** (easy to miss; causes silent 403s otherwise).
3. **Telegram**: message `@BotFather` → `/newbot` → copy the token. Message your new bot once, then hit `https://api.telegram.org/bot<token>/getUpdates` to read your chat id.
4. **LLM**: install [Ollama](https://ollama.com) and `ollama pull mistral` for local/free use. Optionally set `ANTHROPIC_API_KEY` to use the hosted provider instead — **required** for the GitHub Actions workflow, since Ollama has nothing to run against on a hosted runner.
5. **GitHub** (for the dashboard's "Run now" button): once this repo is pushed, create a fine-grained PAT scoped to *only this repo*, with *only* the `Actions: write` permission.
6. Copy `.env.example` → `.env` and `dashboard/.env.local.example` → `dashboard/.env.local`, fill in the values above. Add the same secrets as GitHub Actions repo secrets for the scheduled workflow.

```
make install   # venv + editable install
make lint      # ruff
make test      # pytest
make eval      # score against the hand-labelled eval set (src/eval/dataset.py)
make run       # one real digest run
make inspector # MCP Inspector against the standalone server
```

## Trade-offs / what to harden next

- **Single-layer dashboard auth** (passphrase → signed, expiring cookie checked by middleware) is enough for a single-user personal tool, but a shared/team version should use real OAuth instead.
- **Least-privilege GitHub PAT**: the dispatch token is scoped to one repo and one permission (`Actions: write`) — if this project grows to need more automation, each capability should get its own narrowly-scoped token rather than widening this one.
- **Eval set is small (15–20 hand-labeled papers)**. It's enough to catch regressions and gate CI, not enough to tightly bound real-world accuracy — growing it is the highest-leverage next step.
- **Grounding threshold (`verify.py`'s token-overlap cutoff) is a heuristic**, tuned by inspection, not learned — worth revisiting if false positives/negatives show up in practice.
- **Deferred/stretch**: full-PDF parsing (currently abstract-only), a second delivery channel, a more polished/filterable dashboard, wrapping the MCP server as a Claude Code skill.
