# Code review guidelines (Python / Flask)

These rules guide **automated PR review** (Claude via GitHub Actions) and humans. Edit this file to change what reviewers emphasize.

---

## Always check

- **Correctness:** Logic, edge cases, off-by-one errors, race conditions in shared state, and error paths behave sensibly.
- **Security — secrets:** No API keys, passwords, or tokens committed; use environment variables and config for production `SECRET_KEY` and similar.
- **Security — web / Flask:**
  - **CSRF:** State-changing requests from forms use CSRF protection (`Flask-WTF` / `csrf_token` in templates) where applicable; do not disable CSRF globally without a documented exception.
  - **Sessions / cookies:** Appropriate cookie flags for production (e.g. `Secure`, `HttpOnly`, `SameSite`) when sessions are used.
  - **Injection:** Avoid SQL string concatenation (use parameterized queries / ORM); be careful with `render_template_string` and untrusted input; validate and sanitize redirects and URLs.
  - **Headers / XSS:** Rely on Jinja autoescaping; avoid `|safe` on untrusted data; set security headers where the app serves HTML.
- **Debug / deployment safety:** `DEBUG=True` or insecure defaults must not leak into production configuration paths.
- **Dependencies:** New packages should be justified, version-pinned in `requirements.txt`, and free of known critical issues when practical.
- **Tests:** New or changed behavior should have or update tests under `tests/` when the change is non-trivial.
- **Documentation:** User-visible behavior changes should touch `README.md` or inline docs when appropriate.

---

## Flask structure and patterns

- Prefer an **application factory** (`create_app`) and **blueprints** for routes; avoid a single global `app` with everything registered ad hoc.
- Keep **routes thin**; put orchestration and I/O in **services** or small modules.
- Use **`app.config`** (e.g. `DevelopmentConfig` / `ProductionConfig`) instead of scattered `os.getenv` in route handlers when possible.
- Register extensions (e.g. CSRF) in one place tied to the factory.

---

## Python style and quality

- Prefer **explicit** over clever; use **type hints** on new public functions where it clarifies intent.
- Avoid **bare** `except:`; catch specific exceptions and log or re-raise appropriately.
- Prefer **`logging`** over `print` for application diagnostics in library-style or server code.
- Use **context managers** for files and resources; prefer **`pathlib`** for paths when it simplifies code.
- Avoid mutable **default arguments** (`def f(x=[]):`); use `None` and assign inside the function.
- Keep functions **focused**; extract helpers when a block does multiple things.

---

## Severity rubric (for review comments)

Use these labels in findings:

| Level | Meaning |
|-------|---------|
| **High** | Security flaw, data loss risk, broken auth/session, crash on common path, or incorrect behavior that likely reaches users. |
| **Medium** | Bug in an edge case, missing validation, weak error handling, missing tests for risky code, or maintainability that will slow the team. |
| **Low** | Style, small refactors, optional improvements, minor doc gaps, or suggestions that are not blocking. |

If severity is unclear, state that explicitly next to the finding.

---

## De-prioritize / skip in review

- Pure formatting-only changes when a formatter or linter already enforces style (unless the change hides a real bug).
- Cosmetic CSS nits unless they affect **accessibility**, **layout bugs**, or **security** (e.g. clickable area).
- Bikeshedding names when existing names are already clear and consistent with the file.

---

## Output shape (automated review)

When posting the PR comment, use: **Summary**, **Findings (High / Medium / Low)**, **Suggested follow-ups**, matching the workflow instructions.
