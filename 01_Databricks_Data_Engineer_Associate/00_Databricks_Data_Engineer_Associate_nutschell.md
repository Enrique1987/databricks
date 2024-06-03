# Data Engineer Associate in a Nutshell

## Your 8-20 You Should Know

### 

### ETL with SparkSQL and PySpark

You should know: `Querying Files`, `Writing to Tables`, `Advanced Transformations`, `Higher Order Functions`, and `SQL UDF`.

- **Higher Order Functions**: Advanced analytical functions that allow you to manipulate complex data types like arrays and maps more efficiently. They enable operations such as transforming array elements or filtering map entries, enhancing data processing capabilities within Databricks notebooks or clusters.
  
- **SQL UDF**: A custom function created by users to extend the capabilities of Databricks' SQL language, allowing for custom processing and transformations of data. These functions can be written in languages like Python or Scala and are integrated into Spark SQL queries for use in data analysis and manipulation tasks within Databricks environments.

**Workflow Orchestration Patterns**

- **Fan-out Pattern**: A single task or job is followed by multiple tasks that can be executed in parallel.
- **Funnel Pattern**: Multiple tasks or jobs that run in parallel are followed by a single task that starts after all parallel tasks are completed.
- **Hourglass Pattern**: Combines Fan-out and Funnel patterns.
- **Sequence Pattern**: Tasks or jobs are organized in a strict sequence, where each task starts only after the previous one has completed.
- **Multi-sequence Pattern**: Multiple sequences of tasks that can run in parallel with each other.