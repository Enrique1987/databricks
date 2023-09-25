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

```
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

**Python**  

```
(spark.readStream
      .table("bronze")
      .createOrReplaceTempView("bronze_tmp"))
```

**SQL**

```
CREATE OR REPLACE TEMPORARY VIEW orders_silver_tmp AS
  SELECT v.*
  FROM (
    SELECT from_json(cast(value AS STRING), "order_id STRING, order_timestamp Timestamp, customer_id STRING, quantity BIGINT, total BIGINT, books ARRAY<STRUCT<book_id STRING, quantity BIGINT, subtotal BIGINT>>") v
    FROM bronze_tmp
    WHERE topic = "orders")
```


**Python**  
```
query = (spark.table("orders_silver_tmp")
               .writeStream
               .option("checkpointLocation", "dbfs:/mnt/demo_pro/checkpoints/orders_silver")
               .trigger(availableNow=True)
               .table("orders_silver"))

query.awaitTermination()
```  

Insted of the middle part in Sql now I will all in Python**

```
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

Thanks to ACID in that case the "A" from Atomicy, a transaction will either fully sucess or it´ll fail there is no posible that just one part success.
Thanks to ACID in this case, the "A" standos for Atomicity. This means that a transaciton will either fully succeed or it will fail; its not possible for only a part of it to suceed".



### Streaming Deduplication (code)

### Slowly Changing Dimensions 

### Type2 SCD (Hands On)





## Data Processing

## Databricks Tooling

## Security and Governance

## Testing and Deployment

## Monitoring and logging

