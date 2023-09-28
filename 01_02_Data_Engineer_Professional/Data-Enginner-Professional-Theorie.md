# Databricks Data Engineer Professional

Here we have the two learning path I followed for the Professional the Udemy and the Databricks curseware.

## Databricks 

### Architeching for the Lakehouse

**Data Lakehouse**  

`Data Lakes:`  Is a centralized repository designed to store, process, and secure large amounts of structured, semistructured, and unstructured data. They 
are good for Machine Learning and Big Data but are lacking in BI and face challenges in the Data Governance.  

on the oder side.

`Data Wharehouse` Is a centralized repository for storing large volumens of data from multiple sources. It is designed for query and analysis, often used for business Intelligence activities.


**Streaming Design Patterns**  

	

### Bronze Ingestions Patterns

**Bronze Layer**   
- Replaces the raditional data lake.  
- Represents the full, unprocessed hisotry of the data.  
- Captures the provenance(what,when and from where) of data loaded intoe the lakehouse.  
- Data is stored efficiently using Delta Lakehouse.  
- If downstream layers discover later they need to ingest more, they can come back to the Bronze source to obtain it.  

**Bronze Layer Principles**  
- The goal is data capture and provenance: Capture exactly what is ingested, without parsing or change.
- Typically a Delta Lake table with these fields in each row:
	- Date received/ingested  
	- Data source (filename,external system etc)  
	- Text field with raw unparsed JSON, CSV or other data  
	- Other metadata  
- Should be append only(batch or streaming)  
- Plan ahead if data must be deleted for regulatory purposes  
	- Retain all records when possible  
	- Soft-deletes if necessary  
	- Hard-deletes may be required by regulatory processes.  

**Bronze Inmgestion Patterns**  
- **Singleplex Ingestion**: Every Raw data to a Delta Lake, usually works well fro Batch processing.     
- **Mutiplex Ingestion**: For nearly real-time data ingestion, normaly from a pop up system.  
	- Do not use the pop up system as bronze leyer as they are not real tables and have limited time of retention. Normally every topic will be later split in tables, but at first from the Stream system to Data Lakehause are all together in one table.
  
  
    
	
![](img/Bronze_Patterns.PNG)	

**Auto Load to Multiplex Bronze**  

The initialization script has loaded a **`date_lookup`** table. This table has a number of pre-computed date values.
 Note that additional fields indicating holidays or financial quarters might often be added to this table for later data enrichment
 
*Note: I dont know why Databricks consider to make the join with the lookup table from raw to bronze and not later from Bronze to Silver..bronze should be just to store data from data sources*  

```
query = (spark.readStream
              .format(cloudFiles) # that configure the Auto Loader
              .option("cloudFiles.format", "json") # configure Auto Loader to use the JSON format
              .option("cloudFiles.schemaLocation", f"{DA.paths.checkpoints}/bronze_schema")
              .load(DA.paths.source_daily)
              .join(F.broadcast(date_lookup_df), F.to_date((F.col("timestamp")/1000).cast("timestamp")) == F.col("date"), "left") # Perform a broadast join with the date_lookup table
              .writeStream
              .option("checkpointLocation", f"{DA.paths.checkpoints}/bronze")
              .partitionBy("topic", "week_part") # Partition by topic and week part
              .trigger(availableNow=True)
              .table("bronze"))
```

**.broadcast**  
In the context of ApacheSpark is related to optimizing join operations. In Spark, when you join two Data frames, the engine tries to distribute the join operation 
across multiple nodes in the cluster. Howerver for cetain types of joins **where one DataFrame is much smaller than the other** shuffling data across the network 
can be expensive and  time consuming.
The function **F.broadcast** is a hint to Spark taht the given dataframe (date_lookpu_df) is samll enough that it should be sent to all worker nodes in the cluster. This way
 each node has a fully copy of the smaller DataFrame in memory and can perform the join locally without any network shuffling. This can significantly speed up the join operation.
 
**Streaming vs Auto Load**  
Streaming is a method of processing data in real-time as it's generated, without waiting for batch intervals. Auto-load, especially in the context
 of cloud data platforms like Databricks, refers to the automatic detection and ingestion of new data into the system, often combined with both batch
 and streaming processing methods.  
 
**Streaming from Multiplex Bronze**    

We going to proceed with stream read agains a bronze table, the bronze table recive data from kafka.  
- When are just interested in the topic 'bpm'
```
from pyspark.sql import functions as F

json_schema = "device_id LONG, time TIMESTAMP, heartrate DOUBLE"

(spark
   .readStream.table("bronze")
   .filter("topic = 'bpm'")
   .select(F.from_json(F.col("value").cast("string"), json_schema).alias("v"))
   .select("v.*") # select all sufields of previous column
   .writeStream
       .option("checkpointLocation", f"{DA.paths.checkpoints}/heart_rate")
       .option("path", f"{DA.paths.user_db}/heart_rate_silver.delta")
       .trigger(availableNow=True)
       .table("heart_rate_silver"))

query.awaitTermination()
```




### Promoting to Silver

**Silver Layer**   
- Easier to query than the non-curated Bronzed   
	- Data is clean  
	- Transactions have ACID guarantees  
- Represent the "Enterprise Data Model"  
- Captures the full history of business action modeled  
	- Each record processes is preserved  
	- All records can be efficiently queried  
- Reduces data stroage complexity, latency and redundancy  
	- Built for both ETL throughput AND analytic query performance.  
	
- Silver Layer guiding Principles  

	- Uses Delta Lake tables(with SQL table names)  
	- Preserves grain of original data(no aggregation)  
	- Eliminate duplicate records   
	- Production schema enforced   
	- Data quality checks passed  
	- Corrupt data guarantine   
	- Data stored to support production workloads  
	- Optimized for long-term retention and ad-hoch queries  
	
**Promotion Bronze to Silver**  

- Schema enforcement  
	- Prevents bad records from entering table   
	- Mismatch in Type or field name.  
- Schema evolution   
	- Allows new fields to be added  
	- Useful when schema changes in production/new fields added to nested data   
	- All previous records will show newly added as Null   
		- For previously written records, the underlying file isn´t modified.   
		- The additional field is simply defined in the metadata and dynamically read as null.   


**Streaming Deduplication**

How to eliminte duplicate records while working with Structure Streaming and Delta Lake.  
While Spark Structure Streaming provides exactly-once preocessing guaranteees, many source system will introduce duplicate records

**Quality Enforcemnt**

**Promotion to Silver**

**Slowly Changing Dimensions**


**Type 2 SCD**

**Streaming Joins and Statefulness**

**Stream Static Join**



### Gold Query Layer

**Gold Layer**
- Powers ML applications, reporting, dashboards, ad hoch analytics
- Reduces costs associated with ad hoch queries on silver tables
- Allow fine grained permissions
- Reduces strain on production systems  
- Shifts query updates to production workloads

**Lakehouse and the Query Layer**

**Stored Views**

**Materialized Gold Tables**


### Storing Data Securely


**PII & REgulatory Compliance**

**PII Lookup Table**

**Storing PII Securely**

**Managing ACLs**

**Deidentified PII Access**


### Propagating Updated and Deletes

**Change Data Feed**

**Processing Records from Change Data Feed**


**Propagating Deletes with CDF**

**Deleting at PArtitions Boundaries**



### Orchestration and Scheduling

**Orchestration and Scheduling with Multi-Task Jobs**

**Multi-Task Jobs**

**Promoting Code with Repos**

**CLI**

**REST API**

**Deploying Batch and Streaming Workloads**






## Udemy

## Modeling Data Management Solutions.  

![](img/Data_Management_Solutions.PNG)


#### Multiplex Bronze Code

```python
from pyspark.sql import functions as F

def process_bronze():
  
    schema = "key BINARY, value BINARY, topic STRING, partition LONG, offset LONG, timestamp LONG"

    query = (spark.readStream
                        .format("cloudFiles")
                        .option("cloudFiles.format", "json")
                        .schema(schema)
                        .load(f"{dataset_bookstore}/kafka-raw")
                        .withColumn("timestamp", (F.col("timestamp")/1000).cast("timestamp"))  
                        .withColumn("year_month", F.date_format("timestamp", "yyyy-MM"))
                  .writeStream
                      .option("checkpointLocation", "dbfs:/mnt/demo_pro/checkpoints/bronze")
                      .option("mergeSchema", True) # If the dataset changes and there is a new column is added there is not problem (schema evolution)
                      .partitionBy("topic", "year_month")
                      .trigger(availableNow=True) # All data will processed in multiple micro batching untill not more data ise available.
                      .table("bronze"))

    query.awaitTermination()
```

### Streaming from Multiplex Bronze (code)  

  
```python
(spark.readStream
      .table("bronze")
      .createOrReplaceTempView("bronze_tmp"))
```



```sql
CREATE OR REPLACE TEMPORARY VIEW orders_silver_tmp AS
  SELECT v.*
  FROM (
    SELECT from_json(cast(value AS STRING), "order_id STRING, order_timestamp Timestamp, customer_id STRING, quantity BIGINT, total BIGINT, books ARRAY<STRUCT<book_id STRING, quantity BIGINT, subtotal BIGINT>>") v
    FROM bronze_tmp
    WHERE topic = "orders")
```


  
```python
query = (spark.table("orders_silver_tmp")
               .writeStream
               .option("checkpointLocation", "dbfs:/mnt/demo_pro/checkpoints/orders_silver")
               .trigger(availableNow=True)
               .table("orders_silver"))

query.awaitTermination()
```  

Fully in Python


```python
from pyspark.sql import functions as F

json_schema = "order_id STRING, order_timestamp Timestamp, customer_id STRING, quantity BIGINT, total BIGINT, books ARRAY<STRUCT<book_id STRING, quantity BIGINT, subtotal BIGINT>>"

query = (spark.readStream.table("bronze")
        .filter("topic = 'orders'")
        .select(F.from_json(F.col("value").cast("string"), json_schema).alias("v"))
        .select("v.*")
     .writeStream
        .option("checkpointLocation", "dbfs:/mnt/demo_pro/checkpoints/orders_silver")
        .trigger(availableNow=True)
        .table("orders_silver"))

query.awaitTermination() # Its used to keep the streaming job alivem, allowing it to coninuosly process icoming data.
```

### Quality Enforcement (code)


Check contrains will be appear under Table Properties when we run the code `DESCRIBE EXTENDED my_table`

Thanks to ACID in this case, the "A" standos for Atomicity. This means that a transaciton will either fully succeed or it will fail; its not possible for only a part of it to suceed".


`ALTER TABLE orders_silver ADD CONSTRAINT timestamp_within_range CHECK (order_timestamp >= '2020-01-01');`    
drop the Constraint  
`ALTER TABLE orders_silver DROP CONSTRAINT timestamp_within_range;`  


### Streaming Deduplication (code)

*Watermark*
A watermark is a moving threshold in time, which helps Spark to keep track of the progress of the stream. By definig a watermark, you are essentially telling Spark
Structure Streaming how long you´re willingo to wait for out of oder or late data.

Watermark determines how late(in terms of system processing time) and event can arrive and still be included in its respective window. Watermark its directly attached to the 
concern of latency. I we were somehow 100% certain that:  

- Data always arrives in order and There is no latency, meaning that events are processed nstantly or within thei respective windows the we wouldn´t need to use a watermark.
Every event would be processend in its correct time window, and there would be no need to provide a buffer for late-arriving data.

Example.
**Use Case**  
In a streaming system where I m trying to compute hourly sales.

**Problem**  
Due to the fact aht the shops are located in different geogfraphical location aroun the world they sometimes take time to arrive, so how could I process the sales having a window latency of 10 minutes`?

**Solution**  

- By using `watermark`  we can indicate to our system to compute by ranks in that case we can use a watermark of 10 minutes

**2 Problem**  

I have set a watermark of 10 minutes to account for pssible latencies. If I m aggregating sales for two time windows says 
2-3pm and 3-4pm and a order comes in at 3:07 the watermark ensures that this lates orger gest accounted for in the 2-3 pm window, 
provide the actual order timesteamp indicates it was mede within that our

Howerver, how does the system differentiate between an order that genuinely took place at 3:07 pm and an order that was made earlier but only processed at 3:07 due to system latencies?
How does the system ensure that each order is placed in the correct aggregation window based on its actual timestam and not the processing time?

**Solution 2**

When we are processing streaming data, each event typically has a timestam associate with it. This timestamp, which in our example is `order_timestamp`, represent when the order was actually made.
This is different from the processing time.  

In our example:  
- An order made at 2:57 but arriving at 3:07 hast an `order_timestamp` of 2:57 pm. The system processing time is 3:07  
- An order actually made at 3:07 has an `oder_timestamp` of 3:07  

The watermark works with the oder_timestamp no the system processing time.


**Other use of watermark**

```python
deduped_df = (spark.readStream
                   .table("bronze")
                   .filter("topic = 'orders'")
                   .select(F.from_json(F.col("value").cast("string"), json_schema).alias("v"))
                   .select("v.*")
                   .withWatermark("order_timestamp", "30 seconds")
                   .dropDuplicates(["order_id", "order_timestamp"]))
				   
```

In that case will just wait 30 seg to drop the duplicates if a duplicate row come 35 delate will be inserted.	That is the difference between streaming and batch procesing mean in batch processing we could process all our data
in streaming the data its continuosly comming and therefore we must set a range of time for our operations(range of latency)	
		 

When using `dropDuplicates()` in conjuntion with `watermarks`, it ensures that the system will deduplicate records based on the provided columns,
but only within the bound of the watermark. After the watermak has passed a certain timestamp, Spark won´t deduplicate old data with that timestamp.



```python
def upsert_data(microBatchDF, batch):
    microBatchDF.createOrReplaceTempView("orders_microbatch")
    
    sql_query = """
      MERGE INTO orders_silver a
      USING orders_microbatch b
      ON a.order_id=b.order_id AND a.order_timestamp=b.order_timestamp
      WHEN NOT MATCHED THEN INSERT *
    """
    
    microBatchDF.sparkSession.sql(sql_query)
```



```python
query = (deduped_df.writeStream
                   .foreachBatch(upsert_data)
                   .option("checkpointLocation", "dbfs:/mnt/demo_pro/checkpoints/orders_silver")
                   .trigger(availableNow=True)
                   .start())
```


### Slowly Changing Dimensions 

- **Type 0**: The type 0 dimensions attributes never change.7  
- **Type 1**: Overwrite old with new data and therefore does not track historical data.  
- **Type 2**: Add a new row, tracks historical data by creating amultiple records for a given natural key. We could add "effective date" columns.  

| Supplier_Key | Supplier_Code | Supplier_Name  | Supplier_State | Start_Date           | End_Date             |
|--------------|---------------|----------------|----------------|----------------------|----------------------|
| 123          | ABC           | Acme Supply Co | CA             | 2000-01-01T00:00:00  | 2004-12-22T00:00:00  |
| 124          | ABC           | Acme Supply Co | IL             | 2004-12-22T00:00:00  | NULL                 |


Another method from SCD2 uses an effective date and current flag.

| Supplier_Key | Supplier_Code | Supplier_Name  | Supplier_State | Effective_Date       | Current_Flag |
|--------------|---------------|----------------|----------------|----------------------|--------------|
| 123          | ABC           | Acme Supply Co | CA             | 2000-01-01T00:00:00  | N            |
| 124          | ABC           | Acme Supply Co | IL             | 2004-12-22T00:00:00  | Y            |


- **Type 3**: Add a new attribute  

This methos tracks changes using separate columsn and preservers limited history.

| Supplier_Key | Supplier_Code | Supplier_Name  | Original_Supplier_State | Effective_Date       | Current_Supplier_State |
|--------------|---------------|----------------|-------------------------|----------------------|------------------------|
| 123          | ABC           | Acme Supply Co | CA                       | 2004-12-22T00:00:00  | IL                    |

- **Type 4**: Same as Type 3 but win unlimited histroy by using a **separate history table**

Supplier Table:
| Supplier_Key | Supplier_Code | Supplier_Name              | Supplier_State |
|--------------|---------------|----------------------------|----------------|
| 124          | ABC           | Acme & Johnson Supply Co   | IL             |

Supplier_History Table
| Supplier_Key | Supplier_Code | Supplier_Name              | Supplier_State | Create_Date           |
|--------------|---------------|----------------------------|----------------|----------------------|
| 123          | ABC           | Acme Supply Co             | CA             | 2003-06-14T00:00:00  |
| 124          | ABC           | Acme & Johnson Supply Co   | IL             | 2004-12-22T00:00:00  |



- **Type 5** Type 4 + Type 1
- **Type 6** Type 1,2 and 3


### Type2 SCD (code)


Setup:

Target_table (existing data, acts as our dimension table)

Supplier_Key	Supplier_Code	Supplier_Name	Supplier_State	Start_Date	End_Date


Incoming_data (incoming data):

Supplier_Key	Supplier_Code	Supplier_Name	Supplier_State

```sql
MERGE INTO Target_table AS Target
USING Incoming_data AS Source
ON Target.Supplier_Key = Source.Supplier_Key

-- When matched and all columns are the same, update the End_Date
WHEN MATCHED AND 
   (Target.Supplier_Name = Source.Supplier_Name AND Target.Supplier_State = Source.Supplier_State) THEN
    UPDATE SET End_Date = CURRENT_DATE 

-- When matched and any column is different, insert as a new record
WHEN MATCHED AND 
   (Target.Supplier_Name <> Source.Supplier_Name OR Target.Supplier_State <> Source.Supplier_State) THEN
    INSERT (Supplier_Key, Supplier_Code, Supplier_Name, Supplier_State, Start_Date, End_Date)
    VALUES (Source.Supplier_Key, Source.Supplier_Code, Source.Supplier_Name, Source.Supplier_State, CURRENT_DATE, NULL)

-- When not matched by target, insert the record
WHEN NOT MATCHED THEN
    INSERT (Supplier_Key, Supplier_Code, Supplier_Name, Supplier_State, Start_Date, End_Date)
    VALUES (Source.Supplier_Key, Source.Supplier_Code, Source.Supplier_Name, Source.Supplier_State, CURRENT_DATE, NULL);
```

## Data Processing

### Change Data Capture
Its a technique to identify and capture changes made to data. The changes can be inserts, updates or deletes. The primary goal is to ensure data synchronization, replication, or loading without needing to scan the entire databse or data source.


Imagine we have an e-commerce website with a database taht stores production information. Each day, new products are added, old ones are updated, and some might be removed. Using traditional methods, if you wanted to synchronize this production
data to a data warehouse for analytics, you would have to extract ALL product data nightly, which is bor resource-intensive and time-consuming.

With CDC, instead of extracting all the products, you had only capture the changes made since the last extraction. If 50 products were added, 30 pudated and 10 deleted you had only process those 90 records. This save a lot of computational resources and time.

**microBatchDF`**  
In structured streaming, certain operations, like window functions, required processing in discrete chunks rather than on a continuous stream. this is achive using micro-batches
`microBatchDF` represents the data of a single micro-batch, allowing stateful operations to be applied efficiently on streamed data.

### Processing CDC (code)

Create a Windows function to insert the most recent records. The SQL code would be as follows.

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

The goal is to package that code into a function so that we can launch it in Stream.

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Assuming you've already loaded the data into a DataFrame
df = spark.read.table("customer_window")

# Define the window specification
window_spec = Window.partitionBy("customer_id").orderBy(F.desc("row_time"))

# Use the rank function over the window specification
ranked_df = df.withColumn("rank", F.rank().over(window_spec))

# Filter the rows where rank is 1
newest_df = ranked_df.filter(F.col("rank") == 1).drop("rank")

# If you need to show or collect the result
newest_df.show()

```

Declare function

```python
from pyspark.sql.window import Window

def batch_upsert(microBatchDF, batchId):
    window = Window.partitionBy("customer_id").orderBy(F.col("row_time").desc())
    
    (microBatchDF.withColumn("rank", F.rank().over(window))
                 .filter("rank == 1")
                 .drop("rank")
                 .createOrReplaceTempView("ranked_updates"))
    
    query = """
        MERGE INTO customers_silver c
        USING ranked_updates r
        ON c.customer_id=r.customer_id
            WHEN MATCHED AND c.row_time < r.row_time
              THEN UPDATE SET *
            WHEN NOT MATCHED
              THEN INSERT *
    """
    
    microBatchDF.sparkSession.sql(query)

```

```python
query = (spark.readStream
                  .table("bronze")
                  .filter("topic = 'customers'")
                  .select(F.from_json(F.col("value").cast("string"), schema).alias("v"))
                  .select("v.*")
                  .join(F.broadcast(df_country_lookup), F.col("country_code") == F.col("code") , "inner")
               .writeStream
                  .foreachBatch(batch_upsert)
                  .option("checkpointLocation", "dbfs:/mnt/demo_pro/checkpoints/customers_silver")
                  .trigger(availableNow=True)
                  .start()
          )

query.awaitTermination()
```

### Delta Lake CDF

**CDF** Stands for Change Data Feed  
- Automatically generate CDC feed about Delta Lake Tables.    
- Records row-level changes for all data written into a Delta table.  
	- Row data + metadata (whether row was inserted, deleted or updated)  

### Stream-Stream Joins(Hands On)

### Stream-Static Join

### Stream-Static Join (Hands On)

### Materialized Gold Tables


## Databricks Tooling

## Security and Governance

## Testing and Deployment

## Monitoring and logging

