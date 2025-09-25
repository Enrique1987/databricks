# Key Concepts 📚

<!-- 
This section collects core concepts we use in our data engineering work. 
Each term is explained at three levels of depth (kid, teenager, tech lead) 
so that everyone in the team — from juniors to seniors — can build a shared understanding. 
-->

## Deterministic vs. Idempotent 🚀

This section explains two important concepts — **deterministic** and **idempotent** — in three levels of depth: like a kid 👶, like a teenager 👦, and like a technical lead 👨‍💻.

---

### 👶 As a 5-year-old

- **Deterministic**: Every time you press the same Lego button, you always get the **same toy** built 🧱.  
- **Idempotent**: When you clean up your toys, the room is clean. If you try to clean it again, nothing changes — it’s **still clean** 🧹.

---

### 👦 As a teenager

- **Deterministic**: Doing the same math equation with the same numbers always gives the **same result** ➕➖.  
- **Idempotent**: On Instagram, pressing the ❤️ once means you liked the post. Pressing it again doesn’t double it — it’s still **just one like** 👍.

---

### 👨‍💻 As a Technical Lead

- **Deterministic**: An operation is deterministic when the same input **always produces the same output**. In data pipelines, rerunning a job with the same source files should give identical results, with no randomness or order issues. ⚙️  
- **Idempotent**: An operation is idempotent when it can be **safely repeated** without changing the final state beyond the first run. In ETL, if we reprocess a file we already ingested, it should **not create duplicates** or corrupt data — the table remains correct. 🗄️

---

### 🎯 Quick cheat sheet

- **Deterministic** = Same input → same output (predictable).  
- **Idempotent** = Repeat the action → same final state (safe to retry).  



## Databricks Asset Bundles (DAB) 📦 — 3-Level Explainer 💡

> **One-liner:** A **Bundle** is a packaged description of your Databricks project so you can **set it up and run it the same way** in dev → test → prod. 🚀

---

### 👶 As a 5-year-old

- You put your toys in a **magic box**.  
- On the box, a picture shows **where each toy goes** and **what to play first**.  
- Wherever you open the box (home, grandma’s, school), your play space looks **the same**.  
- That magic box is a **Bundle**. It tells Databricks what to create and how to start. 🧰

---

### 👦 As a teenager (13)

- Think of a **playlist**: it remembers **which songs**, **what order**, and **the volume** you like.  
- A **Bundle** is a playlist for your **data project**: which jobs to run, which notebooks to start, and when.  
- You can have different **modes**—*practice*, *match*, *tournament*—like **dev / test / prod**.  
- You hit one button (or run one command) and Databricks **sets everything up the same way** every time. 🔁

---

### 👨‍💻 As a Technical Lead

**What it is**  
- **Projects-as-code** for Databricks workspace assets: Jobs, Lakeflow/DLT pipelines, SQL warehouses/queries, permissions, variables, and environment “targets.”  
- Lives alongside your repo; a single definition drives **repeatable, idempotent** deployment and execution across workspaces.

**Purpose**
Deploy same project consistently across enviroments.

**Scope

**Why it matters**  
- **Deterministic & reviewable** changes (PRs, code review, artifact history).  
- **Drift resistance**: declarative updates keep dev/test/prod aligned.  
- **Promotion flow**: same bundle, different targets and overrides.  
- **Onboarding speed**: clone → deploy → run.

**How it works (concise)**  
- Root contains a `databricks.yml` that declares `resources` (jobs/pipelines/etc.) and `targets` (env-specific overrides).  
- Use Databricks CLI: `bundle validate | deploy -t <env> | run <job>`.  
- Reference secrets via scopes/Key Vault; apply permissions in the spec.  
- Complements **Terraform** (infra, networking, UC metastore/workspaces, policies). DAB = app/workspace assets; Terraform = platform.

## Databricks Auto Loader ⚡

### 👶 Kid — New toys bin
- Every day, new toys appear in a big box.
- Instead of emptying the whole box, you only pick up **the new toys** since yesterday.
- If a toy shape you’ve never seen shows up, you learn its shape and keep going.
**Takeaway:** Auto Loader grabs **only the new stuff** and learns new shapes as they appear.

### 🧑‍🎓 Teen — Daily photo dump
- Your friends keep dropping photos into a shared folder.
- You set your phone to **auto-import only the photos you don’t have yet**.
- If someone starts adding **HEIC** instead of **JPG**, your phone adapts and still imports.
**Takeaway:** It’s a smart “import-new-only” that **adapts to changes** without breaking.

### 👨‍💻 Tech Lead — Ingesting cloud files into a lakehouse
- **Scenario:** Partners land files (CSV/JSON/Parquet) into S3/ADLS/GCS. You need **incremental, schema-evolving** ingestion into Bronze/Delta with strong scaling and idempotency.
- **Definition:** Auto Loader is Databricks’ **incremental file source** (`format("cloudFiles")`) for streaming/batch-like ingestion from cloud object storage. It tracks what’s been processed, supports **schema inference/evolution**, and scales directory discovery (or uses cloud notifications) to handle large folders reliably.

- **When to use:**
  - Landing zone ingestion from object storage where files arrive continuously.
  - You need **“exactly-once”-like** ingestion semantics for files and automatic tracking.
  - Schemas evolve over time (new columns/fields) and you want minimal manual ops.
  - You want Bronze → Silver pipelines with **Structured Streaming** or **DLT**.

- **Pros / Cons:**
  - **Pros:** Incremental (no reprocessing), scalable discovery, schema inference & evolution, checkpointing, rescued data column for dirty records, integrates with Delta/Unity Catalog.
  - **Cons:** File-based latency (seconds–minutes, not sub-second), requires cloud IAM/paths & checkpoints, schema evolution beyond additive changes still needs planning, very “wide” directories can still be operationally tricky if poorly partitioned.

