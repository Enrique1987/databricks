# Databricks Data Engineer Professional - in a Nutshell



## Data Processing.

**CDC**: Change Data Capture, is used to propagate changes made in on database to another. Only acts on database.  
**CDF**: Change Data Feed, broader than CDC because it acts on the changes that thedta has undergone, regardless of whether it is tied to a database.  
`microBatchDF`: Allows data to be processed in micro-batches, which is usefull and necessary for some operations such as Windows functions.  
`.broadcast`: Helps optimize join operations between DataFrames. When join a large DataFrame witha much smaller one, `.broadast` speed up the operation sending smaller Dataframes directly to al lworker nodes. This avoids slow networ shuffling and makes the join process faster.
`watermark`:is used to deal with process where latency can have a big impact.