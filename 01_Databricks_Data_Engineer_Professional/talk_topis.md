
## Databricks Concepts – Summary Notes

#### 1. Databricks Cluster

* A **cluster** is the compute engine used to execute workloads.
* It is **not physically inside Databricks**, but deployed on cloud infrastructure (e.g. Azure VMs).
* Databricks acts as an **orchestration and control layer**.
* You configure:

  * VM type
  * Number of nodes
  * Autoscaling
* **Cost model:**

  * Cloud provider → infrastructure (VMs, storage, networking)
  * Databricks → DBUs (Databricks Units for runtime & features)

---

#### 2. Photon

* **Photon** is an optimized execution engine (C++ vectorized engine).
* Works on top of the same cluster infrastructure.
* Improves performance mainly for:

  * Large-scale queries
  * SQL / DataFrame workloads
* **Important limitation:**

  * Cannot be enabled/disabled dynamically.
  * Requires **cluster restart**.

👉 Recommendation:

* Use Photon by default for production workloads unless proven otherwise.

---

#### 3. Databricks Connect:

Coe Idea, is for developers that love his own local IDE and do not want to use the one from Databricks.

* Allows running code from **local IDE (e.g. VS Code, PyCharm)** against a Databricks cluster.
* Execution happens **remotely**, not locally.
* Use cases:

  * Developer productivity
  * Debugging
  * Avoiding notebook-only workflows

👉 Positioning:

* Best for engineers who prefer **code-first workflows over notebooks**.

---

#### 4. Delta Sharing & Sharing Identifier

* **Delta Sharing** enables secure data sharing across:
  * Workspaces
  * Accounts
  * Organizations

* A **sharing identifier** acts like:
  * A **resource locator + access reference**
  * Comparable to an API endpoint identifier

* Authentication is handled via:
  * Tokens / credentials (not just identifier alone)

👉 Key concept:

* Data is **not copied**, it is accessed remotely.

---

#### 5. Auto Loader

### Schema Evolution

When new columns appear in source data:

* Without configuration → pipeline may fail
* With rescue mode:
  * New/unexpected fields go into:

    ```
    _rescued_data
    ```

### Behavior with new columns

* Existing data → `NULL`
* New data → populated values

---

#### 6. Auto Loader Triggers

**Available Trigger Modes**

##### 1. `trigger(once=True)`

* Runs **once**
* Processes all available data
* Then stops

👉 Use case:

* Batch ingestion
* Backfills

---

##### 2. `trigger(availableNow=True)`

* Processes all currently available data
* Stops after completion
* Can be triggered repeatedly

👉 Use case:
* Incremental batch processing
* Scheduled pipelines
---

##### 3. Continuous / Micro-batch (default streaming)

* Runs continuously
* Processes data as it arrives

👉 Use case:

* Near real-time ingestion
---

#### 7. Constraint Handling (`ON VIOLATION`)

##### `ON VIOLATION DROP`

* Keeps the row
* Sets invalid column value → `NULL`

##### `ON VIOLATION DELETE`

* Removes the entire row

👉 Design implication:

* **DROP → data preservation**
* **DELETE → strict data quality**

---

#### 8. Delta Live Tables (DLT)

#### Live Table

* General concept in DLT
* Can read from:

  * Batch sources
  * Streaming sources

#### Live Streaming Table

* Special case of Live Table
* Reads from **streaming source only**

---

### Key Rule

| Table Type           | Input Type Allowed |
| -------------------- | ------------------ |
| Live Table           | Batch or Streaming |
| Live Streaming Table | Streaming only     |

---

### Important Clarification

* A **Live Streaming Table cannot read from batch**
* If it reads batch → it is just a **Live Table**

---

### Design Insight

Even if source is batch:

* You may still use DLT for:

  * Automation
  * Dependency management
  * Data quality enforcement

---

## 9. Streaming vs Live Concepts (Clarification)

* **Streaming** → data ingestion mode
* **Live Table** → managed pipeline abstraction
* **Live Streaming Table** → Live Table + streaming input

👉 Think:

* *Streaming = how data arrives*
* *Live Table = how pipeline is managed*

---

# Practical Takeaways (Consulting View)

## Recommended Defaults

* Use **Photon** for most production workloads
* Use **Auto Loader + schema evolution with rescue**
* Prefer **availableNow** for controlled ingestion
* Use **DLT** when:

  * You need governance
  * You want managed pipelines
  * You need data quality rules

---

## When to Be Careful

* Photon on small datasets → limited benefit
* Streaming when batch is enough → unnecessary complexity
* Overusing DLT → operational overhead if not needed

---

## Architecture Perspective

* Databricks = control plane
* Cloud (Azure/AWS/GCP) = data plane (compute + storage)
* Clusters = ephemeral compute layer
* Delta = storage + transaction layer

