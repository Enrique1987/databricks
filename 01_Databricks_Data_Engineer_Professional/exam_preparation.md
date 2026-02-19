## Exam-Style Question: Delta Live Tables Change Data Capture (CDC)

### Question

A data engineer is designing a **Delta Live Tables (DLT)** pipeline. The source system generates files containing **change events** (CDC). Each event includes:

* metadata indicating whether a record was **inserted**, **updated**, or **deleted**
* a **timestamp** column that indicates the order of changes

The data engineer needs to **apply these change events** to keep a target table up to date.

**Which of the following commands can the data engineer use to best solve this problem (in Delta Live Tables)?**

A. `COPY INTO`
B. `APPLY CHANGES INTO`
C. `MERGE INTO`
D. `UPDATE`

---

### ✅ Correct Answer

**B. `APPLY CHANGES INTO`**

---

### Why (short, exam-style rationale)

* **`APPLY CHANGES INTO`** is the **DLT-native CDC command** designed to process **inserts/updates/deletes** using:

  * a **sequence column** (e.g., timestamp) for ordering
  * an optional **delete condition**
* `MERGE INTO` can implement CDC in plain Delta, but **DLT best practice for CDC pipelines** is `APPLY CHANGES INTO`.
* `COPY INTO` is for ingestion (copy files into a Delta table), not for applying CDC logic.
* `UPDATE` cannot handle inserts/deletes and is not CDC-oriented.

---

### Minimal DLT Example (for study)

```sql
APPLY CHANGES INTO LIVE.target
FROM STREAM(LIVE.source_cdc)
KEYS (id)
SEQUENCE BY event_ts
APPLY AS DELETE WHEN operation = 'DELETE'
COLUMNS * EXCEPT (operation);
```

**Notes:**

* `KEYS` identifies the primary key
* `SEQUENCE BY` ensures correct ordering
* `APPLY AS DELETE WHEN` handles deletes based on the CDC operation flag
