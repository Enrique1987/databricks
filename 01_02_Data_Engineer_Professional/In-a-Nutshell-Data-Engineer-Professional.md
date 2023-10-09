# Databricks Data Engineer Professional - in a Nutshell



## Data Processing.

**CDC**: Change Data Capture, is used to propagate changes made in on database to another. Only acts on database.  Is a Theretical concept or patter rather than any mechanism. 
**CDF**: Change Data Feed, broader than CDC because it acts on the changes that the data has undergone, regardless of whether it is tied to a database. Its a mechanish and could be activate as `SET TBLPROPERTIES (delta.enableChangeDataFeed = true)`   its generate a log of changes made to a Delta table.
`microBatchDF`: Allows data to be processed in micro-batches, which is usefull and necessary for some operations such as Windows functions.  
`.broadcast`: Helps optimize join operations between DataFrames. When join a large DataFrame witha much smaller one, `.broadast` speed up the operation sending smaller Dataframes directly to al lworker nodes. This avoids slow networ shuffling and makes the join process faster.
`.withWatermark`:is used to deal with process where latency can have a big impact.  
**Singleplex Ingestion**: Every Raw data to a Delta Lakem, usually Batch processing.  
**Multiplex Ingestion**: Ingesting multiple sources of data concurrently into a single location. Optimal for Real time processing (data comming from a pop up system)