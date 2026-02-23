
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

