# India weather — Flask POC

Small web app: pick an Indian city, submit, see **mock** current temperature and **date/time in IST**. No API keys or external calls.

## Layout

- `app/` — application package (factory, config, blueprints, services, templates, static)
- `wsgi.py` — dev server and Gunicorn entry
- `tests/` — pytest smoke tests
- [`REVIEW.md`](REVIEW.md) — **PR / code review rules** (Python, Flask, security, severity rubric)

## Local setup

```bash
cd /path/to/rala-claude-code-review-poc
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt   # optional, for tests
cp .env.example .env                    # optional
python wsgi.py
```

Open http://127.0.0.1:5000

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `FLASK_ENV` | `development` | `development` or `production` |
| `SECRET_KEY` | dev placeholder | Session / CSRF secret (set in production) |
| `USE_MOCK_WEATHER` | `true` | Must stay `true` unless you add a real HTTP provider |

## Production-style run (Gunicorn)

```bash
gunicorn -w 2 -b 127.0.0.1:8000 wsgi:app
```

## Tests

Run from the repository root (so the `app` package resolves):

```bash
pytest -q
```

`pyproject.toml` sets `pythonpath = ["."]` for pytest so `from app import create_app` works without installing the project.

## Mock data

Editable in `app/services/mock_weather.py` (`MOCK_BY_CITY_ID`). City list in `app/data/indian_cities.py`.

---

## Claude PR review (GitHub Actions)

Workflow: [`.github/workflows/claude-pr-review.yml`](.github/workflows/claude-pr-review.yml).

On `pull_request` (`opened`, `synchronize`, `reopened`), [Claude Code Action](https://github.com/anthropics/claude-code-action) reviews the diff and posts **one top-level PR comment** via `gh pr comment`. It does **not** merge or approve; you review and merge manually.

### Setup

1. Push this repo to GitHub and enable **Actions**.
2. Add a repository secret **`ANTHROPIC_API_KEY`** (from [Anthropic Console](https://console.anthropic.com/)).
3. Optional: install the [Claude GitHub App](https://github.com/apps/claude) if you follow Anthropic’s guided setup; the workflow still needs the API key as in [their docs](https://code.claude.com/docs/en/github-actions).

### PR-agent setup checklist

| Step | Status | Notes |
|------|--------|--------|
| `.env` not committed | Done in repo | `.env` is in [`.gitignore`](.gitignore); never `git add .env`. |
| Pin Claude Code Action | Done in repo | Workflow uses commit SHA for `v1` (see YAML); bump SHA when upgrading. |
| Commit and push to GitHub | **You** | `git add` / `git commit` / `git push` (remote `origin` must exist). |
| Add `ANTHROPIC_API_KEY` secret | **You** (when ready) | Repo **Settings → Secrets and variables → Actions**. Until then the workflow **skips** the review job—no failure. |
| Enable Actions | **You** | Repo **Settings → Actions → General** if previously disabled. |
| Smoke-test with a PR | **You** | Open any PR from a branch on this repo; check **Actions** tab and one bot comment on the PR. |
| Branch protection (optional) | **You** | Protect `main`; keep this workflow **non-required** if you do not want failed runs to block merge. |
| Billing alerts (optional) | **You** | [Anthropic console](https://console.anthropic.com/) / org usage for API spend. |

### Notes

- **No API key yet:** If **`ANTHROPIC_API_KEY`** is not set in repo secrets, the review job is **skipped** (workflow does not fail). Add the secret when you have a key; the next PR will run the review.
- **Fork PRs** are skipped (secrets are not available to workflows from forks).
- **Branch protection:** Leave this workflow **non-required** if you never want a failed review run to block merges; merging stays a human decision either way.
- **Cost:** Anthropic API usage applies per run; cancel-in-progress is enabled per PR to reduce duplicate runs.

### Customizing what Claude checks

You can mix and match what fits your team. Typical choices:

| Where to edit | What it’s for | When to use it |
|---------------|----------------|----------------|
| **[`REVIEW.md`](REVIEW.md)** | **Canonical** review policy: Flask/Python/security, severity rubric, what to skip. | **Start here.** The workflow instructs Claude to **read** this file. Humans can use the same doc. |
| **[`.github/workflows/claude-pr-review.yml`](.github/workflows/claude-pr-review.yml)** → `prompt:` | CI-only instructions: reminds Claude to read `REVIEW.md`, **condensed checklist**, output format (one PR comment, sections). | Tweak when you want **stronger emphasis** in automation without duplicating all of `REVIEW.md`, or to change **comment structure**. Keep the condensed list roughly aligned with `REVIEW.md`. |
| **`CLAUDE.md`** (optional, not required today) | Project memory for **local** Claude Code / IDE sessions: stack conventions, commands. | Add if you use Claude in the terminal/IDE and want shared rules; see [Anthropic memory docs](https://code.claude.com/docs/en/memory). |
| **Same workflow** → `claude_args:` | e.g. `--model`, `--max-turns`, `--append-system-prompt "..."`. | Cost, length, or a short global nudge; see [GitHub Actions doc](https://code.claude.com/docs/en/github-actions). |

**Practical guidance**

- To change **what** is reviewed (new rules, stricter security, different severity meanings): edit **`REVIEW.md`** first.
- To change **how** the bot behaves in CI only (tone, section headings, “always mention tests”): adjust the **`prompt:`** block in the workflow.
- If `REVIEW.md` and the workflow **disagree**, the workflow tells Claude to follow **`REVIEW.md`**.

---

## Review rules in this repo

- Full text: **[`REVIEW.md`](REVIEW.md)** (Python, Flask, security, tests, dependencies, severity, out-of-scope).
- Workflow mirror: condensed checklist + “read `REVIEW.md`” in [`.github/workflows/claude-pr-review.yml`](.github/workflows/claude-pr-review.yml).
