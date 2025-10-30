# 🧩 Databricks — Exam-Style 

## Views

Below are four realistic data-engineering or analytics scenarios.  
Decide **which type of view** you would use in each case —  
then scroll down to see the **answers and reasoning**.

---

## 🔹 Scenario 1 — BI dashboard performance

The analytics team has a Power BI dashboard that queries
`main.demo.sales` every few minutes.  
Each query aggregates millions of rows with `SUM`, `AVG`, and `GROUP BY` operations.  
The underlying data only changes once or twice per day, but the dashboard is slow.

> ❓ Which type of view would you create to improve performance and reduce compute cost?

---

## 🔹 Scenario 2 — Row-Level Security (RLS)

You must expose sales data to regional managers.  
Each manager should see **only their own region’s** sales,  
based on their account group in Unity Catalog.  
The data must always reflect the **latest transactions**.

> ❓ Which type of view allows filtering logic like  
> `WHERE region IN (SELECT region FROM user_region_map WHERE user = current_user())`  
> while remaining always up-to-date?

---

## 🔹 Scenario 3 — Temporary data exploration

A data scientist is experimenting in a notebook and runs a quick transformation:
```python
df_filtered = df.filter("amount > 1000")
df_filtered.createOrReplaceTempView("v_large_sales")
```
They only need to query this view during the current session for testing.

> ❓ What type of view is suitable for this short-lived, session-only exploration?

---

## 🔹 Scenario 4 — Share a quick result across notebooks on the same cluster

Two colleagues are collaborating on the same interactive cluster.  
Notebook A creates an intermediate result set that Notebook B needs to query,  
but both will disconnect after finishing the analysis.  
The view should be visible to both notebooks but not permanent.

> ❓ What view type lets both notebooks access it without writing to the metastore?

---

---

# ✅ Answers & Explanations

### 1️⃣ Scenario 1 → **Materialized View**
- **Why:** Data changes infrequently, queries are heavy, and dashboards run repeatedly.  
  A materialized view stores the aggregated results as Delta files and Databricks refreshes them automatically.  
  → *Fast reads, lower warehouse cost, acceptable eventual consistency.*

---

### 2️⃣ Scenario 2 → **Persistent View**
- **Why:** Requires dynamic filtering (`current_user()`) and always-fresh data.  
  Persistent views store only the SQL definition, so every read re-executes the query on current data.  
  Perfect for **governance** and **row-level security** logic.

---

### 3️⃣ Scenario 3 → **Temporary View**
- **Why:** Used inside one notebook/session, not saved to the metastore.  
  Exists only while the Spark session is active.  
  Ideal for **ad-hoc exploration or debugging.**

---

### 4️⃣ Scenario 4 → **Global Temporary View**
- **Why:** Must be accessible across multiple notebooks on the same cluster.  
  Created with `CREATE GLOBAL TEMP VIEW` and queried as `global_temp.view_name`.  
  Survives until the **cluster stops**.

---

## 🧠 Summary Table

| Scenario | Description | Correct View | Lifetime | Typical Use |
|-----------|--------------|--------------|-----------|--------------|
| 1 | Heavy BI dashboard, rare data changes | **Materialized View** | Permanent | Cached analytics |
| 2 | Row-level security, always current | **Persistent View** | Permanent | Secure semantic layer |
| 3 | One-session exploration | **Temporary View** | Session | Ad-hoc analysis |
| 4 | Share across notebooks, same cluster | **Global Temporary View** | Until cluster ends | Shared exploration |

