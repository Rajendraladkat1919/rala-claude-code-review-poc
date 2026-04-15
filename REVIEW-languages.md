# Language-specific review guidelines

Apply the relevant section(s) based on which file types changed in the PR.

---

## Python

- **Security:** No SQL string concatenation (use parameterised queries / ORM); avoid `render_template_string` with untrusted input; validate and sanitise redirects.
- **Flask specifics:** Application factory (`create_app`), blueprints for routes, thin routes with logic in services, config via `DevelopmentConfig`/`ProductionConfig`, extensions registered in one place, CSRF on all state-changing forms (`Flask-WTF`), `Secure`/`HttpOnly`/`SameSite` cookie flags for production.
- **Quality:** No bare `except:`; catch specific exceptions. Prefer `logging` over `print`. Use type hints on new public functions. Avoid mutable default arguments (`def f(x=[]):`). Use context managers for files/resources.

---

## JavaScript / TypeScript

- **Security:** No `eval()`, `innerHTML` with untrusted data, or `dangerouslySetInnerHTML` without sanitisation. No hardcoded secrets in frontend code (visible to users). Validate all inputs on the server side — never trust client-side validation alone.
- **Async:** Unhandled promise rejections; missing `await`; no `.catch()` on promises that can fail. Prefer `async/await` over raw `.then()` chains for readability.
- **TypeScript:** Avoid `any` type; use explicit return types on exported functions; no `@ts-ignore` without a comment explaining why.
- **React / frontend:** No missing `key` props in lists; avoid side effects in render; clean up `useEffect` subscriptions. Avoid prop drilling across more than 2 levels — use context or state management.
- **Node.js:** Avoid synchronous `fs` calls in request handlers; use environment variables for config; sanitise inputs before passing to shell commands (`child_process`).
- **Dependencies:** Check `package.json` for unpinned versions (`^` / `~`); flag new `devDependencies` added to `dependencies` by mistake.

---

## Java / Kotlin

- **Security:** No string concatenation in SQL queries (use `PreparedStatement` or ORM); avoid `ObjectInputStream` deserialisation of untrusted data; no hardcoded credentials.
- **Null safety:** Kotlin — use `?.` and `?:` instead of `!!`; flag nullable returns on public APIs without null checks. Java — flag unchecked `null` dereferences on return values from external calls.
- **Concurrency:** Shared mutable state accessed from multiple threads must be synchronised or use thread-safe types (`AtomicXxx`, `ConcurrentHashMap`). Flag `synchronized` blocks that are too broad.
- **Resource management:** Use `try-with-resources` (Java) or `.use {}` (Kotlin) for streams, connections, and files.
- **Spring (if applicable):** Avoid field injection (`@Autowired` on fields); prefer constructor injection. Do not expose internal entities directly via REST responses — use DTOs.

---

## Go

- **Error handling:** Never ignore errors with `_`; always check and propagate or log. Avoid `panic` in library code — return errors instead.
- **Concurrency:** Goroutine leaks — every goroutine must have a clear exit path. Channel operations should be paired with `select`/`context` for cancellation. Use `sync.WaitGroup` or `errgroup` for fan-out.
- **Security:** Avoid `os/exec` with unsanitised user input (shell injection). Use `crypto/rand` not `math/rand` for security-sensitive randomness.
- **Resource management:** Always `defer` close on files, HTTP response bodies (`resp.Body`), and DB rows.
- **Interfaces:** Keep interfaces small (1–3 methods); define them at the point of use, not the point of implementation.

---

## Ruby / Rails

- **Security:** No SQL string building with user input — use ActiveRecord queries or `sanitize_sql`. Avoid `send` or `const_get` with user-supplied strings (arbitrary method/class invocation). Mass assignment — ensure `permit` in strong params is explicit and not `permit!`.
- **Rails specifics:** Thin controllers — move business logic to service objects or models. Avoid callbacks (`before_save`, `after_create`) for non-persistence concerns; they make code hard to test. Use `find_by` instead of `find` when you expect nil (no exception). Scope access with `current_user` — never trust user-supplied IDs without scoping to the current user (e.g. `current_user.orders.find(params[:id])`).
- **Quality:** Avoid `rescue Exception` — catch specific errors. No `puts` in application code — use `Rails.logger`. Prefer `present?` / `blank?` over manual nil and empty checks. Keep methods under 10 lines; extract concerns when a class grows beyond a single responsibility.
- **Dependencies:** `Gemfile` should pin major versions; audit new gems for known CVEs (`bundle audit`).

---

## Rust

- **Memory safety:** Flag uses of `unsafe` blocks — every `unsafe` block must have a comment explaining the invariant being upheld. Avoid raw pointer arithmetic without clear justification.
- **Error handling:** No `.unwrap()` or `.expect()` in library or production code paths — propagate errors with `?` or handle explicitly. `unwrap` is acceptable only in tests or clearly unreachable paths.
- **Concurrency:** Prefer `Arc<Mutex<T>>` or message passing (`mpsc`) for shared state. Flag `Mutex` locks held across `await` points in async code — can deadlock.
- **Performance:** Avoid unnecessary `.clone()` on large data structures; prefer references. Flag allocations inside hot loops (e.g. `Vec` or `String` creation per iteration).
- **Dependencies (`Cargo.toml`):** Pin dependencies to minor versions at minimum; flag `*` version specs. Check for duplicate transitive dependencies of the same crate at different major versions.
