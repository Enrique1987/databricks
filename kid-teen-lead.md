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


### Databricks Metastore 🗂️

#### 👶 Kid — Toy labels in one big house

* Imagine all the toys in the house have labels.
* The label says what the toy is called and who is allowed to play with it.
* The metastore is the big label book that keeps those rules.
  **Takeaway:** A metastore is the place that remembers what data exists and who can use it.

#### 🧑‍🎓 Teen — Shared playlist rules

* Think of a music app where lots of people use shared playlists.
* The metastore is like the system that says which playlists exist and who can view, edit, or share them.
* It is not the song itself — it is the record and the access rules around it.
  **Takeaway:** The metastore is the control center for data names and permissions.

#### 👨‍💻 Tech Lead — Central governance across teams

* In Unity Catalog, the metastore is the top-level metadata container.
* It stores metadata for securable objects and the permissions that govern access to them.
* It exposes the 3-level namespace: catalog.schema.table.
* A workspace must be attached to a Unity Catalog metastore to use Unity Catalog.
* Databricks recommends one metastore per region for the workspaces in that region.
* **Definition:** A Unity Catalog metastore is the account-level governance boundary for metadata, privileges, and organization of data/AI assets.
* **When to use:**

  * When multiple teams or workspaces need centralized governance.
  * When you want shared catalogs, consistent permissions, lineage, and auditing.
  * When you want to separate governance by region.
* **Pros / Cons:**

  * Pros: central access control, shared catalogs across workspaces, lineage, auditability.
  * Cons: adds governance design decisions up front; migration from legacy Hive metastore can take planning.
    **Takeaway:** Metastore = the governance brain, not the place where users do daily work.

### 🎯 Cheat sheet

* Holds metadata, not the actual data files.
* Controls permissions for Unity Catalog objects.
* Owns the catalog.schema.table namespace.
* Usually shared by multiple workspaces in the same region.
* Think: governance layer.

---

## Databricks Workspace 🏢

### 👶 Kid — Your own room in the house

* A workspace is like your room where you draw, play, and keep your school stuff.
* You do your work there.
* But the house rule book can still decide what you are allowed to use.
  **Takeaway:** A workspace is where people work every day.

### 🧑‍🎓 Teen — Your school app account

* A workspace is like your school app area where you open notes, do homework, and work with classmates.
* It is the place where you actually use tools.
* But the school admin system can still control what files and folders you are allowed to access.
  **Takeaway:** Workspace = your working environment; metastore = the rules behind shared data.

### 👨‍💻 Tech Lead — Team environment for assets and compute

* A Databricks workspace is a Databricks deployment in your cloud account for a defined set of users.
* It is where teams interact with notebooks, files, jobs, dashboards, experiments, and compute.
* Workspaces are often separated by environment or team, such as dev, staging, and prod.
* A workspace can be attached to a Unity Catalog metastore so users in that workspace can access governed catalogs.
* **Definition:** A workspace is the execution and collaboration boundary where users build, run, and manage Databricks assets.
* **When to use:**

  * To isolate teams or environments.
  * To manage workspace-level settings, admins, compute, and collaboration assets.
  * To give users a place to run pipelines, notebooks, and analytics.
* **Pros / Cons:**

  * Pros: operational isolation, team autonomy, environment separation, simpler workspace admin model.
  * Cons: too many workspaces can create operational sprawl; governance becomes fragmented without shared metastore strategy.
    **Takeaway:** Workspace = where work happens; metastore = what makes shared governance consistent.

### 🎯 Cheat sheet

* A workspace is a user-facing Databricks environment.
* It contains notebooks, jobs, files, dashboards, and access to compute.
* Teams often split workspaces by dev/staging/prod or business unit.
* A workspace can be connected to a metastore for centralized governance.
* Think: working environment.

---

## Metastore vs Workspace 🔀

### 👶 Kid — House rules vs your room

* The metastore is the house rule book.
* The workspace is your room where you play.
  **Takeaway:** One tells the rules; one is where you do things.

### 🧑‍🎓 Teen — Platform rules vs your app space

* The metastore is the app admin panel.
* The workspace is your personal/team area inside the app.
  **Takeaway:** Metastore decides access; workspace is where you use the data.

### 👨‍💻 Tech Lead — Governance boundary vs execution boundary

* Metastore = shared metadata and authorization layer.
* Workspace = collaboration and execution layer.
* One metastore can govern multiple workspaces in the same region.
* Users work in a workspace, but access governed assets through the attached metastore.
* Legacy setups often had per-workspace Hive metastores; Unity Catalog shifts governance toward a central metastore model.
* **Definition:** Metastore and workspace solve different layers of the platform: governance vs operations.
* **When to use:**

  * Central metastore when you want common governance.
  * Multiple workspaces when you want operational isolation.
* **Pros / Cons:**

  * Pros: strong separation of concerns.
  * Cons: confusion happens when teams think a workspace owns governance. Usually, the metastore does.
    **Takeaway:** Use workspaces to separate teams/environments; use the metastore to keep governance consistent.

### 🎯 Cheat sheet

* Metastore = metadata + permissions.
* Workspace = users + tools + compute.
* One metastore can serve many workspaces.
* Workspaces are for doing; metastores are for governing.
* Best mental model: control tower vs office floor.

---

## Rule of thumb 📌

* **Metastore = central rulebook for data and permissions.**
* **Workspace = place where engineers, analysts, and scientists actually work.**
* If you ask “where is access controlled?” → metastore.
* If you ask “where do people run notebooks and jobs?” → workspace.
