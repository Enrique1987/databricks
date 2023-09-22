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
- **Singleplex Ingestion**: Every Raw data to a Delta Lake   
- **Mutiplex Ingestion**: For nearly real-time data ingestion, normaly from a pop up system.  
	- Do not use the pop up system as bronze leyer as they are not real tables and have limited time of retention.  
	
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
```
from pyspark.sql import functions as F

json_schema = "device_id LONG, time TIMESTAMP, heartrate DOUBLE"

(spark
   .readStream.table("bronze")
   .filter("topic = 'bpm'")
   .select(F.from_json(F.col("value").cast("string"), json_schema).alias("v"))
   .select("v.*")
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
	


### Gold Query Layer

**Gold Layer**
- Powers ML applications, reporting, dashboards, ad hoch analytics
- Reduces costs associated with ad hoch queries on silver tables
- Allow fine grained permissions
- Reduces strain on production systems  
- Shifts query updates to production workloads

### Storing Data Securely

### Propagating Updated and Deletes

### Orchestration and Scheduling



## Udemy

## Data Modeling

## Data Processing

## Databricks Tooling

## Security and Governance

## Testing and Deployment

## Monitoring and logging

