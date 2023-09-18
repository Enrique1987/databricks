# databricks  Associate and Professional Questions 

Some of the questions are just theortical concepts that we have to know.



### DLT Delta Live Tables

#### Events Logs

DLT uses event logs to stroe much of the important information used to manage, report and understand what´s happening during pipeline execution.

`event log`: is managed as a Delta Lake table with some of the more imoprtan fiesld stored as nested Json data.

#### Tables, Live Tables and Stream Live Tables, what are the difference ?

`Tables`: Made for data processing in batch mode

`Stream Table`: continuously ingest and update data from streaming sources, presenting a real-time view of data as it's being received. 


`Live Tables`: Reflects the results of the query that defines it, including when the query defining the table or view is updated,
 or an input data source is updated. Like a traditional materialized view, a live table or view may be entirely computed when possible to optimize computation resources and time.
 
* Always "correct", meaning their contents will match their definition after any update.
* Return same results as if table had just been defined for first time on all data.
* Should not be modified by operations external to the DLT Pipeline (you'll either get undefined answers or your change will just be undone).

 
 in a very very simple way to think about that could be a table that is automatically refresh, 
 
`streaming live table`: Processes data that has been added only since the last pipeline update.

* Only supports reading from "append-only" streaming sources.
* Only reads each input batch once, no matter what (even if joined dimensions change, or if the query definition changes, etc).
* Can perform operations on the table outside the managed DLT Pipeline (append data, perform GDPR, etc).



#### Scenario of Stream table.

**Real-time Fraud Detection:**

**Scenario:**
Imagine a bank that offers online banking services to its customers. With millions of transactions occurring every day,
it's critical for the bank to quickly identify potentially fraudulent transactions to protect its customers.

**Stream Table Use:**
The bank sets up a streaming system where every transaction is instantly sent to a stream table. 
As each transaction comes in, it's analyzed in real-time against a set of rules or machine learning models to identify if it looks suspicious.
If a transaction is deemed suspicious, an alert is generated, and the bank can take immediate action, such as blocking the transaction, notifying the customer,
or flagging it for further investigation.

**Why Not Batch Processing?**
If the bank used batch processing, they'd collect transactions over a set period (e.g., an hour or a day) and then analyze them all at once. 
The problem with this approach in the fraud detection scenario is the delay.

A fraudulent transaction might not be detected until the batch is processed, which could be hours after the transaction occurred. By that time:

The fraudster may have already caused significant financial damage.
The actual customer may face inconvenience if, for example, their card is used elsewhere or they check their account and find unauthorized transactions.
The bank might face reputational damage and potential financial liabilities.
Conclusion:
For scenarios like fraud detection, where instant response is crucial, stream tables and real-time processing are essential. Batch processing, due to its inherent delay, would not be suitable for such time-sensitive applications.




#### Scenario of Live Table and Stream Live Table

**Live Table Example: E-Commerce Inventory Management**

*Scenario:*  
An e-commerce platform wants to maintain an up-to-date inventory of products. This inventory is affected by new stock arrivals, product returns, and products being sold.

**Why a Live Table?:**

**Frequent Updates:** Stock levels can be influenced by a multitude of factors such as sales, returns, and new shipments.
**Query Definition Updates:** Sometimes the e-commerce platform might want to change the logic of how it calculates available inventory.
For instance, they might decide to keep a buffer stock and not show it to customers. 
With a live table, any change in the logic will be reflected in the table without the need for manual adjustments.

**Instant Reflection:** If there's an error or update in the source data (maybe a returned item was mistakenly marked as 'damaged' when it wasn't), correcting this in the source will instantly reflect in the live table.


**Streaming Live Table Example: Social Media Trend Analysis**

**Scenario:**vv
A social media platform wants to detect trending hashtags in real-time to showcase them to its users.

**Why a Streaming Live Table?:**

Continuous Data Ingestion: New posts, comments, and hashtags are continuously being created. The platform doesn't need to know about every hashtag ever used, just the ones
trending right now.  
**Stateful Processing:** If the definition of "trending" changes (e.g., from "most hashtags in the last hour" to "most hashtags in the last 30 minutes with at least
1,000 unique users using it"), the streaming live table will process new data based on this new logic. 
The historical data doesn't need recomputation because the platform is only interested in what's trending now.

**Efficiency:** Instead of recalculating trends from all historical data every time, 
the system only focuses on the new data. This is both resource-efficient and ensures real-time results.



#### Large scale ETL is complex and brittle

**complex pipeline development:**

	 - Hard to build and maintain table depencencies

	 - Difficult to switch between `batch` and `stream`   
	 
**Data quality and governance**  

    - Difficult to monitor and enfornce `data quality`
	- Impossible to trace data lineage


**Difficult pipeline operations**

	- Poor ´observability´ at granual data levels
	- Error handling and `recovery is laborious`
	
	
#### Delta Live Tables come to action

**Agility**: Build batch and streaming data pipelines.
**Trust your data** Quality controls with expectations and actions to take
**Scale with reliability** Easy scale.


#### What is a Live Table and what provides for

DLT: materialized views for th lakehause. 
Provides: - manage dependencies
          - Control quality
          - Automate opeations
          - Simplify collaboration
          - Save costs
          - Reduce latency


##### How to use DLT 

1) declare in notebooks
2) workflows in Delta Live Tables + start

#### What are the differences between development and producdtion in DLT, what are teh best practices ?

Development Mode: 
			- re-use **long-running cluster** running for **fast iteration**
            - No retries on errorrs enabling faster debugging
Production mode:
			Cuts costs by turning off clusters as soon as they are done
			Escalating retries, including cluster restarts `ensure reliability`
			
##### What can you do if you have many DLT 

Declaring dependencies from Lives TAbles

```
CREATE LIVE TABLE table_1
AS SELECT ... FROM schema.my_table


CREATE LIVE TABLE table_2
AS SELECT ... FROM LIVE.table_1


```

DLT detects LIVE dependencies and executes all operations in correct order.
DLT handles parallelism and captures the `lineage` of data.

##### How can you ensure Data Quality in DLT

You can ensure correctness with Expectations

```
CONSTRAINT valid_timestamp
EXPECT(timestamp > '2012-01-01')
ON VIOLATION DROP	
```

The records that violate expectations you can "Track", "Drop", "Abort"


#### What is Event Logs and what offers

Event Log automatically records all pipelines operations.

**Operational Statistics:** Time and current status, for all operations, Pipeline and cluster configurations, Row counts  
**Provenance:** Table and schema definitions and declared properties, Table-level lineage, Query plans 
**Data Quality:** Expectation pass/failure /drop statistics 

#### What does STREAM ?

CREATE STREAMING LIVE TABLE mystream
AS SELECT * 
FROM STREAM(my_table)

`STREAM` Function: When you see STREAM(my_table), it means that my_table is being treated as a streaming source. 
Instead of treating it as a static batch of data, Databricks will continuously monitor it for new data and process that data in real-time.

#### What is Automated Data Management ?

refers to the ability of DLTs to automatically optimizes data for performance & ease-of-use

**Best Practices** DLT encodes Delta best practices automatically when creating DLT: `optimizerWrite`, `AutoCompact`, `tuneFileSizesForRewrites`
**Physical Data** DLT automatically manages your physical data to minimice cost and optimize performance --> runs vacuum, run optimize 
**Schema Evolution** Schema evolution is handle for owner

#### CDC Change data capture  in DLT

CDC Maintain and up-to-date replica of a talbe stored elsewhere

```
APPLY CHANGES INTO LIVE.table_1
FROM STREAM(LIVE.table_1_updates)
KEYS (id)
SQUENCE BY ts
```

#### Data Live Tables with SQL

##### Declaring Delta Live Tables

Bronze --> Silver --> Gold
```
CREATE OR REFRESH STREAMING LIVE TABLE orders_bronze
AS SELECT current_timestamp() processing_time, input_file_name() source_file, *
FROM cloud_files("${source}/orders", "json", map("cloudFiles.inferColumnTypes", "true"))
```
we go now for the Silver  Table

```
CREATE OR REFRESH STREAMING LIVE TABLE orders_silver
(CONSTRAINT valid_date EXPECT (order_timestamp > "2021-01-01") ON VIOLATION FAIL UPDATE)
COMMENT "Append only orders with valid timestamps"
TBLPROPERTIES ("quality" = "silver")
AS SELECT timestamp(order_timestamp) AS order_timestamp, * EXCEPT (order_timestamp, source_file, _rescued_data)
FROM STREAM(LIVE.orders_bronze)
```


#### Quality Enforcement continued. Create a Stream Live talble and make the following constrains

* Create a bronce Streaming live table
* Quality constrains in the silver table

In order to ensure only good data makes it into our silver table, we'll write a series of quality enforcement rules that ignore the expected null values in delete operations.

We'll break down each of these constraints below:

##### **`valid_id`**
This constraint will cause our transaction to fail if a record contains a null value in the **`customer_id`** field.

##### **`valid_operation`**
This contraint will drop any records that contain a null value in the **`operation`** field.

##### **`valid_address`**
This constraint checks if the **`operation`** field is **`DELETE`**; if not, it checks for null values in any of the 4 fields comprising an address. Because there is no additional instruction for what to do with invalid records, violating rows will be recorded in metrics but not dropped.

##### **`valid_email`**
This constraint uses regex pattern matching to check that the value in the **`email`** field is a valid email address. It contains logic to not apply this to records if 
the **`operation`** field is **`DELETE`** (because these will have a null value for the **`email`** field). Violating records are dropped.


```
CREATE OR REFRESH STREAMING LIVE TABLE customers_bronze
COMMENT "Raw data from customers CDC feed"
AS SELECT current_timestamp() processing_time, input_file_name() source_file, *
FROM cloud_files("${source}/customers", "json")
```
Apply Constrains in the in the bronce Table

```
CREATE STREAMING LIVE TABLE customers_bronze_clean
(CONSTRAINT valid_id EXPECT (customer_id IS NOT NULL) ON VIOLATION FAIL UPDATE,
CONSTRAINT valid_operation EXPECT (operation IS NOT NULL) ON VIOLATION DROP ROW,
CONSTRAINT valid_name EXPECT (name IS NOT NULL or operation = "DELETE"),
CONSTRAINT valid_address EXPECT (
  (address IS NOT NULL and 
  city IS NOT NULL and 
  state IS NOT NULL and 
  zip_code IS NOT NULL) or
  operation = "DELETE"),
CONSTRAINT valid_email EXPECT (
  rlike(email, '^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$') or 
  operation = "DELETE") ON VIOLATION DROP ROW)
AS SELECT *
  FROM STREAM(LIVE.customers_bronze)
  
```

#### In the previos table proceed with CDC with APPLY Changes INTO for the silver

CREATE OR REFRESH STREAMING LIVE TABLE customers_silver;

APPLY CHANGES INTO LIVE.customers_silver
  FROM STREAM(LIVE.customers_bronze_clean)
  KEYS (customer_id)
  APPLY AS DELETE WHEN operation = "DELETE"
  SEQUENCE BY timestamp
  COLUMNS * EXCEPT (operation, source_file, _rescued_data)


#### What kind of SCD is taking of Apply Changes into

APPLY CHANGES INTO defaults to creating a Type 1 SCD table, meaning that each unique key will have at most 1 record and that updates will overwrite the original information.


#### Troubleshooting DLT SQL Syntax



### Data Governance models



Programmatically grant, deny and revoke access to ata objects

example: `GRANT SELECT ON TABLE my_table TO user@mycopany.com`

**Data Objects**: CATALOG, SCHEMA, TABLE, VIEW, FUNCTION, ANY FILE
**Privilege**: SELECT, MODIFY, CREATE, READ_METADATA, USAGE, ALL_PRIVILEGES
**Operations**: GRANT, DENY, REVOKE



Granting Privileges by Role

**Databricks administgrator** All objects in the catalog and the underlying filesystem.  
**Catalog owner** : All objects in the catalog.
**Database owner**: All objects in the database.
**Table owner**: Only the table.



catalog --> Schema(database) -->(Table, View, Function)


#### Unity Catalog

Centralized governance solution across all your workspace on any cloud.

Unify governance for all data and AI assets

- files, tables, machine learning models and dashboards


**UC hiearchy**

UC Metastore --> catalog --> Schema(database) -->(Table, View, Function)


**Identities for UC:**

Users: Identified by emal-address, can have a admin roll  

Service PRinciples: Identified by Application IDs, for tools and applications

Groups: grouping Users and Service Principles


**Identity federation** 





