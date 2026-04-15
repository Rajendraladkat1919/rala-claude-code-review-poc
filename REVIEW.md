# Code review guidelines — index

These rules guide **automated PR review** (Claude via GitHub Actions) and humans.

## Policy files

| File | Covers |
|---|---|
| `REVIEW.md` (this file) | Universal checks, severity rubric, output shape |
| `REVIEW-languages.md` | Python, JavaScript/TypeScript, Java/Kotlin, Go, Ruby/Rails, Rust |
| `REVIEW-infra.md` | Terraform, Docker, Kubernetes, Helm, Ansible, CI/CD, Cloud (AWS/GCP/Azure) |
| `REVIEW-data.md` | Databases & Migrations, API Design (REST/GraphQL/gRPC) |

Read all four files before reviewing. Apply only the sections relevant to the files changed in the PR.

---

## Universal checks (apply to every PR regardless of language)

- **Correctness:** Logic, edge cases, off-by-one errors, race conditions in shared state, and error paths behave sensibly.
- **Security — secrets:** No API keys, passwords, tokens, or credentials committed anywhere; use environment variables, secret managers, or CI secrets.
- **Debug / deployment safety:** Debug flags, verbose logging, or insecure defaults must not leak into production configuration paths.
- **Dependencies:** New packages/modules should be justified, version-pinned, and free of known critical CVEs when practical.
- **Tests:** New or changed behavior should have or update tests when the change is non-trivial.
- **Documentation:** User-visible or API-visible behavior changes should touch `README.md` or inline docs when appropriate.

---

## Severity rubric (for review comments)

| Level | Meaning |
|-------|---------|
| **High** | Security flaw, data loss risk, broken auth/session, crash on common path, infrastructure misconfiguration exposing data, or incorrect behavior that likely reaches users. |
| **Medium** | Bug in an edge case, missing validation, weak error handling, missing tests for risky code, non-backwards-compatible migration, or maintainability that will slow the team. |
| **Low** | Style, small refactors, optional improvements, minor doc gaps, or suggestions that are not blocking. |

If severity is unclear, state that explicitly next to the finding.

---

## De-prioritize / skip in review

- Pure formatting-only changes when a formatter or linter already enforces style (unless the change hides a real bug).
- Cosmetic CSS nits unless they affect **accessibility**, **layout bugs**, or **security** (e.g. clickable area).
- Bikeshedding names when existing names are already clear and consistent with the file.
- Lock file changes (`package-lock.json`, `poetry.lock`, `go.sum`) — only flag if the diff shows a suspicious new package or a major version bump on a sensitive dependency.

---

## Output shape (automated review)

When posting the PR comment, use: **Summary**, **Findings (High / Medium / Low)**, **Suggested follow-ups**, matching the workflow instructions.
