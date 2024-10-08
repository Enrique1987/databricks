## Databricks Data Engineer Interview Questions.

These questions are based on my experience as a data engineer over several years in the industry.  They are related to Databricks

#### Question 1
**A new task arrives. A column needs to be changed from `timestamp` to `date`. This is a column that has been in the table for a long time.
It is a created column and the process that creates it is as follows**

`insert_values["valid_from"] = date_sub(current_timestamp(), 1)`

*Answer:*
we need to change 2 things  

- The function that generates this column and modify the code to convert that column to date.
`insert_values["valid_from"] = to_date(date_sub(current_timestamp(), 1))`

- Change the existing data in this column to Date type, otherwise the next time this data is generated,
 an inconsistency will be created, as the incoming data is date type and the existing data is timestap type.
 This only needs to be done once as it would be part of a script that would only be launched once on the system.
  - To finish the process we should simply check that the change has been made correctly.
  - Add a dummy data and check that it has been inserted correctly with the desired data type.
  - Delete the test dummy data.

#### Question 2
**Related with question 1, so how would do change the data type already existing in a table ?**

*Answer*

We can made it in python or SQl, that would be the pseudo-code.

- Select all table you are intereseted, 
- Change data type 
- Overwritte your df with already corrected values in the path where the delta table is.
	
	
```python
# Define the path to the Delta table
delta_table_path = "my_path"

# Step 1: Read the existing Delta table
df = spark.read.format("delta").load(delta_table_path)

# Step 2: Create a temporary view with the date transformations
transformed_df = df.selectExpr("* EXCEPT(valid_from)", "valid_from") \
					withColumn("valid_from", to_date(df["valid_from"]))


# Step 3: Overwrite the existing Delta table with the transformed data
transformed_df.write.format("delta").mode("overwrite").save(delta_table_path)
```

`sql`
  ```sql
-- Step 1: Create a temporary view with the date transformations
CREATE OR REPLACE TEMP VIEW transformed_my_table AS
    SELECT
	* EXCEPT(valid_from), 
	  to_date(valid_from) AS valid_from
	FROM delta.`my_path`;

-- Step 2: Overwrite the existing Delta table with the transformed data
	CREATE OR REPLACE TABLE delta.`my_path` AS
	SELECT * FROM transformed_my_table;
  ```
  
#### Question 3
**You realize that the data in TableA is corrupt, something has happened during development that has corrupted some data and left the table with incorrect values. What would you do ?**

I would use the time travel function to see what has happened and that would give me a view of what processes have been carried out on the table. Once we have taken a look at the table we
can see when modifications were made to the table and in this way restore the stable version that we need.


#### Question 4

**You are the architect of a data lakehouse, a data engineer calls you and tells you that table X has corrupted data, they are trying to revert to an earlier version of
the table but can't find it, they ask you what could have happened.**

There are possible cases taht could explain this.

- The tables have a default retetion perior of 30 days. If the previous stable version of this table was more than 30 days old, the dat is no longer there.  
- If the table that had a steable version is less than 30 dayas old, what could have happend is that a VACUU; has been applied to his table and the retention has been reduced.

#### Quesiton 5
**Can you tell us about your experience in reducing costs on a project?**

I examine the work team and find that there are 4 Data Engineers working on the project.
They have a cluster that seems to be fine, but when I dig a little deeper, I realize that not all the Data Engineers are working on the cluster.
One is more dedicated to the topic of Data Protection and requesting access to the data, another Data Engineer is working on the concept and modeling,
another Data Engineer is in charge of everything related to infrastructure and job orchestration.
Finally, I discover that there is only one engineer who really uses the cluster.
So, I decide to lower the power of the cluster and increase it only if necessary, realizing that starting with such a high power was a mistake.


#### Question 6

**Managed vs External tables, what can you tell me about them, when to use some and when to use others ?** 

- `External Tables` are tables that are mounted on top of a stroage location, and herefore need to use "location" when they are created. 
Need a location outside databricks wherethe data is located. if these tables are deleted the data remain.  

- `Managed Tables` are the ones where teh data is inside databricks, if tables are dopred the dat is deleted.  

In my personal opinion it makes sense to use managed tables in small projects where no external storage is available, i.e. only databricks are available for the project. For large projects like a Data Lakehouse it makes more sense to always have external tables pointing to our data.

#### Question 7
**What is Photon in Databricks ?**

**Photon** is a compute engine from Databricks, get up to 12x faster in vectorials operatinons.

#### Question 8
**What do you mean with Vectorial operations ?**

Vectorial operations are those that can be executed all at once, the operatios i executed on the entire vector array at once. 

check the example of vectorial operations here


#### Question 9, 
**I as you say, Photon is a capacity that can increase the speed of computation, why is it not always activated and why does it appear as an option to be activated ?**  

The activation of Photon also leads to an increase in DBUs consumption and therefore an increase in costs, each team must decide whether the improvement of their process by activating phton 
is worth the increase in costs.

#### Question 10.
**You arrives as a solution architec at a Data Lakehouse your aim is to improive the project, take control of it etc.. One of the task you are concerned with is monioring if any of the pipelines beak in production,
Indee you see that the pipelines all have sucess status, would this be enough to be sure that everything is ok ?**

it is definitelly something really positve but not enought, we have to take a look at the code to see what is being aunched.  

**base on your experience can you tell us more abou it ?**

I arrived to a project where everything was running smoothly but the results sometines in the gold layer were not as expected, when I check the code I reallice that was 
complete encapsulate in try: Exception and therefore all possible errors were avoid without break the pipeline, but still no working propertly, lession learn is that we have to take care abut your try: Exception 
where you put them as they may be covering up a problem that needs to be solved.  

#### Question 11
**What is RLS in Databricks ?**

Its a Data governance feature that allows you to control access to individual rows within your dataset based on the attributes of the user querying the data. This fine-grained access control ensures taht users can only view the data 
they are authorized to see enhancing data privacy and compliance.  


#### Question 12
**A data engineer jnr calls you because 1 hour ago he has joined two life tables and the result table is still loading, hes is not sure if he did it right, you examine the code and oyu see this**

```python
# Read from the first streaming table
stream_df1 = spark.readStream.format("delta").table("bronze_table1")

# Read from the second streaming table
stream_df2 = spark.readStream.format("delta").table("bronze_table2")

# Perform the join without any time constraints
joined_stream = stream_df1.join(
    stream_df2,
    on="key",  # Assuming 'key' is the column to join on
    how="inner"
)

# Write the joined stream to a sink (e.g., a Delta table)
joined_stream.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/path/to/checkpoint/dir") \
    .table("silver_table")
```
That code is not correct: When you join two streaming tables without specifying time-based windowing and watermarking, 
Spark's Structured Streaming doesn't have sufficient information to manage the streaming state efficiently.
This can lead to the query appearing to "load" indefinitely because it's waiting for potential matching records that may arrive in the future.


correct 

```python
from pyspark.sql.functions import expr, col

# Read from the first streaming table
stream_df1 = spark.readStream.format("delta").table("bronze_table1")

# Read from the second streaming table
stream_df2 = spark.readStream.format("delta").table("bronze_table2")

# Ensure both DataFrames have a proper timestamp column
# If not, you may need to parse or add it
# For illustration, let's assume both have a 'timestamp' column of TimestampType

# Apply watermarking to manage state and handle late data
stream_df1_watermarked = stream_df1.withWatermark("timestamp", "10 minutes")
stream_df2_watermarked = stream_df2.withWatermark("timestamp", "10 minutes")

# Perform the join with time constraints
joined_stream = stream_df1_watermarked.join(
    stream_df2_watermarked,
    expr("""
        stream_df1_watermarked.key = stream_df2_watermarked.key AND
        stream_df1_watermarked.timestamp BETWEEN stream_df2_watermarked.timestamp AND stream_df2_watermarked.timestamp + INTERVAL 10 MINUTES
    """),
    "inner"
)

# Write the joined stream to a sink (e.g., a Delta table)
joined_stream.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/path/to/checkpoint/dir") \
    .table("silver_table")
```

Certainly! Here's the table formatted in Markdown:

### **Summary of the Differences**

| **Aspect**                 | **Incorrect Approach**                       | **Corrected Approach**                         |
|----------------------------|----------------------------------------------|------------------------------------------------|
| **Watermarking**           | Not applied                                  | Applied (`withWatermark`)                      |
| **Time-Based Constraints** | Absent                                       | Present (time-based join condition)            |
| **State Accumulation**     | Unbounded (can grow indefinitely)            | Bounded (limited by watermark duration)        |
| **Output Timeliness**      | Delayed or no output                         | Timely output within the defined window        |
| **Resource Usage**         | High memory consumption, potential failure   | Efficient memory usage, stable operation       |


