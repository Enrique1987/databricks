## Exan questions for Databricks Data Engineer Professional
------------------------------------------------------------

**Question 1.  
Tranlsate that code from Python to SQL ?**

**Python**  
```python
from pyspark.sql.window import Window

window = Window.partitionBy("customer_id").orderBy(F.col("row_time").desc())

ranked_df = (customers_df.withColumn("rank", F.rank().over(window))
                          .filter("rank == 1")
                          .drop("rank"))
display(ranked_df)
```

**SQL**
```sql
SELECT newest.*
FROM 
(
    SELECT 
        *,
        RANK() OVER (PARTITION BY customer_id ORDER BY row_time DESC) AS rank
    FROM 
        customer_window
) AS newest
WHERE 
    newest.rank = 1;
```


**Question 2.    
The following code produces an error. Can you determine why ?** 

```python
window = Window.partitionBy("customer_id").orderBy(F.col("row_time").desc())

ranked_df = (spark.readStream
                   .table("bronze")
                   .filter("topic = 'customers'")
                   .select(F.from_json(F.col("value").cast("string"), schema).alias("v"))
                   .select("v.*")
                   .filter(F.col("row_status").isin(["insert", "update"]))
                   .withColumn("rank", F.rank().over(window))
                   .filter("rank == 1")
                   .drop("rank")
             )

display(ranked_df)
```

&nbsp;&nbsp;&nbsp;&nbsp;Stream DataFrames do not support windows functions. The data would need to be processed in micro-Batches.

**Question 3.  
You are creating a Table in Databricks with the following Code, A senior Data Engineer comes to you and let you know that you dont need to initializing "SparkSession" do you know why ?**  

```python
from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.appName("CreateCustomerTable").getOrCreate()

# Create customer table
spark.sql("""
CREATE OR REPLACE TABLE customer_window (
    customer_id INT,
    email STRING,
    first_name STRING,
    last_name STRING,
    gender STRING,
    row_time TIMESTAMP
)
""")
```

&nbsp;&nbsp;&nbsp;&nbsp;In a management environments like Databricks a SparkSession is automatically created for you. When you start a Spark cluster. As
part of this process, Databricks automatically initializates a SparkSession named `spark`. This is why you can directly start running Spark commands using the `spark` object without
explicitly creating a session.  

&nbsp;&nbsp;&nbsp;&nbsp;Databricks simplifies many of the setup and configuration steps for Spark, making it user-friendly. However, if you wre to run your PySpark code outise of such 
management environments, that´s when explicit initialization would be necessary.  

**Question 4  
What does `microBatchDF` and what is it used for ?**  
&nbsp;&nbsp;&nbsp;&nbsp;In structured streaming, certain operations, like window functions, required processing in discrete chunks rather than on a continuous stream. this is achive using micro-batches
`microBatchDF` represents the data of a single micro-batch, allowing stateful operations to be applied efficiently on streamed data.


**Question 5  
As a data architect you are in charge of implementing an Analytics system on the following company that has a specific use case:
Use Case: Updating Customer Profiles in an E-commerce Data Lake Hause**
  
**Background**
An e-commerce company stores detailed profiles of its customers in a data lake house to support various operations such as personalized marketing, customer support, and sales analytics. This data is sourced from multiple touchpoints like user sign-ups,
 order histories, customer support interactions, and browsing behaviors.
 
**Solution**
We will implement a medallion architecture, where we will enrich the user profiles in the silver layer and finally reach the gold layer to apply advanced analysis (ML/BI).

**Quesiton 6  
The data engineers of the above company are wondering whether they should apply CDF to their tables or whether it does not apply in this case.
 What is your decision as a data architect ?**

The table in the scneario described above should be applied to CDFs as they meet the 2 fundamental requiremetns for the use of CDF´s 

- **Tables changes include updates and/or deletes**
	- **Updates:** As customers interact with the platform, their preferences, recent activity, or personal information might change.
	For instance, they might update their delivery address, change their associated phone number, or modify their email subscription preferences.  
	- **Deletes:** Sometimes, customers may choose to delete their accounts or the company might need to remove records for compliance reasons.  

- **Small fraction of records updated in each batch (from CDC feed)**
	- Given the vast number of customers, in each batch (daily/weekly), only a small fraction of the total customer profiles might change. 
	For example, only a small percentage of users might update their information or delete their accounts in any given batch interval.
	- CDC (Change Data Capture) from the operational database can detect and send only these changed records to be processed and updated in the data lake house.
	
**Question 7
Determinate if in the following scneario do we need a CDF:    
"Use Case: Tracking User Activities on an Online News Portal"  
A popular online news portal wants to understand its readers' behaviors better. Every time a user interacts with an article - be 
it reading an article, clicking on an ad, leaving a comment, or sharing an article on social media - an event is generated.**

&nbsp;&nbsp;&nbsp;&nbsp;No.  We should not apply CDF as the Table is a Append-Only Table.

**Why append only?**  
&nbsp;&nbsp;&nbsp;&nbsp;- **Immutable Events** Each user interaction is a unique event with its timestamp. Once an event is generated, it doesnt´change. Instead of updating existing records, new interacions    
&nbsp;&nbsp;&nbsp;&nbsp;- **Scalability** Given the large number of reader and the multitude of interactions they can have on the platform, the system generates a massive volume of events daily. An append only system scales well to handle such high-velocity data.

**Question 8  
The data engineering team wants to build a pipeline that receives customers data as change data capture (CDC) feed from a source system. The CDC events logged at the source 
contain the data of the records along with metadata information. This metadata indicates whether the specified record was inserted, updated, or deleted. 
In addition to a timestamp column identified by the field update_time indicating the order in which the changes happened. 
Each record has a primary key identified by the field customer_id.In the same batch, multiple changes for the same customer could be received with different update_time. 
The team wants to store only the most recent information for each customer in the target Delta Lake table.**

&nbsp;&nbsp;&nbsp;&nbsp;Use MERGE INTO with SEQUENCE BY clause on the update_time for ordering how operations should be applied.

```sql
MERGE INTO target_table AS target
USING source_table AS source
ON target.id = source.id
WHEN MATCHED THEN
    UPDATE SET ...
WHEN NOT MATCHED THEN
    INSERT ...
SEQUENCE BY source.timestamp;
```

**Question 9
Wich statement regarding checkpointing in Spark Structured Streaming is not correct ?**

A)checkpoints stores the current state of a streaming job to cloud storage  
B)checkpoiting allows the streaming engine to track the progress of a stream processing  
C)Checkpoints can be shared between separates streams  


&nbsp;&nbsp;&nbsp;&nbsp;*Solution* Checkpoints can be shared between separates streams.   	

As checkpoints are designed to store the progress and state of a specific streaming query. They should not be shared between multiple streaming quereis. 


**Question 10

What is the trigger configuration of a stream table that need to fetch the data in near real time process without any wait and shold be active continuously making that**

**Solution**  
 
**Available Now (using trigger(availableNow=True))**

- This is a Databricks-specific trigger. When set to True, it will only process the data that's available right now and will not wait for new data.  
- Is very similar to *trigger-once* but can run multiple batches untill all availabe data is consumed, instead of once big batch.  
*Use Case: When you want to clear the existing backlog of data without waiting for new data to arrive.*

```
(spark.table("your_table")
.writeStream
.format("delta")
... # other configurations
.trigger(availableNow=True)
.table("output_table"))
```

**Question 11
A data engineer wants to pass multiple parameters from a Databricks Job to a notebook. They already configured the key and value of each parameter in the configurations of the job.
Which of the following utilities can the data engineer use to read the passed parameters inside the notebook ?**

&nbsp;&nbsp;&nbsp;&nbsp;dbutils.widgets

**Question 12 
Which of the following describes the minimal permissions a data engineer needs to view the metrics, driver logs, and Spark UI of an existing cluster ?**

&nbsp;&nbsp;&nbsp;&nbsp;"Can Attach To" privilege on the cluster.

*Explination*: You can configure two types of cluster permissions:

1- The "Allow cluster creation" entitlement controls your ability to create clusters.   
2- Cluster-level permissions control you ability to use and  modify a specific cluster. There are foru permissions levels for a cluster    

![](img/Cluster-Permissions.PNG)


**Question 13

For production Databricks jobs, which of the following cluster types is recommended to use ?**

&nbsp;&nbsp;&nbsp;&nbsp;Job clusters

*Explination* Job clusters are dedicated clusters for a job or task run. A job cluster auto terminates once the job is completed, which save costs compared to all-purpose clusters.
In addition, Databricks recommends using job clusters in production so that each job rns, in a fully isolate enviroment.

**Question 14 
The data engineering team ahs a Delta Lake table creted with following query:**

```sql
CREATE TABLE target
AS SELECT * FROM source
```

**A Data engineer wants to drop the source table with the following query:**

`DROP TABLE source`

**Which statement describes the result of running this drop command ?**

&nbsp;&nbsp;&nbsp;&nbsp;Only the source table will be dropped, while the target table will not be affected.


**Question 15 Which of the following describes the minimal permissions a data engineer needs to start and terminate and existing cluster?**

&nbsp;&nbsp;&nbsp;&nbsp;"Can Restart" privilege on the cluster

**Question 16 
The data engineering team has a Delta Lake table created with following querey**

```sql
CREATE TABLE customers_clone
LOCATION 'somelocation'
AS SELECT * FROM customers
```

A data engineer wants to drop the table with the following query:

`DROP TABLE customers_clone`

Wich statements describes the result of running this drop command?

&nbsp;&nbsp;&nbsp;&nbsp;Only the table´s metadata will be deleted from the catalog, while the data files will be kept in the storage.

*Explination* External tables are whose dat is stored in an external storage path by using LOCATION clause, when drop table in a external table just the metadata its dropped while the underlying data files are kept.




**Question 17 
Which of the following describes the minimal permissions a data engineer needs to edit the configurations of an existing cluster ?**

&nbsp;&nbsp;&nbsp;&nbsp;"Can Manage" privilege on the cluster

**Question 18
Given the following code block in a notegook**

```python
db_password = dbutils.secret.get(scope="dev", key=""database_password)
print(db_password)

```



