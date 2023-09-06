### Data Pipelines with Delta Live Tables and Spark SQL


**Auto Loader** is when you have data landing in cloud storage continuously or in upredictable intervals. Instead of scheduling periodic scans of the entiredirectofy,
Auto Loader will automatically pick up an process just the new data as it arrives, making the ingestion process more timely and cost-effective.

**DLT** Delta Live Tables in Databricks provide structured streaming capabilities, which allow data to be continuosly ingested, processed and written to Delta tables.

**What are DLT designed for** Delta Live Tables (DLT) is designed for defining reliable and maintainable pipelines. DLT is not intended for interactive execution in a notebook.

**What happend when you query a DLT that is not attached to a DLT pipeline inside of a notebook ?**
When you query a DLT in a notebook that is not attached to a DLT pipeline, you are querying the table as it is at that moment, no the live streaming version.
When you are querying a DLT outside of the pipeline, you are essentially querying the current state of the Delta table. Whether the table was defined as batch or streaming doesnt´

**How much time could preserve the data the DLT ?**
Delta Lake allows for multiple versions of data to co-exist. Every time you modify a dataset, Delta Lake retains a new version of that dataset. This is how Time travel works by keeping multiple version.
But... retention perios matter, if every change is retained idenfinitely you storage usage would grow rapidly, especially in active dataset with frequent modification. 
Thats why Delta Lake allows you to set a retention prediod for how long to keep old versionof th data.

**Metastore**
Metastore keeps track of all the table metadatga, like the schema and the location of the datga. When you create a table in Delta Lake or DAtabricks, the details bout the table,
including where its data is stored, are saved in the metastored

**Table directory**
Is referring to: Location, Physical Files, Metadata and Logs. For example consider a Delta Lake table saved in a Azure Data Lake Storage(ADLS).
The table directory could be a path like abfss://my-data-lake-container@mydatalakeaccount.dfs.core.windows.net/my-delta-table/ whithn this directory, you´d find 
multiple Parquet Files and Transaction Logs. _delta_log

**Event Log**
Event log is about logging events or changes. In context of Delta Lake, the event log keeps track of transactions but doesn´t serve as a direct way to
view the contents of the table directory. Are desing to capure various acxtivities

**Checkpointing directory** Checkpointing typically refers to a mechanism that saves the state of a stream at regular intervals, ensuring fault-tolerance for streamimg operations.


**checkpoint directory** is mainly used for storing the progress of streaming queries to ensure fault-tolerance.

**What DAG primarily does?**
DAG visualizes the sequence and dependencies of taks.

**Task Details** Typically provide information about the task´s execution, status, duration.	

**row_epectations


**Example of Silver and Gold**
Silver tables enrich data by joining fields from bronze tables. Gold tables provide business level aggregates often used for reporting and dashboarding.

**Job Runs Page**: Provide a detailed overview of all the jobs executed, including those from DLT pipelines.
Clicking on individual tables or task within a job run will providespecifics bout that task.


**Table directory** In a concern of distributed file storage systems, a table directory typically refers to the underlying location in the distributed storage where the data is stored.

**Databricks Tables** Allows you to create tables which are essentially metadata definitions on top of your data. These tables can point to data stored in various formats like 
parquet, Avro, CSV, JSON, etc

**Storage Systems** Databricks can be integrated with different distributed storage systems like Azure Blob Storage, Azure Data Lake, AWS S3 and more.


#### A data engineer is creating a live streaming table to be used by other members of their team. They want to indicate that the table contains silver quality data.
Which of the following describes how the data engineer can clarify this to other members of their team? Select two responses.

 

WHEN QUALITY = SILVER THEN PASS  
**TBLPROPERTIES ("quality" = "silver")**  
None of these answer choices are correct.  
**COMMENT "This is a silver table"**
EXPECT QUALITY = SILVER"  


CHECK AGAIN!!
#### A data engineer needs to examine how data is flowing through tables within their pipeline. 
Which of the following correctly describes how they can accomplish this? Select one response.



**The data engineer can query the flow definition for the direct predecessor of each table and then combine the results.**

The data engineer can view the flow definition of each table in the pipeline from the Pipeline Events log.

The data engineer can combine the flow definitions for all of the tables into one query.

The data engineer can query the flow definition for each table and then combine the results.

The data engineer can query the flow definition for the direct successor of the table and then combine the results.



#### A data engineer is configuring a new DLT pipeline and is unsure what mode to choose.
They are working with a small batch of unchanging data and need to minimize the costs associated with the pipeline.
Which of the following modes do they need to use and why? Select one response

 
Continuous; continuous pipelines ingest new data as it arrives.

Triggered; triggered pipelines update once and cannot be updated again for 24 hours.

Triggered; triggered pipelines update once and cannot be updated again until they are manually run.

**Triggered; triggered pipelines run once and then shut down until the next manual or scheduled update.**

Continuous; continuous pipelines run at set intervals and then shut down until the next manual or scheduled update.



#### Which of the following correctly describes how to access contents of the table directory? Select one response.


The contents of the table directory can be viewed through the checkpointing directory.

The contents of the table directory can be viewed through the Auto Loader directory.

**The contents of the table directory can be viewed through the metastore.**
*The metastore is where the metadata of tables, including their locations schema and other properties are sotred. By querying the metastore you can find out wherethe data 
for a particular table is stored and access its directory path.

The contents of the table directory can be viewed through the flow definition’s output dataset.

The contents of the table directory can be viewed through the event log




#### A data engineer has built and deployed a DLT pipeline. They want to see the output for each individual task.
Which of the following describes how to explore the output for each task in the pipeline? Select one response.

 
They can run the commands connected to each task from within the DLT notebook after deploying the pipeline.
*Not typically how pipelines are debugged, command manually from the notebook to verify task outpus can be inefficient and can also create unnecessary executions*

They can display the output for each individual command from within the notebook using the %run command.
*doenst make sense that answer*

They can specify a folder for the task run details during pipeline configuration.

They can go to the Job Runs page and click on the individual tables in the job run history.

**They can go to the Pipeline Details page and click on the individual tables in the resultant Directed Acyclic Graph (DAG).**






#### A data engineer has created the following query to create a streaming live table from transactions.

 

Code block:

CREATE OR REFRESH STREAMING LIVE TABLE transactions

AS SELECT timestamp(transaction_timestamp) AS transaction_timestamp, * EXCEPT (transaction_timestamp, source)

________________________


Which of the following lines of code correctly fills in the blank? Select two responses.

 

FROM STREAMING LIVE.transactions  
FROM DELTA STREAM(LIVE.transactions)  
**FROM STREAM(LIVE.transactions)**  
FROM STREAMING LIVE (transactions)  
**FROM LIVE.transactions**  


#### Which of the following data quality metrics are captured through row_epectations in a pipeline’s event log? Select three responses.

 

**Failed records**  
**Name**
Flow progress  
**Dataset**  
Update ID


#### A data engineer is using the code below to create a new table transactions_silver from the table transaction_bronze. 
However, when running the code, an error is thrown.

 
```
CREATE OR REFRESH STREAMING LIVE TABLE transactions_silver

(CONSTRAINT valid_date EXPECT (order_timestamp > "2022-01-01") ON VIOLATION DROP ROW)

FROM LIVE.transactions_bronze

```

Which of the following statements correctly identifies the error and the stage at which the error was thrown? Select one response.

 


LIVE.orders_bronze needs to be changed to STREAM(LIVE.orders_bronze). The error will be detected during the Initializing stage.

**A SELECT statement needs to be added to create the columns for the transactions_silver table. The error will be detected during the Initializing stage.**

The EXPECT statement needs to be changed to EXPECT (order_timestamp is NOT NULL). The error will be detected during the Setting Up Tables stage.

A SELECT statement needs to be added to create the columns for the transactions_silver table. The error will be detected during the Setting Up Tables stage.

LIVE.orders_bronze needs to be changed to STREAM(LIVE.orders_bronze). The error will be detected during the Setting Up Tables stage.




#### Which of the following statements accurately describes the difference in behavior between 	s and live tables? Select one response.

*remembering*

**Live Tables**: Tables that are define within a DLT pipeline. The data within these tables is written to disk,
they support features like enforcing data quality, versioning and transactional guarantees.  

**Live Views**: They are intermediate or temporary views taht are used within the context of a DLT pipeline. They allow you to manipulate and transform datga within a pipeline,
but do not store results to a disk as a persistent table does.

knowing that definition, the most acurate answer is:


Live tables can be used to enforce data quality, while views do not have the same guarantees in schema enforcement.

**The results of live tables are stored to disk, while the results of views can only be referenced from within the DLT pipeline in which they are defined.**

Live tables can be used with a stream as its source, while live views are incompatible with structured streaming.

Metrics for live tables can be collected and reported, while data quality metrics for views are abstracted to the user.

The results of live tables can be viewed through a Directed Acyclic Graph (DAG), while the results for live views cannot.



#### A data engineer needs to add a file path to their DLT pipeline. They want to use the file path throughout the pipeline as a parameter for various statements and functions.
Which of the following options can be specified during the configuration of a DLT pipeline in order to allow this? Select one response.


They can add a widget to the notebook and then perform a string substitution of the file path.
*Widgets in Databricks notebooks allow for paremeteized inputs* However requires human interaction to set its.

They can specify the file path in the job scheduler when deploying the pipeline.

They can set the variable in a notebook command and then perform a variable substitution of the file path.

**They can add a key-value pair in the Configurations field and then perform a string substitution of the file path.**

They can add a parameter when scheduling the pipeline job and then perform a variable substitution of the file path.




#### Which of the following correctly describes how code from one library notebook can be referenced by code from another library notebook? Select one response.


**Within a DLT Pipeline, code in any notebook library can reference tables and views created in any other notebook library.**

Within a DLT Pipeline, code in a notebook library can reference tables and views created in another notebook library as long as the referenced notebook library is installed on the other notebook library’s cluster.

Within a DLT Pipeline, code in a notebook library can reference tables and views created in another notebook library that is running on the same cluster.

Within a DLT Pipeline, code in a notebook library can reference tables and views created in another notebook library as long as one notebook library references the other notebook library.

Within a DLT Pipeline, code in notebook libraries cannot reference tables and views created in a different notebook library.



#### A data engineer needs to review the events related to their pipeline and the pipeline’s configurations.
Which of the following approaches can the data engineer take to accomplish this? Select one response.

 


The data engineer can select events of type user_action in the resultant DAG.
*Dag display sequence and dependencies of task*

The data engineer can query events of type user_action from the configured storage location.
*vague option*

**The data engineer can query events of type user_action from the event log.**

The data engineer can query events of type user_action from the checkpoint directory.
*The checkpoint directory is mainly used for storing the progress of streaming queries to ensure fault-tolerance. It does not store pipeline-specific events or configurations.*

The data engineer can select events of type user_action in the output table of the pipeline.




#### A data engineer needs to ensure the table updated_history, which is derived from the table history, contains all records from history.
Each record in both tables contains a value for the column user_id.

 

Which of the following approaches can the data engineer use to create a new data object from updated_history and history containing the records with
matching user_id values in both tables? Select one response.

 


The data engineer can merge the history and updated_history tables on user_id.

The data engineer can create a new dynamic view by querying the history and updated_history tables.

**The data engineer can create a new view by joining the history and updated_history tables.**

The data engineer can create a new temporary view by querying the history and updated_history tables.

The data engineer can create a new common table expression from the history table that queries the updated_history table.
Single Choice


#### A data engineer wants to query metrics on the latest update made to their pipeline. The pipeline has multiple data sources.
Despite the input data sources having low data retention, the data engineer needs to retain the results of the query indefinitely.
Which of the following statements identifies the type of table that needs to be used and why? Select one response.

 


**Streaming live table; streaming live tables can preserve data indefinitely.**


Streaming live table; streaming live tables record live metrics on the query.
*recording metrics doesnt´ necessarily correlate with indefinite data retention*

Streaming live table; streaming live tables are always "correct", meaning their contents will match their definition after any update.

Live table; live tables retain the results of a query for up to 30 days.
*30 days would not be enought *

Live table; live tables only support reading from "append-only" streaming sources.




#### A data engineer has configured and deployed a DLT pipeline that contains an error. The error is thrown at the third stage of the pipeline,
but since DLT resolves the order of tables in the pipeline at different steps, they are not sure if the first stage succeeded.
Which of the following is considered a good practice to determine this? Select one response.

 


The data engineer can fix the tables using iterative logic, starting at their earliest dataset.

The data engineer can fix the tables using iterative logic, starting at the dataset containing the error.

The data engineer can fix the tables from the Directed Acyclic Graph (DAG), starting at their earliest dataset.

The data engineer can fix the tables from the Directed Acyclic Graph (DAG), starting at the dataset containing the error.

**The data engineer can fix one table at a time, starting at their earliest dataset.**



#### Which of the following are guaranteed when processing a change data capture (CDC) feed with APPLY CHANGES INTO? Select three responses.

 

**APPLY CHANGES INTO automatically orders late-arriving records using a user-provided sequencing key.**
APPLY CHANGES INTO automatically quarantines late-arriving data in a separate table.
APPLY CHANGES INTO supports insert-only and append-only data.
**APPLY CHANGES INTO defaults to creating a Type 1 SCD table.**
**APPLY CHANGES INTO assumes by default that rows will contain inserts and updates.**




#### A data engineer has a Delta Live Tables (DLT) pipeline that uses a change data capture (CDC) data source. 
They need to write a quality enforcement rule that ensures that records containing the values INSERT or UPDATE
in the operation column cannot contain a null value in the name column. The operation column can contain one of three values: INSERT, UPDATE, and DELETE.
If the constraint is violated, then the entire transaction needs to fail.  
Which of the following constraints can the data engineer use to enforce this rule? Select one response.

 
**Summarize**
- If `operation` is INSERT or UPDATE, then `name` should not be NULL
- If the condition is vilated, the entire transaction should fail.


**CONSTRAINT valid_name EXPECT (name IS NOT NULL or operation = "DELETE") ON VIOLATION FAIL UPDATE**

CONSTRAINT valid_operation EXPECT (valid_operation IS NOT NULL and valid_operation = "INSERT") ON VIOLATION DROP ROW
*no even comparing the name column*

CONSTRAINT valid_operation EXPECT (operation IS NOT NULL) ON VIOLATION DROP ROW

*Wrong as not even consider "name is not null"*


CONSTRAINT valid_name EXPECT (name IS NOT NULL or operation = "DELETE") ON VIOLATION DROP ROW
*This comes close, but the action is to drop the row insted of failing the update* 

CONSTRAINT valid_id_not_null EXPECT (valid_id IS NOT NULL or operation = "INSERT")ON VIOLATION FAIL UPDATE
*not even comparing the name column*


#### Which of the following correctly describes how Auto Loader ingests data? Select one response.


**Auto Loader incrementally ingests new data files in batches.**

Auto Loader automatically writes new data files continuously as they land.

Auto Loader writes new data files in incremental batches.

Auto Loader only detects new data files during scheduled update intervals.

Auto Loader automatically detects new data files during manual or scheduled updates.



#### A data engineer wants to query metrics on the latest update made to their pipeline. They need to be able to see the event type and timestamp for each update.
Which of the following approaches allows the data engineer to complete this task? Select one response. CHECK AGAIN


The data engineer can view the update ID from the Pipeline Details page in the user_action table.  
*This option does not explicit mention querying for the event type or timestamp*

**The data engineer can query the update ID from the events log where the event type is create_update.**
*That seem to be the correct one cause sounds like it might refer to updates made to the pipeline*  

The data engineer can query the update ID from the events log where the action type is user_action.  
*It doesn´t specify thatt this action type would have the event type and timestamp of pipeline updates*

The data engineer can query the update ID from the events log where the event type is last_update.
*last update could be the most recent update but we need to see "each update"*

The data engineer can view the update ID from the Pipeline Details page in the create_update table.
*Does not explicitly state that the data engineer can see the event type and timestamp*


#### A data engineer needs to query a Delta Live Table (DLT) in a notebook. The notebook is not attached to a DLT pipeline.

Which of the following correctly describes the form of results that the query returns? Select one response.


Queries outside of DLT will return the most recent version from DLT tables only if they were defined as a streaming table

Live queries outside of DLT will return snapshot results from DLT tables only if they were defined as a batch table.

Queries outside of DLT will return the most recent version from DLT tables, regardless of how they were defined.

Queries outside of DLT will return snapshot results from DLT tables only if they were defined as a streaming table

**Queries outside of DLT will return snapshot results from DLT tables, regardless of how they were defined.**



#### A data engineer needs to identify the cloud provider and region of origin for each event within their DLT pipeline.
Which of the following approaches allows the data engineer to view this information? Select one response. 



The data engineer can view this information in the Task Details page for each task in the pipeline.
*The Task Details page would typically provide information about the task's execution status, duration,*

The data engineer can use a SELECT query to directly query the cloud_details field of the event.

The data engineer can use a utility command in Python to list information about each update made to a particular data object.
*This doesn´t address the specific need*

The data engineer can view the event details for the pipeline from the resultant Directed Acyclic Graph (DAG).
*While the DAG visualizes the sequence and dependencies of tasks, it doesnt typically display detailed event information*

**The data engineer can load the contents of the event log into a view and display the view.**
*This method would be suitable if the event log already captures the required information*



#### A data engineer is running a Delta Live Tables (DLT) notebook. They notice that several commands display the following message:

This Delta Live Tables query is syntactically valid, but you must create a pipeline in order to define and populate your table.
Which of the following statements explains this message? Select one response.

 


DLT notebooks must be run at scheduled intervals using the job scheduler.

DLT queries must be connected to a pipeline using the pipeline scheduler.

DLT does not support the execution of Python and SQL notebooks within a single pipeline.

**DLT is not intended for interactive execution in a notebook.**

DLT does not support the execution of Python commands.




#### Which of the following are advantages of using a Delta Live Tables (DLT) pipeline over a traditional ETL pipeline in Databricks? Select two responses.

DLT automates data management through physical data optimizations and schema evolution.  
DLT decouples compute and storage costs regardless of scale.  
**DLT has built-in quality controls and data quality monitoring.**
**DLT provides granular observability into pipeline operations and automatic error handling.**
DLT leverages additional metadata over other open source formats such as JSON, CSV, and Parquet.  


#### A data engineer has built and deployed a DLT pipeline. They want to perform an update that writes a batch of data to the output directory. 
Which of the following statements about performing this update is true? Select one response.

 


All newly arriving data will be continuously processed through their pipeline. Metrics will be reported for the current run if specified during pipeline deployment.

**With each triggered update, all newly arriving data will be processed through their pipeline. Metrics will always be reported for the current run.**

With each triggered update, all newly arriving data will be processed through their pipeline. Metrics will not be reported for the current run.

With each triggered update, all newly arriving data will be processed through their pipeline. Metrics will be reported if specified during pipeline deployment.

All newly arriving data will be continuously processed through their pipeline. Metrics will always be reported for the current run.




#### A data engineer has a Delta Live Tables (DLT) pipeline that uses a change data capture (CDC) data source. 
They need to write a quality enforcement rule that ensures that values in the column operation do not contain null values.
If the constraint is violated, the associated records cannot be included in the dataset. 

 

Which of the following constraints does the data engineer need to use to enforce this rule? Select two responses.


CONSTRAINT valid_operation EXCEPT (operation) ON VIOLATION DROP ROW

CONSTRAINT valid_operation EXCEPT (operation != null) ON VIOLATION FAIL UPDATE

CONSTRAINT valid_operation ON VIOLATION FAIL UPDATE

CONSTRAINT valid_operation EXPECT (operation IS NOT NULL)

**CONSTRAINT valid_operation EXPECT (operation IS NOT NULL) ON VIOLATION DROP ROW**
*here is the key "if the constrain is violated the records cannot be included" if it were "If the constraint is violated, then the entire transaction needs to fail" then 
we would need "ON VIOLATION FAIL UPDATE" 

CONSTRAINT valid_operation EXCEPT (operation) ON VIOLATION DROP ROW
