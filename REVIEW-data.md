# Data & API review guidelines

Apply the relevant section(s) based on which file types changed in the PR.

---

## Databases & Migrations

- **Safety:** Migrations must be backwards-compatible — adding a `NOT NULL` column without a default will break existing running instances during deployment. Prefer additive migrations.
- **Irreversibility:** Flag `DROP TABLE`, `DROP COLUMN`, or bulk `DELETE` without a rollback plan.
- **Indexes:** Large table migrations without `CONCURRENTLY` (Postgres) will lock the table; flag for production risk.
- **Transactions:** Migrations that mix DDL and DML without transaction awareness; flag for DB engines where DDL is auto-commit.

---

## API Design (REST / GraphQL / gRPC)

- **Breaking changes:** Removing or renaming fields, changing response types, or tightening validation on existing endpoints is a breaking change — flag it.
- **Auth:** New endpoints must have authentication and authorisation checks; flag endpoints missing `@login_required` or equivalent middleware.
- **Input validation:** All user-supplied inputs validated and sanitised before use. Return `400` for bad input, not `500`.
- **Idempotency:** `POST` endpoints that create resources should document or implement idempotency keys where retries are likely.
