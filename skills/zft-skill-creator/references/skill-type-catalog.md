# Skill Type Catalog

Read this file when classifying a new skill into one of the nine canonical types before generating its structure.

## How to Use This Catalog

Match the user's description to one type. If two types seem equally applicable, pick the one whose structural signals best match the user's primary use case. A skill that straddles types is a design problem — split it or prioritize the dominant behavior.

---

## Type 1: Library & API Reference

**Definition**: Skills that explain how to correctly use a library, CLI, or SDK — especially when Claude tends to get it wrong or uses outdated patterns.

**Examples**: `billing-lib`, `internal-platform-cli`, `frontend-design-system`, `openai-responses-api`

**Structural signals**:
- Heavy `references/` with API docs, gotcha patterns, and code snippets
- Light or no `scripts/`
- Gotchas section lists specific footguns (wrong method names, deprecated parameters)

**Choose this type when** the user's description mentions: "help Claude use", "our internal library", "avoid mistakes with", "correct usage of", "gotchas for", "CLI reference".

---

## Type 2: Product Verification

**Definition**: Skills that describe how to test or verify that code is working, often paired with Playwright, tmux, or similar external tools.

**Examples**: `signup-flow-driver`, `checkout-verifier`, `tmux-cli-driver`, `e2e-smoke-test`

**Structural signals**:
- Strong Commands section with test-runner invocations
- `scripts/` with test driver or assertion scripts
- Gotchas section covers flaky tests, state leakage, TTY requirements

**Choose this type when** the user's description mentions: "test", "verify", "check correctness", "end-to-end", "browser automation", "assertion", "smoke test".

---

## Type 3: Data Fetching & Analysis

**Definition**: Skills that connect to data and monitoring stacks to query, analyze, and summarize operational data.

**Examples**: `funnel-query`, `cohort-compare`, `grafana-dashboards`, `db-query-helper`

**Structural signals**:
- `references/` with datasource IDs, credential paths, table schemas
- `scripts/` with query helper functions (standard library only, credentials from env)
- Gotchas section covers auth, stale data, metric naming inconsistencies

**Choose this type when** the user's description mentions: "fetch data", "query", "dashboard", "metrics", "analysis", "monitoring", "report on".

---

## Type 4: Business Process & Team Automation

**Definition**: Skills that automate repetitive workflows into one command, often depending on other skills or MCPs.

**Examples**: `standup-post`, `create-linear-ticket`, `weekly-recap`, `pr-description-generator`

**Structural signals**:
- Workflow steps map to external system actions (Slack, Linear, GitHub)
- Memory pattern: log file or JSON storing previous executions
- Gotchas section covers API rate limits, auth token expiry, idempotency

**Choose this type when** the user's description mentions: "automate", "post to Slack", "create ticket", "recurring", "standup", "recap", "every week/day".

---

## Type 5: Code Scaffolding & Templates

**Definition**: Skills that generate framework boilerplate for specific functions in a codebase, especially when natural language requirements can't be covered by pure code generation.

**Examples**: `new-service-workflow`, `new-migration`, `create-app`, `api-endpoint-scaffold`

**Structural signals**:
- `references/` with template files and naming conventions
- `scripts/` with a generation script that writes files to disk
- Gotchas section covers naming collisions, template staleness, missing context

**Choose this type when** the user's description mentions: "scaffold", "template", "boilerplate", "generate new", "create a new X", "set up the structure for".

---

## Type 6: Code Quality & Review

**Definition**: Skills that enforce code quality or help review code, potentially running as hooks or in CI.

**Examples**: `adversarial-review`, `code-style-enforcer`, `testing-practices`, `security-audit`

**Structural signals**:
- `references/` with rubrics, checklists, and anti-pattern catalogs
- `scripts/` with linters or static analysis runners
- Gotchas section covers false positives, subjective criteria, review fatigue

**Choose this type when** the user's description mentions: "review", "audit", "quality", "enforce", "lint", "check style", "code standards".

---

## Type 7: CI/CD & Deployment

**Definition**: Skills that help fetch, push, and deploy code, often referencing other skills for data collection.

**Examples**: `babysit-pr`, `deploy-api-service`, `cherry-pick-prod`, `release-cut`

**Structural signals**:
- Hooks section (on-demand hooks for deployment safety)
- `scripts/` with deployment and rollback scripts
- Gotchas section covers destructive actions, rollback triggers, environment confusion

**Choose this type when** the user's description mentions: "deploy", "release", "CI", "CD", "pipeline", "push to prod", "rollback", "merge", "auto-merge".

---

## Type 8: Runbooks

**Definition**: Skills that take a symptom (alert, error, Slack thread) and walk through a multi-tool investigation to produce a structured finding.

**Examples**: `api-service-debugging`, `oncall-runner`, `log-correlator`, `alert-investigator`

**Structural signals**:
- `references/` with symptom-to-tool mapping tables
- `scripts/` with log-fetching and correlation helpers
- Gotchas section covers missing data, misleading symptoms, stale runbook steps

**Choose this type when** the user's description mentions: "debugging", "oncall", "investigate", "alert", "symptom", "find the cause of", "incident".

---

## Type 9: Infrastructure Operations

**Definition**: Skills that perform routine maintenance and operational procedures, often with guardrails for destructive actions.

**Examples**: `resource-orphans`, `dependency-management`, `cost-investigation`, `certificate-rotation`

**Structural signals**:
- Guardrail notes and destructive-action warnings in Gotchas
- `scripts/` with dry-run mode and confirmation prompts
- Workflow steps include soak periods and explicit confirmation gates

**Choose this type when** the user's description mentions: "infrastructure", "cleanup", "orphaned resources", "maintenance", "cost", "certificate", "rotate", "purge".
