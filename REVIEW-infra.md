# Infrastructure review guidelines

Apply the relevant section(s) based on which file types changed in the PR.

---

## Terraform / OpenTofu

- **Security:** No hardcoded secrets in `.tf` files; use `var` with sensitive flag or a secrets manager. S3 buckets must have `block_public_acls = true` and `block_public_policy = true` unless explicitly justified. Security groups must not open `0.0.0.0/0` on sensitive ports (22, 3306, 5432, 6379) without a documented exception.
- **State:** Remote state backend must be configured with state locking (e.g. DynamoDB for S3 backend). No `terraform.tfstate` files committed to git.
- **Modules:** Pin module versions (`source = "..." version = "x.y.z"`); avoid `latest` or unpinned references.
- **Blast radius:** Destructive operations (`destroy`, resource replacements) must be clearly intentional. Flag `lifecycle { prevent_destroy = false }` on critical resources.
- **Naming / tagging:** Resources must have `Name` and environment tags; consistent naming convention across the PR.

---

## Docker / Containers

- **Base images:** Use specific version tags (e.g. `python:3.12-slim`), never `latest`. Prefer slim or distroless images to reduce attack surface.
- **Secrets:** No secrets, passwords, or tokens in `ENV` or `ARG` instructions — they are baked into the image layer and visible in history.
- **User:** Containers must not run as `root` unless explicitly required; add `USER nonroot` after setup.
- **Multi-stage builds:** Use multi-stage builds for compiled languages to keep the final image small.
- **Layer efficiency:** `COPY` and `RUN` ordering — copy `requirements.txt`/`package.json` before source code to maximise cache hits.

---

## Kubernetes

- **Security:** No `privileged: true` containers. Set `readOnlyRootFilesystem: true` where possible. Use `securityContext` with `runAsNonRoot: true`. Secrets must use `kind: Secret` or an external secrets operator — never `ConfigMap` for sensitive values.
- **Resource limits:** Every container must have `resources.requests` and `resources.limits` set; missing limits can cause node OOM evictions.
- **Health checks:** `livenessProbe` and `readinessProbe` must be present on all long-running containers.
- **Replicas:** `replicas: 1` on production workloads without a justification is a flag; use PodDisruptionBudget for HA services.
- **Image tags:** Never use `latest` in Kubernetes manifests; pin to a specific image digest or semver tag.

---

## Helm (Charts)

- **Values hygiene:** Sensitive values (passwords, tokens) must not have defaults in `values.yaml` — leave them empty and require explicit override at deploy time. Document required values in `README` or `values.yaml` comments.
- **Image tags:** Never default `image.tag` to `latest` in `values.yaml`; use a pinned semver or digest.
- **Resource limits:** Chart templates must include `resources:` with requests and limits; do not leave them empty by default.
- **RBAC:** If the chart creates `ClusterRole` or `ClusterRoleBinding`, flag the scope — prefer namespaced `Role`/`RoleBinding` unless cluster-wide access is justified.
- **Upgrades:** Templates must be backwards-compatible across minor chart upgrades — flag changes to `selector` labels (immutable in Deployments) or PVC specs (require manual migration).
- **Lint:** Charts must pass `helm lint` without warnings.

---

## Ansible

- **Secrets:** No passwords, tokens, or keys in plaintext in playbooks or `vars/` files — use `ansible-vault` or an external secrets manager. Flag `vars_prompt` used for secrets in unattended CI runs.
- **Idempotency:** Every task must be idempotent — using `shell` or `command` modules without `creates`/`removes` or `changed_when` is a flag. Prefer purpose-built modules (`apt`, `copy`, `template`, `service`) over `shell`.
- **Privilege escalation:** `become: true` should be scoped to the tasks that need it — not set globally on the play unless every task requires root. Document why escalation is needed.
- **Hardcoding:** No hardcoded IPs, hostnames, or environment-specific values in tasks — use inventory variables or `group_vars`/`host_vars`.
- **Tags:** Tasks should have tags for selective execution; untagged tasks in large playbooks become hard to run partially.
- **Handlers:** Use handlers for service restarts — do not restart services unconditionally in tasks. Ensure `notify` is paired with a handler so restarts only happen when changes occur.

---

## CI/CD (GitHub Actions / GitLab CI / Jenkins)

- **Secrets:** No secrets hardcoded in workflow files; use `${{ secrets.NAME }}` or vault references.
- **Permissions:** Workflows should use least-privilege permissions (`permissions:` block); avoid `write-all`.
- **Pinning:** Third-party actions must be pinned to a commit SHA, not a branch or mutable tag (e.g. `uses: actions/checkout@v4` → prefer `uses: actions/checkout@<SHA>`).
- **Script injection:** Avoid `${{ github.event.pull_request.title }}` directly inside `run:` steps — it can be used for script injection. Use environment variables to pass context into scripts.
- **Self-hosted runners:** Flag if a PR modifies workflows that run on self-hosted runners — higher privilege escalation risk.

---

## Cloud (AWS / GCP / Azure)

- **IAM / Permissions:** Avoid `*` actions or `*` resources in IAM policies unless explicitly justified. Use least-privilege roles. Flag service accounts with `roles/owner` or `AdministratorAccess`.
- **Encryption:** Storage resources (S3, GCS, EBS, RDS) should have encryption at rest enabled. Data in transit should use TLS.
- **Logging / Auditing:** CloudTrail, GCP Audit Logs, or Azure Monitor should remain enabled; flag any changes that disable or restrict audit logging.
- **Networking:** Flag open security groups, public subnets for backend services, missing VPC flow logs, or direct internet access to databases.
