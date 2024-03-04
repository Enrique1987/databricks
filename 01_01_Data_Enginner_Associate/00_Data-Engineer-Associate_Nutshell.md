# Data Engineer Associate in a Nutshell

## Your 8-20 you should know.

### ETL with SparkSQL and PySpark

You should know: `Querying Files`, `Writing to Tables`, `Advanced Transformations`, `Higher Oder Functions` and  `SQL UDF`


`Higher Oder Functions`:advanced analytical functions that allow you to manipulate complex data types like arrays and maps more efficiently. They enable operations such as transforming array elements or filtering map entries, enhancing data processing capabilities within Databricks notebooks or clusters.  
`SQL UDF`:is a custom function created by users to extend the capabilities of Databricks' SQL language, allowing for custom processing and transformations of data. These functions can be written in languages like Python or Scala and are integrated into Spark SQL queries for use in data analysis and manipulation tasks within Databricks environments.  


**Workflow orchestration patterns.**

- **Fan-out Pattern:**A single task or job is followed by multiple tasks that can be executed in parallel  
- **Funnel Pattern**Multiple task or jobs that run in parallel are followed by a single tas that stgart afther all parallel task completed  
- **Hourglas Pattern**Combine Fan-out and Funnel
- **Sequence Pattern**Task or jobs are organized in a sgtrict sequence, where each task starts only after the previous one has completed.
- **Multi-sequence Pattern**Multi sequences of task that can run in parallel with each other.
