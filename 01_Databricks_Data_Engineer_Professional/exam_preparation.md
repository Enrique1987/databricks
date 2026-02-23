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
