# Get Started with Databricks

These questions are the ones that appear along the learning path during the Databricks training.

**Question 1. Two data engineers are collaborating on one notebook in the same repository. Each is worried that if they work on the notebook at different times, they might overwrite changes that the other has made to the code within the notebook. Which of the following explains why collaborating in Databricks Notebooks prevents these problems from occurring? Select one response.**

- A. Databricks Notebooks supports alerts and audit logs for easy monitoring and troubleshooting, so the data engineers will be alerted when changes are made to their code.
- B. Databricks Notebooks supports real-time co-authoring, so the data engineers can work on the same notebook in real-time while tracking changes with detailed revision history.
- C. Databricks Notebooks are integrated into CI/CD pipelines by default, so the data engineers can work in separate branches without overwriting the other’s work.
- D. Databricks Notebooks automatically handles schema variations to prevent insertion of bad records during ingestion, so the data engineers will be prevented from overwriting data that does not match the table’s schema.
- E. Databricks Notebooks enforces serializable isolation levels, so the data engineers will never see inconsistencies in their data.

**Question 2. Due to the platform administrator’s policies, a data engineer needs to use a single cluster on one very large batch of files for an ETL workload. The workload is automated, and the cluster will only be used by one workload at a time. They are part of an organization that wants them to minimize costs when possible. Which of the following cluster configurations can the team use to satisfy their requirements? Select one response.**

- A. Multi node all-purpose cluster
- B. Single node all-purpose cluster
- C. High concurrency all-purpose cluster
- D. Single node job cluster
- E. Multi node job cluster

**Question 3. A data engineer wants to stop running a cluster without losing the cluster’s configuration. The data engineer is not an administrator. Which of the following actions can the data engineer take to satisfy their requirements and why? Select one response.**

- A. Delete the cluster; clusters are retained for 60 days after they are deleted.
- B. Delete the cluster; clusters are retained for 30 days after they are deleted.
- C. Edit the cluster; clusters can be saved as templates in the cluster configuration page before they are deleted.
- D. Detach the cluster; clusters are retained for 70 days after they are detached from a notebook.
- E. Terminate the cluster; clusters are retained for 30 days after they are terminated.

**Question 4. A data engineer is trying to merge their development branch into the main branch for a data project's repository. Which of the following is a correct argument for why it is advantageous for the data engineering team to use Databricks Repos to manage their notebooks? Select one response.**

- A. Databricks Repos allows integrations with popular tools such as Tableau, Looker, Power BI, and RStudio.
- B. Databricks Repos provides a centralized, immutable history that cannot be manipulated by users.
- C. Databricks Repos REST API enables the integration of data projects into CI/CD pipelines.
- D. Databricks Repos provides access to available data sets and data sources, on-premises or in the cloud.
- E. Databricks Repos uses one common security model to access each individual notebook, or a collection of notebooks, and experiments.

**Question 5. Which of the following cluster configuration options can be customized at the time of cluster creation? Select all that apply.**

- A. Access permissions
- B. Restart policy
- C. Maximum number of worker nodes
- D. Cluster mode
- E. Databricks Runtime Version

**Question 6. Three data engineers are collaborating on a project using a Databricks Repo. They are working on the notebook at separate times of the day. Which of the following is considered best practice for collaborating in this way? Select one response.**

- A. The engineers can set up an alert schedule to notify them when changes have been made to their code.
- B. The engineers can each design, develop, and trigger their own Git automation pipeline.
- C. The engineers can each create their own Databricks Repo for development and merge changes into a main repository for production.
- D. The engineers can use a separate internet-hosting service to develop their code in a single repository before merging their changes into a Databricks Repo.
- E. The engineers can each work in their own branch for development to avoid interfering with each other.

**Question 7. A data engineer is creating a multi-node cluster. Which of the following statements describes how workloads will be distributed across this cluster? Select one response.**

- A. Workloads are distributed across available worker nodes by the executor.
- B. Workloads are distributed across available worker nodes by the driver node.
- C. Workloads are distributed across available memory by the executor.
- D. Workloads are distributed across available driver nodes by the worker node.
- E. Workloads are distributed across available compute resources by the executor.

**Question 8. Which of the following are data objects that can be created in the Databricks Data Science and Engineering workspace? Select two responses.**

- A. Clusters
- B. SQL Warehouses
- C. Tables
- D. Functions
- E. MLflow Models

**Question 9. A data engineer needs to develop an interactive dashboard that displays the results of a query. Which of the following services can they employ to accomplish this? Select one response.**

- A. Delta Live Tables (DLT)
- B. Databricks Machine Learning
- C. Unity Catalog
- D. Databricks SQL
- E. Delta Lake

**Question 10. A data architect is proposing that their organization migrate from a data lake to a data lakehouse. The architect claims that this will improve and simplify the work of the data engineering team. Which of the following describes the key benefits of why migrating from a data lake to a data lakehouse will be beneficial for the data engineering team? Select two responses.**

- A. Data lakehouses are able to support cost-effective scaling.
- B. Data lakehouses are able to support data quality solutions like ACID-compliant transactions.
- C. Data lakehouses are able to support machine learning workloads.
- D. Data lakehouses are able to improve query performance by managing metadata and utilizing advanced data partitioning techniques.
- E. Data lakehouses are able to support programming languages like Python.

**Question 11. Which of the following correctly lists the programming languages that Databricks Notebooks can have set as the default programming language? Select one response.**

- A. Python, R, Scala, SQL
- B. HTML, Python, R, SQL
- C. Java, Pandas, Python, SQL
- D. HTML, Python, R, Scala
- E. Bash script, Python, Scala, SQL

**Question 12. Which of the following resources reside in the control plane of a Databricks deployment? Select two responses.**

- A. Notebook commands
- B. Job scheduler
- C. JDBC and SQL data sources
- D. Databricks File System (DBFS)
- E. Job configurations

**Question 13. A data engineer has a long-running cluster for an ETL workload. Before the next time the workload runs, they need to ensure that the image for the compute resources is up-to-date with the latest image version. Which of the following cluster operations can be used in this situation? Select one response.**

- A. Delete
- B. Start
- C. Terminate
- D. Restart
- E. Edit

**Question 14. A data engineer needs to run some SQL code within a Python notebook. Which of the following will allow them to do this? Select two responses.**

- A. They can wrap the SQL command in spark.sql().
- B. They can run the import sql statement at the beginning of their notebook.
- C. They can use the %sql command at the top of the cell containing SQL code.
- D. They can use the %md command at the top of the cell containing SQL code.
- E. It is not possible to run SQL code from a Python notebook.

**Question 15. Which of the following pieces of information must be configured in the user settings of a workspace to integrate a Git service provider with a Databricks Repo? Select two responses.**

- A. Administrator credentials for Git service provider account
- B. Username for Git service provider account
- C. Personal Access Token
- D. Two-factor authentication code from Git service provider
- E. Workspace Access Token

**Question 16. A data engineer needs the results of a query contained in the third cell of their notebook. It has been verified by another engineer that the query runs correctly. However, when they run the cell individually, they notice an error. Which of the following steps can the data engineer take to ensure the query runs without error? Select two responses.**

- A. The data engineer can choose “Run all above” from the dropdown menu within the cell.
- B. The data engineer can choose “Run all below” from the dropdown menu within the cell.
- C. The data engineer can clear the execution state before re-executing the cell individually.
- D. The data engineer can clear all cell outputs before re-executing the cell individually.
- E. The data engineer can run the notebook cells in order starting from the first command.

**Question 17. A data engineering team is working on a shared repository. Each member of the team has cloned the target repository

 and is working in a separate branch. Which of the following is considered best practice for the team members to commit their changes to the centralized repository? Select one response.**

- A. The data engineers can each commit their changes to the main branch using an automated pipeline after a thorough code review by other members of the team.
- B. The data engineers can each sync their changes with the main branch from the Git terminal, which will automatically commit their changes.
- C. The data engineers can each call the Databricks Repos API to submit the code changes for review before they are merged into the main branch.
- D. The data engineers can each run a job based on their branch in the Production folder of the shared repository so the changes can be merged into the main branch.
- E. The data engineers can each create a pull request to be reviewed by other members of the team before merging the code changes into the main branch.

**Question 18. Which of the following operations are supported by Databricks Repos? Select two responses.**

- A. Pull
- B. Rebase
- C. Clone
- D. Sync
- E. Reset

**Question 19. A data engineer is working on an ETL pipeline. There are several utility methods needed to run the notebook, and they want to break them down into simpler, reusable components. Which of the following approaches accomplishes this? Select one response.**

- A. Create a separate task for the utility commands and make the notebook dependent on the task from the original notebook’s Directed Acyclic Graph (DAG).
- B. Create a separate notebook for the utility commands and use the %run magic command in the original notebook to run the notebook with the utility commands.
- C. Create a pipeline for the utility commands and run the pipeline from within the original notebook using the %md magic command.
- D. Create a separate notebook for the utility commands and use an import statement at the beginning of the original notebook to reference the notebook with the utility commands.
- E. Create a separate job for the utility commands and run the job from within the original notebook using the %cmd magic command.

**Question 20. Which of the following resources reside in the data plane of a Databricks deployment? Select one response.**

- A. Web application
- B. Job scheduler
- C. Databricks File System (DBFS)
- D. Notebooks
- E. Cluster manager

**Question 21. Which of the following statements describes how to clear the execution state of a notebook? Select two responses.**

- A. Use the Clear State option from the Run dropdown menu.
- B. Perform a Clean operation from the terminal.
- C. Detach and reattach the notebook to a cluster.
- D. Perform a Clean operation from the driver logs.
- E. Perform a Clear State operation from the Spark UI.

## Transform Data with PySpark

**Question 22. A data engineer has the following query, where path is a variable that represents the location of a directory. SELECT * FROM csv.`${path}`;**

- A. The query loads the contents of a directory of CSV files from a source table to a target table.
- B. The query streams data from a directory of CSV files into a table.
- C. The query displays the underlying file contents of a directory of CSV files.
- D. The query converts a directory of files into CSV format.
- E. The query displays the metadata of a directory of CSV files.

**Question 23. A data engineer needs to extract the calendar date and time in human readable format from a DataFrame containing the timestamp column user_last_touch_timestamp. Which of the following lines of code correctly fills in the blank by adding the column end_date of type date in human readable format? Select one response.**

- A. .withColumn(date_format("end_date"), user_last_touch_timestamp, "HH:mm:ss")
- B. .withColumn(date_time("end_date"), user_last_touch_timestamp, "MMM d, yyyy")
- C. .withColumn(date_time("end_date"), user_last_touch_timestamp, "HH:mm:ss")
- D. .withColumn("end_date", CAST(user_last_touch_timestamp) as date_format)
- E. .withColumn("end_date", date_format("user_last_touch_timestamp", "MMM d, yyyy"))

**Question 24. A data engineer has a table records with a column email. They want to check if there are null values in the email column. Which of the following approaches accomplishes this? Select one response.**

- A. They can check if there is at least one record where email is null by adding a filter for when email IS NULL to a SELECT statement.
- B. They can check if there is at least one record where email is null using SELECT DISTINCT records.
- C. They can check if there is at least one record where email is null by pivoting the table on null values.
- D. They can check if there is at least one record where email is null by running a regular expression function on email to filter out null values.
- E. They can check if there is at least one record where email is null by creating a data expectation to drop null values.

**Question 25. A data engineer has created a DataFrame exploded_eventsDF created from the table exploded_events defined here: CREATE TABLE events (user_id string, event_name string, item_id string, events struct<coupon:string, event_id:string, event_revenue:double>); They are using the following code with multiple array transformations to return a new DataFrame that shows the unique collection of the columns event_name and items.**

```python
from pyspark.sql.functions import array_distinct, collect_set, flatten

exploded_eventsDF
    .groupby("user_id")
    .agg(collect_set("event_name"),
    _____
```

Which of the following lines of code fills in the blank to create the column event_history as a unique collection of events? Select one response.

- A. flatten(collect_set(explode(events:event_id))).alias("event_history")
- B. flatten(array_distinct(events[event_id])).alias("event_history")
- C. array_distinct(flatten(collect_set("events.event_id"))).alias("event_history")
- D. array_distinct(extract(collect_set(events.event_id))).alias("event_history")
- E. flatten(extract(events.event_id)).alias("event_history")

**Question 26. A data engineer wants to extract lines as raw strings from a text file. Which of the following SQL commands accomplishes this task? Select one response.**

- A. SELECT * FROM `${dbfs:/mnt/datasets}/001.txt` as TEXT;
- B. SELECT * FROM `${dbfs:/mnt/datasets}/001.txt`;
- C. SELECT text(*) FROM `${dbfs:/mnt/datasets}/001.txt`;
- D. SELECT (*) FROM `${dbfs:/mnt/datasets}/001.txt`;
- E. SELECT * FROM text.`${dbfs:/mnt/datasets}/001.txt`;

**Question 27. Which of the following commands returns a new DataFrame from the DataFrame usersDF without duplicates? Select one response**

- A. usersDF.select(*)
- B. usersDF.groupBy(nulls)
- C. usersDF.drop()
- D. usersDF.count().dropna()
- E. usersDF.distinct()

**Question 28. Which of the following lines of code counts null values in the column email from the DataFrame usersDF? Select two responses.**

- A. usersDF.drop()
- B. usersDF.selectExpr("count_if(email IS NULL)")
- C. usersDF.distinct()
- D. usersDF.count().dropna()
- E. usersDF.where(col("email").isNull()).count()

**Question 29. A data engineer has a DataFrame events_df that has been registered against an external JSON file. The nested JSON fields have already been converted into struct types. The data engineer now needs to flatten the struct fields back into individual columns for the field event_type. The events_df DataFrame has the following schema:**

```plaintext
date string
month string
event_type StructType<id string, size int>
```

**Which of the following approaches allows the data engineer to retrieve id within event_type? Select one response.**

- A. They can use . syntax to access id in event_type.
- B. They can use event_type.* to pull out id into its own column.
- C. They can use : syntax to access id in event_type.
- D. They can use from_json() to parse the columns for id.
- E. They can index the DataFrame by id.

**Question 30. A data engineer has a query that directly updates the files underlying the external table emails. Which of the following correctly describes how to retrieve the number of rows in the updated table? Select one response.**

```plaintext
REFRESH TABLE emails;
SELECT COUNT(*) FROM emails AS OF VERSION 1;

REFRESH TABLE emails;
SELECT DISTINCT_COUNT(*) FROM emails AS OF VERSION 1;

REFRESH TABLE emails;
SELECT COUNT(*) FROM emails WHEN UPDATED = TRUE;

REFRESH TABLE emails;
SELECT COUNT(*) FROM emails;

REFRESH TABLE emails;
SELECT DISTINCT_COUNT(*) FROM emails;
```

**Question 31. A data engineer is using the following code block to create and register a function that returns the first letter of the string email. Another data engineer points out that there is a more efficient way to do this. Which of the following identifies how the data engineer can eliminate redundancies in the code? Select one response.**

```python
from pyspark.sql.functions import udf

@udf("string")
def first_letter_function(email: str) -> str:
    return email[0]

first_letter_udf = spark.udf.register("sql_udf", first_letter_function)
```

-

 A. They can eliminate the return statement at the end of the function.
- B. They can eliminate the statement that registers the function.
- C. They can eliminate the parameters in the function declaration.
- D. They can eliminate the import statement in the beginning of the code block.
- E. They can eliminate "sql_udf" from the statement that registers the function.

**Question 32. A data engineer needs to query a JSON file whose location is represented by the variable path. Which of the following commands do they need to use? Select one response.**

- A. SHOW TABLE json.`${path}`;
- B. SELECT * FROM path LOCATION `${path}`;
- C. DISPLAY TABLE json.`${path}`;
- D. RETURN json.`${path}`;
- E. SELECT * FROM json.`${path}`;

**Question 33. A data engineer has a DataFrame with string column email_address. They are using a regular expression that returns a string with a matching pattern when it is in the following format: user.address@domain.com. Which of the following lines of code creates a new column domain that contains the domain from the email_address column? Select one response.**

- A. .withColumn("domain", regexp_extract("email_address", "(?<=@).+", 0))
- B. .withColumn("domain", collect_set("email_address", "(?<=@).+", 0))
- C. .withColumn("domain", flatten("email_address", "(?<=@).+", 0))
- D. .withColumn("domain", array_distinct("email_address", "(?<=@).+", 0))

**Question 34. A data engineer has a table high_temps with the following schema, where avg_high_temp represents the monthly average high temperatures for each unique year-month combination.**

```plaintext
year string
month string
avg_high_temp string
```

**They need to reformat the data with years as the primary record key and months as the columns. The existing average high temperature value for each year-month combination needs to be in the month columns. How can the data engineer accomplish this? Select one response.**

- A. The data engineer can rotate the data from wide to long format using the .pivot() function.
- B. The data engineer can rotate the data from long to wide format using the .transform() clause.
- C. The data engineer can rotate the data from wide to long format using the .transform() clause.
- D. The data engineer can rotate the data from long to wide format using the .pivot() function.
- E. The data engineer can rotate the data from long to wide format using the .groupBy() clause.

**Question 35. A data engineer has a DataFrame events_df that has been registered against an external JSON file. They need to access the field date within events_df. The events_df DataFrame has the following schema:**

```plaintext
date string
month string
event_type string
```

**Which of the following approaches can the data engineer use to accomplish this? Select one response.**

- A. They can index the query by subfield using events[date] syntax.
- B. They can use date.* to pull out the subfields of events_df into their own columns.
- C. They can use . syntax to access date in events_df.
- D. They can use : syntax to access date in events_df.
- E. They can use from_json() to parse the column for date.

**Question 36. Which of the following statements about querying tables defined against external sources is true? Select one response.**

- A. When defining tables or queries against external data sources, the storage path, external location, and storage credential are displayed for users who have been granted USAGE access to the table.
- B. When defining tables or queries against external data sources, the performance guarantees associated with Delta Lake and Lakehouse cannot be guaranteed.
- C. None of these statements about external table behavior are true.
- D. When defining tables or queries against external data sources, older cached versions of the table are automatically deleted.
- E. When defining tables or queries against external data sources, older cached versions of the table are automatically added to the event log.

**Question 37. Which of the following statements about the difference between views and temporary views are correct? Select two responses.**

- A. Temporary views reside in the third layer of Unity Catalog’s three-level namespace. Views lie in the metastore.
- B. Temporary views have names that must be qualified. Views have names that must be unique.
- C. Temporary views do not contain a preserved schema. Views are tied to a system preserved temporary schema global_temp.
- D. Temporary views are session-scoped and dropped when the Spark session ends. Views can be accessed after the session ends.
- E. Temporary views skip persisting the definition in the underlying metastore. Views have metadata that can be accessed in the view’s directory.

**Question 38. A data engineer needs a reference to the results of a query that can be referenced across multiple queries within the scope of the environment session. The data engineer does not want the reference to exist outside of the scope of the environment session. Which of the following approaches accomplishes this without explicitly dropping the data object? Select one response.**

- A. They can store the results of their query within a common table expression (CTE).
- B. They can store the results of their query within a table.
- C. They can store the results of their query within a reusable user-defined function (UDF).
- D. They can store the results of their query within a view.
- E. They can store the results of their query within a temporary view.

**Question 39. A data engineer is using the following query to confirm that each unique string value in the phone_number column in the usersDF DataFrame is associated with at most one user_id. They want the query to return true if each phone_number is associated with at most 1 user_id. When they run the query, they notice that the query is not returning the expected result. Which of the following explains why the query is not returning the expected result? Select one response.**

```python
from pyspark.sql.functions import countDistinct

usersDF
    .groupBy("phone_number")
    .agg(countDistinct("user_id").alias("unique_user_ids"))
```

- A. A .dropDuplicates() statement needs to be added after the .agg() function.
- B. A .merge statement on row_count == count(phone_number) needs to be added after the groupBy() function.
- C. A .select(max("unique_user_ids") <= 1) function needs to be added after the .agg() function.
- D. .groupBy("phone_number") needs to be changed to count(*).when(user_id != null).
- E. .groupBy("phone_number") needs to be changed to .countDistinct(phone_number).

**Question 40. A data engineer is registering a table in Databricks using the table users from an external SQL database. One of their colleagues gives them the following code to register the table. However, when the data engineer runs the code, they notice an error.**

```plaintext
CREATE TABLE users_jdbc
USING JDBC
OPTIONS (
  url = "jdbc:sqlite:${DA.paths.ecommerce_db}"
)
```

**Which of the following correctly identifies why running the code is resulting in an error? Select one response.**

- A. A username and password need to be added to OPTIONS.
- B. The line dbtable = "users" needs to be added to OPTIONS.
- C. USING JDBC needs to be changed to USING SQL.
- D. CREATE TABLE needs to be changed to CREATE JDBC TABLE.
- E. None of these responses correctly identify the cause of the error.

**Question 41. A data engineer has created the following Spark DataFrame sales_df that joins the previously created table sales with the Spark DataFrame items_df when sales and items_df have matching values in the sales_id column in both data objects.**

```python
sales_df = (spark
    .table("sales")
    .withColumn("item", explode("items"))
)
items_df = spark.table("item_lookup")
item_purchasesDF = (sales_df
   ______________________)
```

**Which of the following lines of code correctly fills in the blank? Select one response.**

- A. .innerJoin(items_df, sales_df.sales_id == items_df.sales_id)
- B. .merge(items_df, sales_df, on = "item_id")
- C. .join(items_df, sales_df.sales_id == items_df.sales_id)
- D. .outerJoin(items_df, sales.sales_id == items_df.sales_id)
- E. .join(items_df, sales.sales_id == items_df.sales_id, how = "cross")

**Question 42. A data engineer wants to extract lines as raw strings from a text file. Which of the following SQL commands accomplishes this task? Select one response.**

```plaintext
SELECT text(*) FROM ${dbfs:/mnt/datasets}/001.txt`;
SELECT * FROM `${dbfs:/mnt/datasets}/001.txt` as TEXT;
SELECT (*) FROM ${dbfs:/mnt/datasets}/001.txt`;
SELECT * FROM `${dbfs:/mnt/datasets}/001.txt`;
SELECT * FROM text.`${dbfs:/mnt/datasets}/001.txt`;
```

**Question 43. A data engineer has the following query, where path is a variable that represents the location of a directory.**

```plaintext
SELECT * FROM csv.`${path}`;
```

- A. The query converts a directory of files into CSV format.
- B. The query displays the underlying file contents of a directory of CSV files.
- C. The query displays the metadata of a directory of CSV files.
- D. The query streams data

 from a directory of CSV files into a table.
- E. The query loads the contents of a directory of CSV files from a source table to a target table.

## Solutions

| Question | Solution |
|----------|----------|
| 1        | B        |
| 2        | E        |
| 3        | E        |
| 4        | C        |
| 5        | C, D, E  |
| 6        | E        |
| 7        | B        |
| 8        | C, D     |
| 9        | D        |
| 10       | B, D     |
| 11       | A        |
| 12       | A, B     |
| 13       | D        |
| 14       | A, C     |
| 15       | B, C     |
| 16       | A, E     |
| 17       | E        |
| 18       | A, C     |
| 19       | B        |
| 20       | C        |
| 21       | A, C     |
| 22       | C        |
| 23       | E        |
| 24       | A        |
| 25       | C        |
| 26       | E        |
| 27       | E        |
| 28       | B, E     |
| 29       | A        |
| 30       | D        |
| 31       | B        |
| 32       | E        |
| 33       | A        |
| 34       | D        |
| 35       | D        |
| 36       | B        |
| 37       | D, E     |
| 38       | E        |
| 39       | C        |
| 40       | B        |
| 41       | C        |
| 42       | E        |
| 43       | B        |