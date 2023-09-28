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

&nbsp;&nbsp;&nbsp;&nbsp;Stream DataFrames do not support windows functions.

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

The table sin the scneario described above should be applied to CDFs as they meet the 2 fundamental requiremetns for the use of CDF´s 

- **Tables changes include updates and/or deletes**
	- **Updates:** As customers interact with the platform, their preferences, recent activity, or personal information might change.
	For instance, they might update their delivery address, change their associated phone number, or modify their email subscription preferences.  
	- **Deletes:** Sometimes, customers may choose to delete their accounts or the company might need to remove records for compliance reasons.  

