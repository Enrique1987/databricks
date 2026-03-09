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

````md
## Question 6

**Question:**  
According to the Databricks Lakehouse architecture, which of the following is located in the customer's cloud account?

**Options:**
- Databricks web application
- Notebooks
- Repos
- Cluster virtual machines
- Workflows

**Correct answer:**  
- Cluster virtual machines

---

## Question 11

**Question:**  
How long is the default retention period of the `VACUUM` command?

**Options:**
- 0 days
- 7 days
- 30 days
- 90 days
- 365 days

**Correct answer:**  
- 7 days

---

## Question 13

**Question:**  
A data engineer wants to create a relational object by pulling data from two tables. The relational object must be used by other data engineers in other sessions on the same cluster only. In order to save on storage costs, the data engineer wants to avoid copying and storing physical data.

Which of the following relational objects should the data engineer create?

**Options:**
- Temporary view
- External table
- Managed table
- Global Temporary view
- View

**Correct answer:**  
- Global Temporary view

---

## Question 20

**Question:**  
Which of the following code blocks can a data engineer use to create a user defined function (UDF)?

**Options:**

```sql
CREATE FUNCTION plus_one(value INTEGER)
RETURN value +1
````

```sql
CREATE UDF plus_one(value INTEGER)
RETURNS INTEGER
RETURN value +1;
```

```sql
CREATE UDF plus_one(value INTEGER)
RETURN value +1;
```

```sql
CREATE FUNCTION plus_one(value INTEGER)
RETURNS INTEGER
RETURN value +1;
```

```sql
CREATE FUNCTION plus_one(value INTEGER)
RETURNS INTEGER
value +1;
```

**Correct answer:**

```sql
CREATE FUNCTION plus_one(value INTEGER)
RETURNS INTEGER
RETURN value +1;
```

---

## Question 23

**Question:**
Given the following command:

```sql
CREATE DATABASE IF NOT EXISTS hr_db;
```

In which of the following locations will the `hr_db` database be located?

**Options:**

* `dbfs:/user/hive/warehouse`
* `dbfs:/user/hive/db_hr`
* `dbfs:/user/hive/databases/db_hr.db`
* `dbfs:/user/hive/databases`
* `dbfs:/user/hive`

**Correct answer:**

* `dbfs:/user/hive/warehouse`

---

## Question 24

**Question:**
Given the following table `faculties`, fill in the blank to get the students enrolled in less than 3 courses from the array column `students`.

```sql
SELECT
    faculty_id,
    students,
    __________ AS few_courses_students
FROM faculties
```

**Options:**

* `TRANSFORM(students, total_courses < 3)`
* `TRANSFORM(students, i -> i.total_courses < 3)`
* `FILTER(students, total_courses < 3)`
* `FILTER(students, i -> i.total_courses < 3)`
* `CASE WHEN students.total_courses < 3 THEN students ELSE NULL END`

**Correct answer:**

* `FILTER(students, i -> i.total_courses < 3)`

---

## Question 28

**Question:**
A data engineer has defined the following data quality constraint in a Delta Live Tables pipeline:

```sql
CONSTRAINT valid_id EXPECT (id IS NOT NULL) __________
```

Fill in the above blank so records violating this constraint will be added to the target table, and reported in metrics.

**Options:**

* `ON VIOLATION ADD ROW`
* `ON VIOLATION FAIL UPDATE`
* `ON VIOLATION SUCCESS UPDATE`
* `ON VIOLATION NULL`
* There is no need to add `ON VIOLATION` clause. By default, records violating the constraint will be kept, and reported as invalid in the event log.

**Correct answer:**

* There is no need to add `ON VIOLATION` clause. By default, records violating the constraint will be kept, and reported as invalid in the event log.

---

## Question 29

**Question:**
The data engineer team has a DLT pipeline that updates all the tables once and then stops. The compute resources of the pipeline continue running to allow for quick testing.

Which of the following best describes the execution modes of this DLT pipeline?

**Options:**

* The DLT pipeline executes in Continuous Pipeline mode under Production mode.
* The DLT pipeline executes in Continuous Pipeline mode under Development mode.
* The DLT pipeline executes in Triggered Pipeline mode under Production mode.
* The DLT pipeline executes in Triggered Pipeline mode under Development mode.
* More information is needed to determine the correct response.

**Correct answer:**

* The DLT pipeline executes in Triggered Pipeline mode under Development mode.

---

## Question 31

**Question:**
Which of the following code blocks can a data engineer use to query the existing streaming table `events`?

**Options:**

```python
spark.readStream("events")
```

```python
spark.read.table("events")
```

```python
spark.readStream.table("events")
```

```python
spark.readStream().table("events")
```

```python
spark.stream.read("events")
```

**Correct answer:**

```python
spark.readStream.table("events")
```

---

## Question 38

**Question:**
Which of the following alert destinations is **not** supported in Databricks SQL?

**Options:**

* Slack
* Webhook
* SMS
* Microsoft Teams
* Email

**Correct answer:**

* SMS

---

## Question 42

**Question:**
The data engineer team has a DLT pipeline that updates all the tables at defined intervals until manually stopped. The compute resources terminate when the pipeline is stopped.

Which of the following best describes the execution modes of this DLT pipeline?

**Options:**

* The DLT pipeline executes in Continuous Pipeline mode under Production mode.
* The DLT pipeline executes in Continuous Pipeline mode under Development mode.
* The DLT pipeline executes in Triggered Pipeline mode under Production mode.
* The DLT pipeline executes in Triggered Pipeline mode under Development mode.
* More information is needed to determine the correct response.

**Correct answer:**

* The DLT pipeline executes in Continuous Pipeline mode under Production mode.

---

## Question

**Question:**
Which part of the Databricks Platform can a data engineer use to grant permissions on tables to users?

**Options:**

* Data Studio
* Cluster event log
* Workflows
* DBFS
* Data Explorer

**Correct answer:**

* Data Explorer



