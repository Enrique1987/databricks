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

📖 **Explanation:**  
👉 [View detailed explanation](./explanation.md)


## Exam-Style Question: Higher-Order Functions on Arrays (Databricks SQL)

### Question

A data engineer is working with a table called `faculties`.
The table contains a column `students` defined as:

```text
ARRAY<STRUCT<student_id STRING, total_courses INT>>
```

Each element in the `students` array represents a student and the number of courses they are enrolled in.

The engineer needs to create a new column that contains **only the students enrolled in fewer than 3 courses**, while preserving the original struct format.

**Which of the following expressions should be used?**

A. `TRANSFORM(students, s -> s.total_courses < 3)`  
B. `FILTER(students, s -> s.total_courses < 3)`  
C. `WHERE s.total_courses < 3`  
D. `AGGREGATE(students, s -> s.total_courses < 3)`  

---

### ✅ Correct Answer

**B. `FILTER(students, s -> s.total_courses < 3)`**

---

## Explanation

### Why B is Correct

`FILTER`:

* Returns a subset of array elements
* Preserves the original element type (`STRUCT`)
* Reduces array size based on condition

This matches the requirement:

> "Only students enrolled in fewer than 3 courses"

---

### Why the Other Options Are Incorrect

| Option | Why It’s Wrong                                                         |
| ------ | ---------------------------------------------------------------------- |
| A      | `TRANSFORM` keeps all elements and returns booleans instead of structs |
| C      | `WHERE` cannot be applied directly inside an array column              |
| D      | `AGGREGATE` reduces an array to a single value                         |

---

## Key Exam Pattern

If the requirement says:

* **Keep only elements** → `FILTER`
* **Modify elements** → `TRANSFORM`
* **Reduce to one value** → `AGGREGATE`
* **Turn into rows** → `EXPLODE`

---

If you'd like, I can also create a slightly harder version of this question at Professional-level difficulty.
