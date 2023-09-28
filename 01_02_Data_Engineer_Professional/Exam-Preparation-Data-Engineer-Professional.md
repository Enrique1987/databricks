## Exan questions for Databricks Data Engineer Professional
------------------------------------------------------------

Question 1.

**Tranlsate that code from Python to SQL ?**

**Python**  
```
from pyspark.sql.window import Window

window = Window.partitionBy("customer_id").orderBy(F.col("row_time").desc())

ranked_df = (customers_df.withColumn("rank", F.rank().over(window))
                          .filter("rank == 1")
                          .drop("rank"))
display(ranked_df)
```

**SQL**
```
SELECT
    customer_id,
    email,
    first_name,
    last_name,
    gender,
    row_time
FROM 
    (
    SELECT 
        *,
        RANK() OVER (PARTITION BY customer_id ORDER BY row_time DESC) AS rank
    FROM 
        customers
    ) AS RankedCustomers
WHERE 
    rank = 1;

```

Question 2.  
**The following code produces an error. Can you determine why ?** 

```
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
You are creating a Table in Databricks with the following Code**

```
%python
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


**A senior Data Engineer comes to you and let you know that you dont need to initializing "SparkSession" do you know why ?**  
&nbsp;&nbsp;&nbsp;&nbsp;In a management environments like Databricks a SparkSession is automatically created for you. When you start a Spark cluster. As 
paor tof this process, Databricks automatically initializates a SparkSession named `spark`. This is why you can directly start running Spark commands using the `spark` object without
explicitly creating a session.  

&nbsp;&nbsp;&nbsp;&nbsp;Databricks simplifies many of the setup and configuration steps for Spark, making it user-friendly. However, if you wre to run your PySpark code outise of such 
management environments, that´s when explicit initialization would be necessary.  




```
