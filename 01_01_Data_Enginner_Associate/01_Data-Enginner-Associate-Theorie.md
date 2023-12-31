
## Databricks Theorie for Data Engineer Associate.

The theory consists of both theoretical concepts and the corresponding code. Both will be ask in the Exam.

## Data Lakehouse

A Data Lakehouse is a unified data platform that combines the bes features of `data lakes` and `data warehouse`. If offers the vast storage capabilities and flexibility of a data lakehause
to handle large volumes of raw, detailed data, alongside the strutured querying and performance optimizationof a data warehouse.
This hybrid approach aims to support a wide range of use cases, FROM big data processing and machine learning to business intelligence and analytics, all within a single platform.


**Challenges in the Data Lakehouse:** 

- Large scale ETL is complex and brittle.  

**Complex pipeline development:** 
 
- Hard to build and maintain table depencencies´.  
- Difficult to switch between `batch` and `stream`.     
	 
**Data quality and governance**   

- Difficult to monitor and enfornce `data quality`.   
- Impossible to trace data lineage.  

**Difficult pipeline operations** 
  
- Poor ´observability´ at granual data levels.  
- Error handling and `recovery is laborious`.    
	


## ETL with Spark SQL and Python

### External Table

- Location need to be added.
- We cannot expect the performance guarantees associated with Delta Lake, example with DT you always guery the most recent version of your source data but
it could not be the case with external tables.


### External Tables: Querying Files Directly


```python
events_kafka = "dbfs:/mnt/path/"
files = dbutils.fs.ls(events_kafka)
display(files)


data_path = "dbfs:/mnt/my_path//001.json"
data_json = spark.sql(f"SELECT * FROM json.`{data_path}`")
display(data_json)


sales_csv_path = "dbfs:/mnt/my_path/"
display(spark.sql(f"SELECT * FROM csv.`{sales_csv_path}`"))

```

### External Tables: Querying different types of data

`json` `text` `binaryFile` `csv`


```sql
CREATE OR REPLACE VIEW event_view
AS SELECT * FROM json.`dbfs:/mnt/my_path/`

CREATE OR REPLACE TEMP VIEW events_temp_view
AS SELECT * FROM json.`dbfs:/mnt/my_path/`

SELECT * FROM text.`dbfs:/mnt/my_path/`

SELECT * FROM binaryFile.`dbfs:/mnt/my_path/`

SELECT * FROM csv.`dbfs:/mnt/my_path/`

```
**3 different ways to query FROM a Directory**

```sql
SELECT * FROM json.`${dataset.bookstore}/customers-json/export_001.json` 
UNION ALL
SELECT * FROM json.`${dataset.bookstore}/customers-json/export_*.json` 
UNION ALL
SELECT * FROM json.`${dataset.bookstore}/customers-json/` 
```

### External Tables - Providing Options for External Sources
A table is classified as external based on whether you define a storage LOCATION for it, regardless of whether that location is inside DBFS or in other cloud storage services.

```sql
DROP TABLE IF EXISTS books_csv;

CREATE TABLE  if not exists books_csv
  (book_id STRING, title STRING, author STRING, category STRING, price DOUBLE)
USING CSV
OPTIONS (
  header = "true",
  delimiter = ";"
)
LOCATION "${dataset_path}/books-csv"
```

```python
spark.sql(f"""
CREATE TABLE IF NOT EXISTS sales_csv
  (order_id LONG, email STRING, transactions_timestamp LONG, total_item_quantity INTEGER, purchase_revenue_in_usd DOUBLE, unique_items INTEGER, items STRING)
USING CSV
OPTIONS (
  header = "true",
  delimiter = "|"
)
LOCATION "{sales_csv_path}"
""")
```

- Convert a external location in a DELTA table. --> Its a Delta Table but still a external Table.

```sql
CREATE TABLE my_delta_table
USING DELTA
LOCATION '/my_path/'
```
**Describe Extended vs detail vs history**

- `DESCRIBE EXTENDED` for Data types  
- `DESCRIBE DETAIL` for metadata associate to the Table  
- `DESCRIBE HISTORY` for the opertions where made in the Table



### Extracting Data FROM SQL Databases

```sql
CREATE TABLE
USING JDBC
OPTIONS (
    url = "jdbc:{databaseServerType}://{jdbcHostname}:{jdbcPort}",
    dbtable = "{jdbcDatabase}.table",
    user = "{jdbcUsername}",
    password = "{jdbcPassword}"
)
```


### Testing

```python
assert spark.table("events_json"), "Table named `events_json` does not exist" 

assert spark.table("events_json").columns == ['key', 'offset', 'partition', 'timestamp', 'topic', 'value'], "Please name the columns in the order provided above"

assert spark.table("events_json").dtypes == [('key', 'binary'), ('offset', 'bigint'), ('partition', 'int'), ('timestamp', 'bigint'), ('topic', 'string'), ('value', 'binary')], "Please make sure the column types are identical to those provided above"

total = spark.table("events_json").count()
assert total == 2252, f"Expected 2252 records, found {total}"

```

### Writing to Tables

`INSERT OVERWRITE`, `INSERT INTO`, `MERGE INTO`


`INSERT OVERWRITE`: Overwrite the actual data for the given one.  
`INSERT INTO`: Append the give data to the Table. May incur duplication of data.  
`MERGE INTO`: It is used when we want to insert data and at the same time we do not want to have repeated data.  

```sql
INSERT OVERWRITE orders
SELECT * FROM parquet.`${path}/orders`
```



```sql
MERGE INTO books b
USING books_updates u
ON b.book_id = u.book_id AND b.title = u.title
WHEN NOT MATCHED AND u.category = 'Computer Science' THEN 
  INSERT *
```

### Cleaning Data

```python
FROM pyspark.sql import functions as F
FROM pyspark.sql.functions import col


data_path_24 = "dbfs:/mnt/my_path/"
df = spark.createDataFrame(data=[(None, None, None, None), (None, None, None, None), (None, None, None, None)], 
                           schema="user_id: string, user_first_touch_timestamp: long, email:string, updated:timestamp")
(spark.read
      .parquet(f"{data_path_24}/my_parque_file")
      .withColumn("updated", F.current_timestamp())
      .union(df)
      .write
      .mode("overwrite")
      .saveAsTable("users_dirty"))



usersDF = spark.read.table("users_dirty")
usersDF.SELECTExpr("count_if(email IS NULL)")
usersDF.where(col("email").isNull()).count()  
userDF.distinct().count()	  


dedupedDF = (usersDF
    .where(col("user_id").isNotNull())
    .groupBy("user_id", "user_first_touch_timestamp")
    .agg(max("email").alias("email"), 
         max("updated").alias("updated"))
    )
dedupedDF.count()
```


**Validate Datasets**

The result should be True or False


```sql
SELECT max(row_count) <= 1 no_duplicate_ids FROM (
  SELECT user_id, count(*) AS row_count
  FROM deduped_users
  GROUP BY user_id)
``` 

```python
FROM pyspark.sql.functions import count

display(dedupedDF
    .groupby("user_id")
    .agg(count("*").alias("row_count"))
    .SELECT((max("row_count") <= 1).alias("no_duplicate_ids"))) # true or false 
```

**Date Format and Regex**

```sql
SELECT 
  --*, 
  date_format(first_touch, "MMM d, yyyy") AS first_touch_date,
  date_format(first_touch, "HH:mm:ss") AS first_touch_time,
  regexp_extract(email, "(?<=@).+", 0) AS email_domain
FROM (
  SELECT *,
    CAST(user_first_touch_timestamp / 1e6 AS timestamp) AS first_touch 
  FROM deduped_users
)
```

```python
FROM pyspark.sql.functions import date_format, regexp_extract

display(dedupedDF
    .withColumn("first_touch", (col("user_first_touch_timestamp") / 1e6).cast("timestamp"))
    .withColumn("first_touch_date", date_format("first_touch", "MMM d, yyyy"))
    .withColumn("first_touch_time", date_format("first_touch", "HH:mm:ss"))
    .withColumn("email_domain", regexp_extract("email", "(?<=@).+", 0))
	.SELECT("first_touch", "first_touch_date", "first_touch_time", "email_domain")
)

```

### Advanced Transformations

```python
def clone_source_table(table_name, source_path, source_name=None):
    "Make shallow clone table"   

    source_name = table_name if source_name is None else source_name
    print(f"Cloning the \"{table_name}\" table FROM \"{source_path}/{source_name}\".", end="...")
    
    spark.sql(f"""
        CREATE OR REPLACE TABLE {table_name}
        SHALLOW CLONE delta.`{source_path}/{source_name}`
        """)
```

```python
data_path_2_5 = "dbfs:/mnt/my_path/"	
clone_source_table("sales", f"{data_path_2_5}/ecommerce/delta", "sales_hist")
```

```python
df = spark.table("events_raw")
for col, dtype in df.dtypes:
    print(f"{col}: {dtype}")
```

### Work with Nested Data

**Note**: Spark SQL has a built-in functionality to directly interact with nested data stored as JSON string or struct types

Use `:` syntax in queries to access subfiels in JSON strings  
Use `.` syntax in queries to access subfiesl in struct types  
`schema_of_json()` returns the schema derived FROM an example JSON string.  
`FROM_json()` parses a column containing a JSON string into a struct type using the specified schema.  

Let's use the JSON string example above to derive the schema, then parse the entire JSON column into struct types.

```sql
CREATE OR REPLACE TEMP VIEW parsed_customers AS
  SELECT customer_id, FROM_json(profile, schema_of_json('{"first_name":"Thomas","last_name":"Lane","gender":"Male","address":{"street":"06 Boulevard Victor Hugo","city":"Paris",
                                                          "country":"France"}}')) AS profile_struct
  FROM customers;
  
SELECT * FROM parsed_customers
```
	
```python
FROM pyspark.sql.functions import FROM_json, schema_of_json

json_string = """
{"device":"Linux","ecommerce":{"purchase_revenue_in_usd":1047.6,"total_item_quantity":2,"unique_items":2},"event_name":"finalize","event_previous_timestamp":1593879787820475,
"event_timestamp":1593879948830076,"geo":{"city":"Huntington Park","state":"CA"},"items":[{"coupon":"NEWBED10","item_id":"M_STAN_Q","item_name":"Standard Queen Mattress",
"item_revenue_in_usd":940.5,"price_in_usd":1045.0,"quantity":1},{"coupon":"NEWBED10","item_id":"P_DOWN_S","item_name":"Standard Down Pillow","item_revenue_in_usd":107.10000000000001,
"price_in_usd":119.0,"quantity":1}],"traffic_source":"email","user_first_touch_timestamp":1593583891412316,"user_id":"UA000000106459577"}
"""
parsed_eventsDF = (events_stringsDF
    .SELECT(FROM_json("value", schema_of_json(json_string)).alias("json"))
    .SELECT("json.*")
)

display(parsed_eventsDF)

```

Use of `:` 
  
```sql
SELECT * FROM events_strings WHERE value:event_name = "finalize" ORDER BY key LIMIT 1
```

```python
display(events_stringsDF
    .where("value:event_name = 'finalize'")
    .orderBy("key")
    .limit(1)
)

```

**Manipulate Arrays

`explode()` separates the elements of an array into multiple rows; this creates a new row  for each elemnt.  
`size()` provides a count for the number of elements in an array for each row.  


```sql
CREATE OR REPLACE TEMP VIEW exploded_events AS
SELECT *, explode(items) AS item
FROM parsed_events;

SELECT * FROM exploded_events WHERE size(items) > 2
```


```python
FROM pyspark.sql.functions import explode, size

exploded_eventsDF = (parsed_eventsDF
    .withColumn("item", explode("items"))
)

display(exploded_eventsDF.where(size("items") > 2))
```

`collect_set()` collects unique values for a field, including fields within arrays.  
`flatten()` combines multiple arrays into a single array.  
`array_distinct()` removes duplicate elements FROM an array.  


```sql
SELECT user_id,
  collect_set(event_name) AS event_history,
  array_distinct(flatten(collect_set(items.item_id))) AS cart_history
FROM exploded_events
GROUP BY user_id
```

```python
FROM pyspark.sql.functions import array_distinct, collect_set, flatten

display(exploded_eventsDF
    .groupby("user_id")
    .agg(collect_set("event_name").alias("event_history"),
            array_distinct(flatten(collect_set("items.item_id"))).alias("cart_history"))		
```

**Join Tables**

```sql
CREATE OR REPLACE TEMP VIEW item_purchases AS

SELECT * 
FROM (SELECT *, explode(items) AS item FROM sales) a
INNER JOIN item_lookup b
ON a.item.item_id = b.item_id;

SELECT * FROM item_purchases
```


```python
exploded_salesDF = (spark
    .table("sales")
    .withColumn("item", explode("items"))
)

itemsDF = spark.table("item_lookup")

item_purchasesDF = (exploded_salesDF
    .join(itemsDF, exploded_salesDF.item.item_id == itemsDF.item_id)
)

display(item_purchasesDF)
```

**Pivot**

```sql
SELECT *
FROM (SELECT item_id, name, count(item_id) as count_item FROM table_name_item group by item_id, name order by item_id desc) purchases_curated
PIVOT (sum(count_item) for item_id in ("P_FOAM_S", "M_STAN_T"));


SELECT *
FROM item_purchases
PIVOT (
  sum(item.quantity) FOR item_id IN (
    'P_FOAM_K',
    'M_STAN_Q',
    'P_FOAM_S',
    'M_PREM_Q',
    'M_STAN_F',
    'M_STAN_T',
    'M_PREM_K',
    'M_PREM_F',
    'M_STAN_K',
    'M_PREM_T',
    'P_DOWN_S',
    'P_DOWN_K')
)
```

```python
transactionsDF = (item_purchasesDF
    .groupBy("order_id", 
        "email",
        "transaction_timestamp", 
        "total_item_quantity", 
        "purchase_revenue_in_usd", 
        "unique_items",
        "items",
        "item",
        "name",
        "price")
    .pivot("item_id")
    .sum("item.quantity")
)
display(transactionsDF)

```

### SQL Functions and Control Flow 

**SQL user-defined functions:**    
 - Persist between execution environments  
 - Exist as objects in the metastore and are governed by the same Table ACLs as databases, tables or views.  
 - Require **USAGE**and **SELECT**permision to use the SQL UDF  
 - These functions are registered natively in SQL and maintain all of the optimizations of Spark when applying custom logic to large datasets.  
 - We can use **DESCRIBE FUNCTION**to see where a function was registerd and basic information about expected inputs and what is returned   


**CASE WHEN**
```sql
CREATE OR REPLACE FUNCTION item_preference(name STRING, price INT)
RETURNS STRING
RETURN CASE 
  WHEN name = "Standard Queen Mattress" THEN "This is my default mattress"
  WHEN name = "Premium Queen Mattress" THEN "This is my favorite mattress"
  WHEN price > 100 THEN concat("I'd wait until the ", name, " is on sale for $", round(price * 0.8, 0))
  ELSE concat("I don't need a ", name)
END;

SELECT *, item_preference(name, price) FROM item_lookup

```

### Python User-Defined Fuinctions

**UDF**  
User Defined Functions allow users to define their own transformations on Spark DataFrames
- Can´t be optimized by Catalyst Optimizer  
- Function is serialized ans sent to executors  
- Row data is deserializd FROM Spark´s native binary format to pass to the UDF, and the results are serialized back into Spark´s native format.  
- For Python UDF´s additional interprocess communication overhead between the executor and a Python interpreter running on each worked node.  


**Python-functions**

```
def first_letter_function(email):
    return email[0]

first_letter_function("annagray@kaufman.com")
```

Create apply UDF, register the function as a UDF. This serializes the function and sends it to executors to be able to transofrm DataFrame records.


`first_letter_udf = udf(first_letter_function)`

So once you create a UDF functions you would pass FROM a Python function to a Pyspark function


```
FROM pyspark.sql.functions import col
display(sales_df.SELECT(first_letter_udf(col("email"))))
```

**How to make a Register UDF function availabe in SQL ?**

Using `spark.udf.register`


```
sales_df.createOrReplaceTempView("sales")
first_letter_udf = spark.udf.register("sql_udf", first_letter_function)
display(sales_df.SELECT(first_letter_udf(col("email"))))
```

**UDF with decoratos**

```
@udf("string")
def first_letter_udf_decorator(email: str) -> str:
    return email[0]
```
**Pandas UDF**  
Are special types of UDFs that use the power of the `pandas` library withing a Spark DataFrame operation, Here are the advantages of using `pandas UDFs` over normal UDFs:

+  **Performance:** Traditional UDFs operate row-by-row, in contrast pandas UDFs work on batches of rows and ulithe the perfomrance optimization inherent to pandas operatiosn which are oftern implemente in C underneath.

+  **Memory management:** Allow for more efficient memory usage because they use `Arrow` for data serialization

+ Uses **Apache Arrow:**, an in-memory columnar data format that is used in Spark to efficiently transfer data between JVM and Python processes with near-zero (de)serializationcosts

```
import pandas as pd
FROM pyspark.sql.functions import pandas_udf

# We have a string input/output
@pandas_udf("string")
def vectorized_udf(email: pd.Series) -> pd.Series:
    return email.str[0]
```

We can alsro register Pandas UDF to the SQL namespaces

`spark.udf.register("sql_vectorized_udf", vectorized_udf)`


### Higher Oder Functions in Spark SQL -- SparkSQL Built-in Functions

They use indeed use the "optimizer Catalyst" unlike UDF functions.

- `FILTER()` filters an array using the given lambda function.  
- `EXIST()` tests whether a statement is true for one or more elements in an array.  
- `TRANSFORM()` uses the given lambda function to transform all elements in an array.  
- `REDUCE()` takes two lambda functions to reduce the elements of an array to a single value by merging the elements into a buffer, and the apply a finishing function on the final buffer.  


```
SELECT
    items,
    FILTER (items, i -> i.item_id LIKE "%K") AS king_items
FROM sales
````

```
SELECT items,
  TRANSFORM (
    items, i -> CAST(i.item_revenue_in_usd * 100 AS INT)
  ) AS item_revenues
FROM sales limit 3
```

```
SELECT 
    items,
    EXISTS(SELECT 1 WHERE regexp_replace(CAST(items.item_name as STRING), '\\[|\\]', '') LIKE '%Mattress') AS mattress,
    EXISTS(SELECT 1 WHERE regexp_replace(CAST(items.item_name as STRING), '\\[|\\]', '') LIKE '%Pillow') AS pillow
FROM sales 
LIMIT 3;
```

**Summarize Functions**:  

- **SparkSQL Built-in Functions:** They are natively integrated into Spark´s Catalyst optimizer, that will optimize the execution plan for these operations,
ensuring efficient processing. This is one reason why using built-in functions is often faster thatn using custom UDF´s.

- **User Defined Functions(UDFs):** When you create a UDF, Spark´s Catalyst optimizer doesnt´t have visibility into the logic of the function, meaning it can´t optimize it as
 effectively as built-in functions.
 
- **pandas UDFs:** As an intermediary step, pandas UDFs(or vectorized UDFs) allow for more efficient processing than tradicitonal UDFs since they operate on batches of data using
pandas which is inherently more optimized thatn row-by-row operations.

So whenever possible, it´s recommended to utilize SparkSQL´s built-in functions to benefit FROM the full optimization capabilities of the Catalyst engine.







```
OPTIMIZE students
ZORDER BY id

DESCRIBE HISTORY students
```

**Roll Back and Versions**

```
SELECT * FROM students c WHERE c.id not in (SELECT a.id 
FROM (SELECT * FROM students  VERSION AS OF 3) a
INNER JOIN (SELECT * FROM students VERSION as OF 7) b
on a.id = b.id)

DELETE FROM students
RESTORE TABLE students TO VERSION AS OF 8
```

The Idea here is that when we have a error in a SQL command there is not a way to just continue as we can do in Python, so my Idea is 
take the advantages of "try", "except" of Python and combine it with the SQL code that I wanted to insert.

```
# that would fail --> cause drop doesnt admit Rollback
queries_fail1 = [
    "DROP TABLE students;",
    "SELECT * FROM students;",
    "RESTORE TABLE students TO VERSION AS OF 8;",
    "SELECT * FROM students;"
]

for query in queries_fail1:
    try:
        spark.sql(query)
    except Exception as e:
        print(f"Query failed: {query}")
        print(f"Error: {str(e)}")
        continue
```


**VACUUM**  Perfoms garbage cleanup on the table directoy. By default, a retention threshold of 7 days will be enforced

**DRY RUN** Allows you to see which files would be deleted by the VACUUM operation without actually deleting them. 
Its essentially a way to preview the effects of the VACUUM operation


```
SET spark.databricks.delta.retentionDurationCheck.enabled = false;
SET spark.databricks.delta.vacuum.logging.enabled = true;


VACUUM beans RETAIN 0 HOURS DRY RUN
```


**CREATE TABLE AS SELECT(CTAS)**  

statements create and populate Delta tables using data retrieved FROM an input query.

```
CREATE OR REPLACE TABLE purchases AS
SELECT order_id AS id, transactions_timestamp, purchase_revenue_in_usd AS price
-- FROM sales
FROM sales_delta;

SELECT * FROM purchases limit 2;
```

**DATE GENERATED ALWAYS**   
Indicates the Column will be a "generated column" (we cannot specify a computation within a table definition without indicating it´s a generated column)

```
CREATE OR REPLACE TABLE purchase_dates (
  id STRING, 
  transactions_timestamp STRING, 
  price STRING,
  date DATE GENERATED ALWAYS AS (
    cast(cast(transactions_timestamp/1e6 AS TIMESTAMP) AS DATE))
    COMMENT "generated based on `transactions_timestamp` column");

SELECT * FROM purchase_dates;
```

**CONSTRAINTS**: A rule applied to a column or sets of columns in a table that restrics the type of data taht can be inserted, ensuring the accuracy and reliability of the data.

```
ALTER TABLE purchase_dates ADD CONSTRAINT valid_date CHECK (date > '2020-01-01');
DESCRIBE EXTENDED purchase_dates; -- show in TBLPROPERTIES
```



**Enrich Tables wit Additiona Info**    
- Using **current_timestamp()**    
- **Input_file_name()**    


```
CREATE OR REPLACE TABLE users_pii
COMMENT "Contains PII"
LOCATION "dbfs:/mnt/dbacademy-datasets/temp/users_pii"
PARTITIONED BY (first_touch_date)
AS
  SELECT *, 
    cast(cast(user_first_touch_timestamp/1e6 AS TIMESTAMP) AS DATE) first_touch_date, 
    current_timestamp() updated,
    input_file_name() source_file
  FROM parquet.`dbfs:/mnt/dbacademy-datasets/data-engineering-with-databricks/v02/ecommerce/raw/users-historical/`;
  
SELECT * FROM users_pii limit 2;
```
**Deep Clone vs Shallow Clone**

**Deep Clone** Full metadata and data copie FROM source table.  
**Shallow clone** Create a copy of table quickly to test out applying changes without the risk of modifying the current table.  

```
CREATE OR REPLACE TABLE purchases_clone
DEEP CLONE purchases
```





## Incremental Data Processing.

**Introduction** 

In previous chapters we have about ELT operations, ETL is more for DWH
ELT for Data Lake, but both have a sense of Batch processing.
To process streaming data (close to real time) we need some new structures  

### 

**DLT vs Stream DLT vs DT**

`DLT`: are specifically designed for scnearios where pipeles are continuosly running and data is constanly being ingested, transformed and validated.  
`DT`: Less frequent batch updates.  
`Stream DLT`: enables real-time.

**DLT and Notebook** When you query a DLT in y notebook that is not attached toa DLT pipeline you are querying the table as its is at that moment, no the live 
streaming version. DLT is not intended for interactive execution ina notebook.

**How much time could preserve the data the DLT ?**
Delta Lake allows for multiple versions of data to co-exist. Every time you modify a dataset, Delta Lake retains a new version of that dataset. This is how Time travel works by keeping multiple version.
But... retention perios matter, if every change is retained idenfinitely you storage usage would grow rapidly, especially in active dataset with frequent modification. 
Thats why Delta Lake allows you to set a retention prediod for how long to keep old versionof th data.



**Auto Loader**
- When you have data landing in cloud storage continuously or in upredictable intervals. Instead of scheduling periodic scans of the entiredirectofy,
Auto Loader will automatically pick up an process just the new data as it arrives, making the ingestion process more timely and cost-effective.  
-Auto Loader incrementally ingests new data files in batches. 
- Intern use Spark Structrued Streaming.  
- The inclusion of format("cloudFiles") enables the use of Auto Loader.

```
(streaming_df = spark.readStream.format("cloudFiles")
.option("cloudFiles.format", "json")
.option("cloudFiles.schemaLocation", schemaLocation)
.load(sourcePath))
```
´´´
spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "parquet")
        .option("cloudFiles.schemaLocation", "dbfs:/mnt/demo/orders_checkpoint")
        .load(f"{dataset_bookstore}/orders-raw")
      .writeStream
        .option("checkpointLocation", "dbfs:/mnt/demo/orders_checkpoint")
        .table("orders_updates")
)
´´´

**COPY INTO** Provides SQL engineers and idempotent option to incrementally ingest data form external systems.  

**COPY INTO vs Auto Loader**  

**copy into**: Thousand of files, less efficient at scale  
**Auto Loader**: Millions of Files, efficient at scale.  --> its always active and lisening so obviously would cost much more money

### Tiggers

**Fixed Interval Micro-batches**

`(.trigger(Trigger.ProcessingTime(interval)))`

- This option allows you to process the data at fixed time intervals, regardless of when the data arrived.  
- Interval could be a string like "1 minute" or a duration in milliseconds.  
- Use Case: When you want regular, predictable processing intervals, like processing every 10 minutes.  

```
FROM pyspark.sql.streaming import Trigger

(spark.table("your_table")
.writeStream
.format("delta")
... # other configurations
.trigger(Trigger.ProcessingTime("1 minute"))
.table("output_table"))
```

**Once Trigger**

`(.trigger(Trigger.Once()))`

- Processes the available data in the stream just once and then stops the query.  
- Use Case: When you have a backlog of data and you want to process it once to bring your output table up to date.  

```
FROM pyspark.sql.streaming import Trigger

(spark.table("your_table")
.writeStream
.format("delta")
... # other configurations
.trigger(Trigger.Once())
.table("output_table"))
```


**Continuous Processing**

`.trigger(Trigger.Continuous(interval)))`

- This option will continuously process the data with a low-latency.
- Interval specifies the checkpoint interval.  
- Note: Continuous processing is an experimental feature and has some limitations.
- Use Case: When low-latency is more important than throughput and you need near real-time processing.

```
FROM pyspark.sql.streaming import Trigger

(spark.table("your_table")
.writeStream
.format("delta")
... # other configurations
.trigger(Trigger.Continuous("1 second"))  # e.g., checkpoint every second
.table("output_table"))
```

**Available Now (using trigger(availableNow=True))**

This is a Databricks-specific trigger. When set to True, it will only process the data that's available right now and will not wait for new data.
Use Case: When you want to clear the existing backlog of data without waiting for new data to arrive.

```
(spark.table("your_table")
.writeStream
.format("delta")
... # other configurations
.trigger(availableNow=True)
.table("output_table"))
```
### Medallon Architecture

**Medallon Architecture**   `raw`----->`Bronze`-->`Silver`-->`Gold`--> Consume/Dashboard

`Bronze:` This is often the raw, unrefined layer. Data lands in the bronze layer as it arrives. It's the most granular form of the data and is often not suitable for direct
querying due to inconsistencies, missing values, or its verbose nature. The "streaming live" designation means data is continuously streamed into this layer in real-time.

`Silver:` This is the cleaned and enriched version of the bronze layer. It may undergo operations like filtering, formatting, joining with other datasets,
or even some aggregations. Again, the "streaming live" designation means data FROM the bronze layer is being continuously processed and streamed into the silver layer in real-time.

`Gold:` This layer is optimized for consumption, often by business users. It might contain aggregated data, pre-joined datasets, 
or data reshaped into a specific format ideal for BI tools or final consumption. The data in this layer may not need to be updated in real-time, which is why it's a
"live" table without the streaming aspect. This could mean the Gold layer is built in periodic batches FROM the Silver layer, rather than as a continuous stream.
It provides a snapshot that is updated less frequently, which might be preferable for some reporting or analysis tasks.

```
CREATE OR REFRESH STREAMING LIVE TABLE bronze_table
AS SELECT * FROM cloud_files(some_path)
							 
-- Silver

CREATE OR REFRESH STREAMING LIVE TABLE silver_table (
AS
  SELECT some_columns 
  -- some new columns/transformations
  FROM STREAM(LIVE.bronze_table) 

-- gold
CREATE OR REFRESH LIVE TABLE Gold_table

AS
  SELECT some_columns
  -- some aggregations and 
  FROM LIVE.silver_table
```

**Why does the gold table read FROM "LIVE.silver_table" and not FROM "STREAM(LIVE.silver_table)"?**  

This aligns with the above explanation. The "Gold" layer doesn't necessarily operate on a real-time stream FROM the "Silver" layer.
Instead, it might operate on periodic batches or snapshots FROM the "Silver" layer. By reading FROM "LIVE.silver_table", 
it's essentially working with the current state of the "Silver" table. On the other hand, using "STREAM(LIVE.silver_table)"
would imply real-time, continuous processing of the data FROM the "Silver" layer, which might not be the intention for the "Gold" layer in your architecture.

In summary, the distinction between "streaming live" and "live" and the choice of reading methods represents different stages of data refinement
and the associated processing cadence.


**Can a table that have been create as `CREATE OR REFRESH STREAMING LIVE TABLE silver_table` be later reference as LIVE.silver_table ?**

Yes, once a STREAMING LIVE TABLE is created in Databricks, it acts like a Delta table with a continuously updating view of the data.
The underlying data is stored in Delta format, and you can query it like any other table in Databricks using the LIVE keyword.

The STREAM(LIVE.<table_name>)  syntax is used when you want to treat the table as a streaming source and operate on it in a streaming fashion.
So:

- When you declare a table using CREATE OR REFRESH STREAMING LIVE TABLE, it sets up a continuous ingestion process to keep updating that table with new data.
- When you query this table using SELECT ... FROM LIVE.<table_name>, you're querying its current state, getting a snapshot of the table as it is at the time of the query.

When you use the table in another streaming context with STREAM(LIVE.<table_name>), you're setting up another streaming operation on top of the continuously updating table.
Therefore, even if a table is created as a STREAMING LIVE TABLE, you can indeed query it just like a LIVE table.



**Scenario of Live Table and Stream Live Table**



**STREAM Real-time Fraud Detection:**

**Scenario:**  

Imagine a bank that offers online banking services to its customers. With millions of transactions occurring every day,
it's critical for the bank to quickly identify potentially fraudulent transactions to protect its customers.

**Stream Table Use:**  
- The bank sets up a streaming system where every transaction is instantly sent to a stream table. 
- As each transaction comes in, it's analyzed in real-time against a set of rules or machine learning models to identify if it looks suspicious.  
- If a transaction is deemed suspicious, an alert is generated, and the bank can take immediate action, such as blocking the transaction, notifying the customer,flagging it for further investigation.  

**Why Not Batch Processing?**  
If the bank used batch processing, they'd collect transactions over a set period (e.g., an hour or a day) and then analyze them all at once. 
The problem with this approach in the fraud detection scenario is the delay.

A fraudulent transaction might not be detected until the batch is processed, which could be hours after the transaction occurred. By that time:

The fraudster may have already caused significant financial damage.  
The actual customer may face inconvenience if, for example, their card is used elsewhere or they check their account and find unauthorized transactions.  
The bank might face reputational damage and potential financial liabilities.
  
*Conclusion:*  
For scenarios like fraud detection, where instant response is crucial, stream tables and real-time processing are essential. Batch processing, due to its inherent delay, would not be suitable for such time-sensitive applications.



**Live Table Example: E-Commerce Inventory Management**  

An e-commerce platform wants to maintain an up-to-date inventory of products. This inventory is affected by new stock arrivals, product returns, and products being sold.

**Why a Live Table?:**

- **Frequent Updates:** Stock levels can be influenced by a multitude of factors such as sales, returns, and new shipments.

- **Query Definition Updates:**   Sometimes the e-commerce platform might want to change the logic of how it calculates available inventory.
For instance, they might decide to keep a buffer stock and not show it to customers. 
With a live table, any change in the logic will be reflected in the table without the need for manual adjustments.

- **Instant Reflection:**  If there's an error or update in the source data (maybe a returned item was mistakenly marked as 'damaged' when it wasn't), correcting this in the source will instantly reflect in the live table.

**How to use DLT** 

- Declare in notebooks
- Workflows in Delta Live Tables + start

**What are the differences between development and producdtion in DLT, what are teh best practices ?**

Development Mode: 
- re-use  
- long-running cluster  
- running forfast iteration  
- No retries on errorrs enabling faster debugging  

Production mode:  
- Cuts costs by turning off clusters as soon as they are done  
- Escalating retries, including cluster restarts `ensure reliability`  

**What is Automated Data Management ?

refers to the ability of DLTs to automatically optimizes data for performance & ease-of-use

**Best Practices**DLT encodes Delta best practices automatically when creating DLT: `optimizerWrite`, `AutoCompact`, `tuneFileSizesForRewrites`  
**Physical Data**DLT automatically manages your physical data to minimice cost and optimize performance --> runs vacuum, run optimize   
**Schema Evolution**Schema evolution is handle for owner  


**Metastore** 
Metastore keeps track of all the table metadata, like the schema and the location of the data. When you create a table in Delta Lake or DAtabricks, the details bout the table,
including where its data is stored, are saved in the metastored.

**Table directory** 
In a concern of distributed file storage systems, a table directory typically refers to the underlying location in the distributed storage
where the data is stored. Referring to: Location, Physical Files, Metadata and Logs. For example consider a Delta Lake table saved in a Azure Data Lake Storage(ADLS).
The table directory could be a path like `abfss://my-data-lake-container@mydatalakeaccount.dfs.core.windows.net/my-delta-table/` whithn this directory, you´d find 
multiple Parquet Files and Transaction Logs. `_delta_log`  

**Event Log**
Event log is about logging events or changes. In context of Delta Lake, the Event Log keeps track of transactions but doesn´t serve as a direct way to
view the contents of the table directory. Are desing to capure various acxtivities.

**Checkpointing directory**Checkpointing typically refers to a mechanism that saves the state of a stream at regular intervals, ensuring fault-tolerance for streamimg operations.

**What DAG primarily does?**
DAG visualizes the sequence and dependencies of taks. There you can go to the Pipeline Details page and click on the individual tables.  

**Task Details**Typically provide information about the task´s execution, status, duration.	

**Workflow vs Pipeline**  
Task orchestration = Workflow  
Data transofrmation and movement (pipeline)

**Flow Definition** 
In a ETL concept Flow definition is how our data is beeing transformated by the following steps we are using for the ETL.
In visual tools like Azure Data Factory, Apache NiFi, or Talend, the flow definition might be represented visually as a flowchart or diagram where you can see
how different data sources, transformations, and destinations (sinks) are connected. By examining this visual representation, 
you can understand how data is flowing and being transformed.

In a more code-based environment, or if you're using something like Databricks notebooks, the flow definition might be best understood by examining the sequence of SQL queries,
Python transformations, or other code snippets. For example, seeing a sequence of SQL queries that extract data FROM Table A, transform it, and then insert it into Table B.

**Workflow orchestration patterns.**

- **Fan-out Pattern:**A single task or job is followed by multiple tasks that can be executed in parallel  
- **Funnel Pattern**Multiple task or jobs that run in parallel are followed by a single tas that stgart afther all parallel task completed  
- **Hourglas Pattern**Combine Fan-out and Funnel
- **Sequence Pattern**Task or jobs are organized in a sgtrict sequence, where each task starts only after the previous one has completed.
- **Multi-sequence Pattern**Multi sequences of task that can run in parallel with each other.

  

**Job Runs Page**: Provide a detailed overview of all the jobs executed, including those FROM DLT pipelines.
Clicking on individual tables or task within a job run will providespecifics bout that task.

**Databricks Tables**Allows you to create tables which are essentially metadata definitions on top of your data. These tables can point to data stored in various formats like 
parquet, Avro, CSV, JSON, etc...  

**Storage Systems**Databricks can be integrated with different distributed storage systems like Azure Blob Storage, Azure Data Lake, AWS S3 and more.

**Delta Live Tables come to action

**Agility**: Build batch and streaming data pipelines.
**Trust your data**Quality controls with expectations and actions to take
**Scale with reliability**Easy scale.


### Delta Live Tables

**DAG
- execution flow is graphed
- The results are reported in the **Data Quality**section
- With each triggered update, all newly arriving data will be processed through your pipeline. Metrics will always be reported for current run.

```
@dlt.table(comment = "Python comment",table_properties = {"quality": "silver"})

COMMENT "SQL comment" TBLPROPERTIES ("quality" = "silver")
```


** Exploring the Results of a DLT Pipeline


DLT uses Delta Lake to store all tables, each witme a query is executed, we will always return the most recent version of the table. But queries outside of DLT.  
But queries outside of DLT will return snapshot results FROM DLT tables, regardless of how they were defined.


### Pipeline Event Logs

- See Latest Update ID: In many cases, you may wish to gain updates about the latest update to your pipeline.

```
latest_update_id = spark.sql("""
    SELECT origin.update_id
    FROM event_log_raw
    WHERE event_type = 'create_update'
    ORDER BY timestamp DESC LIMIT 1""").first().update_id

print(f"Latest Update ID: {latest_update_id}")

# Push back into the spark config so that we can use it in a later query.
spark.conf.set('latest_update.id', latest_update_id)

```

**Examine Lineage

- DLT provides built-in lineage information for how data flows through your table.

While the query below only indicates the direct predecessors for each table, this information can easily be combined to trace data in any table back to the point it entered the lakehouse

```
SELECT details:flow_definition.output_dataset, details:flow_definition.input_datasets 
FROM event_log_raw 
WHERE event_type = 'flow_definition' AND 
      origin.update_id = '${latest_update.id}'
```


**Examine Data Quality Metrics

```
%sql
SELECT row_expectations.dataset as dataset,
       row_expectations.name as expectation,
       SUM(row_expectations.passed_records) as passing_records,
       SUM(row_expectations.failed_records) as failing_records
FROM
  (SELECT explode(
            FROM_json(details :flow_progress :data_quality :expectations,
                      "array<struct<name: string, dataset: string, passed_records: int, failed_records: int>>")
          ) row_expectations
   FROM event_log_raw
   WHERE event_type = 'flow_progress' AND 
         origin.update_id = '${latest_update.id}'
  )
GROUP BY row_expectations.dataset, row_expectations.name

```


### Creating and Governing Data with UC

**Unity Catalog´s**three-level namespace
`SELECT * FROM mycatalog.myschema.mytable;`

This can be handy in many use cases.

* Separating data relating to business units within your organization (sales, marketing )
* Satisfying SDLC requirements (dev, staging, prod, etc)
* Establishing sandboxes containing temporary datasets for internal use


**Create and use Catalog

```
CREATE CATALOG IF NOT EXISTS ${DA.my_new_catalog}

USE CATALOG ${DA.my_new_catalog}


CREATE SCHEMA IF NOT EXISTS example;
USE SCHEMA example

```

**Grant access to datga objects

```
GRANT USAGE ON CATALOG ${DA.my_new_catalog} TO analysts;
GRANT USAGE ON SCHEMA example TO analysts;
GRANT SELECT ON VIEW agg_heartrate to analysts
```

**Dynamic Views

+ Provide the ability to do fine-grained access control


Governing Data techniques

- Redacted
- Restric rows
- Data masking

```

CREATE OR REPLACE VIEW agg_heartrate AS
SELECT
  CASE WHEN
    is_account_group_member('analysts') THEN mask(mrn)
    ELSE mrn
  END AS mrn,
  time,
  device_id,
  heartrate
FROM heartrate_device
WHERE
  CASE WHEN
    is_account_group_member('analysts') THEN device_id < 30
    ELSE TRUE
  END;

-- Re-issue the grant --
GRANT SELECT ON VIEW agg_heartrate to analysts


```

**Explore objects

```
SHOW TABLES
SHOW VIEWS
SHOW SCHEMAS
SHOW CATALOGS
```


**Explore permisions


```

SHOW GRANTS ON VIEW

SHOW GRANTS ON TABLE

SHOW GRANTS ON SCHEMA

SHOW GRANTS ON CATALOG

```


**Revoke Access

`REVOKE EXECUTION ON FUNCTION mask FROM analysts`

## Data Engineer Associate Udemy

**Code**

```
CREATE SCHEMA IF NOT EXISTS Juanito;

USE Juanito;

CREATE TABLE IF NOT EXISTS Juanito.employees
  (id INT, name STRING, salary DOUBLE);

INSERT INTO Juanito.employees
VALUES 
  (1, "Adam", 3500.0),
  (2, "Sarah", 4020.5),
  (3, "John", 2999.3),
  (4, "Thomas", 4000.3),
  (5, "Anna", 2500.0),
  (6, "Kim", 6200.3)
;
SELECT * FROM Juanito.employees;


DESCRIBE DATABASE EXTENDED Juanito;

DESCRIBE EXTENDED Juanito.employees;

DESCRIBE DETAIL Juanito.employees;

DESCRIBE HISTORY Juanito.employees;

SELECT * FROM Juanito.employees@v1;


OPTIMIZE employees
ZORDER BY id

VACUUM employees

VACUUM employees RETAIN 0 HOURS
SET spark.databricks.delta.retentionDurationCheck.enabled = false;



DROP TABLE external_default;

```

External Tables will need to use `LOCATION`

```

USE new_default;

CREATE TABLE managed_new_default
  (width INT, length INT, height INT);
  
INSERT INTO managed_new_default
VALUES (3 INT, 2 INT, 1 INT);

-----------------------------------

CREATE TABLE external_new_default
  (width INT, length INT, height INT)
LOCATION 'dbfs:/mnt/demo/external_new_default';
  
INSERT INTO external_new_default
VALUES (3 INT, 2 INT, 1 INT);

```



View will be st as Table but Temp View not.


```sql
CREATE VIEW view_apple_phones
AS  SELECT * 
    FROM smartphones 
    WHERE brand = 'Apple';
	
SHOW TABLES;

CREATE TEMP VIEW temp_view_phones_brands
AS  SELECT DISTINCT brand
    FROM smartphones;

SELECT * FROM temp_view_phones_brands;


CREATE GLOBAL TEMP VIEW global_temp_view_latest_phones
AS SELECT * FROM smartphones
    WHERE year > 2020
    ORDER BY year DESC;
	
SHOW TABLES IN global_temp;

DROP TABLE smartphones;
DROP VIEW view_apple_phones;
DROP VIEW global_temp.global_temp_view_latest_phones;

```

## ETL With Spark and Python

```python
dataset_bookstore = 'dbfs:/mnt/demo-datasets/bookstore'
spark.conf.set(f"dataset.bookstore", dataset_bookstore)
files = dbutils.fs.ls(f"{dataset_bookstore}/customers-json")
```



```sql
-- input_file_name and time_s
 SELECT email,
    input_file_name() source_file,
    cast(current_timestamp() as DATE) day_of_insertion
  FROM json.`${dataset.bookstore}/customers-json` limit 3;
  

```


Reading FROM Binaty, CSV, text

```
SELECT * FROM text.`${dataset.bookstore}/customers-json` limit 3

SELECT * FROM binaryFile.`${dataset.bookstore}/customers-json`

SELECT * FROM csv.`${dataset.bookstore}/books-csv`

CREATE OR REPLACE TABLE orders AS
SELECT * FROM parquet.`${dataset.bookstore}/orders`
```


```
DROP TABLE IF EXISTS books_csv;

CREATE TABLE  if not exists books_csv
  (book_id STRING, title STRING, author STRING, category STRING, price DOUBLE)
USING CSV
OPTIONS (
  header = "true",
  delimiter = ";"
)
LOCATION "${dataset.bookstore}/books-csv";

SELECT count(*) FROM books_csv;


%python
(spark.read
        .table("books_csv")
        .write
        .mode("append")
        .format("csv")
        .option('header', 'true')
        .option('delimiter', ';')
        .save(f"{dataset_bookstore}/books-csv")
		
SELECT count(*) FROM books_csv; -- the same as previous


REFRESH TABLE books_csv;
SELECT COUNT(*) FROM books_csv;  --> retrun the actual status, External data will need to be refreshed, that does not happend with Delta Tables.
``

```
CREATE OR REPLACE FUNCTION get_url(email STRING)
RETURNS STRING
RETURN concat("https://www.", split(email, "@")[1]);

-- In that case we cann apply the function directly without use TRANSFORM cause we have just one record in our  cell
SELECT email, get_url(email) domain
FROM customers

```


















## Unity Catalog



### Data Governance models

Programmatically grant, deny and revoke access to ata objects

example: `GRANT SELECT ON TABLE my_table TO user@mycopany.com`

**Data Objects**: CATALOG, SCHEMA, TABLE, VIEW, FUNCTION, ANY FILE
**Privilege**: SELECT, MODIFY, CREATE, READ_METADATA, USAGE, ALL_PRIVILEGES
**Operations**: GRANT, DENY, REVOKE



Granting Privileges by Role

**Databricks administgrator**All objects in the catalog and the underlying filesystem.  
**Catalog owner**: All objects in the catalog.
**Database owner**: All objects in the database.
**Table owner**: Only the table.



## Data Access Control and Unity Catalog
------------------------------------------------------

### Theorie

**Unity Catalog**: Centralized and managed metastore that provides a unified way to manage, discover and govern data across multiple workspaces.  
**Data Access Control**: Control who has access to which data.  
**Data Access Audit**: Capture and record all access to data.  
**Data Lineage**: Capture upstream sources and downstream --> refers to the process of tracking and understanding data flow and dependencies within a data pipeline or system.   
&nbsp;&nbsp;&nbsp;&nbsp;**Upstream sources**refers to the origins of datga ow where data comes FROM.    
&nbsp;&nbsp;&nbsp;&nbsp;**Downstream**refers where the data go ather being processed or transformed.  


**Challenges in the Data Lake**
&nbsp;&nbsp;&nbsp;&nbsp;No fine-grained access controls   
&nbsp;&nbsp;&nbsp;&nbsp;No common metadata layer  
&nbsp;&nbsp;&nbsp;&nbsp;Non-standar cloud-specific governance model  
&nbsp;&nbsp;&nbsp;&nbsp;Hard to audit  
&nbsp;&nbsp;&nbsp;&nbsp;No common governance model for different data asset types.  

**Unity Catalog**
&nbsp;&nbsp;&nbsp;&nbsp;Unify governance across clouds --> Fine-grained governance for data lakes across clouds - based on open standard ANSI SQL.    
&nbsp;&nbsp;&nbsp;&nbsp;Unify data and AI assets --> Centrally share, audit, secure and manage all data types with one simple interface.   
&nbsp;&nbsp;&nbsp;&nbsp;Unify existing catalogs --> Works in concert with existing data, storage and catalogs - no hard migration required.  


**Key Concepts**
&nbsp;&nbsp;&nbsp;&nbsp;**Metastore elements**![](img/Metastore_Elements.PNG)  
&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;**Three-level Namespace**![](img/Three_Level_Namespace.PNG)  
&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;**Before and after unity Catalog**![](img/Before_After_Unity_Catalog.PNG)  
&nbsp;&nbsp;&nbsp;&nbsp;



**Unity Catalog Roles**

&nbsp;&nbsp;&nbsp;&nbsp;**Cloud Administrator**Administer underlying cloud resources   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Storage accounts/buckets   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- role/service Principals/Managed Identities.     


&nbsp;&nbsp;&nbsp;&nbsp;**Identity Administrator**Administer underlying identity   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Identity provider provision users and groups into the account  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Avoids need to manually create and manage identities  


&nbsp;&nbsp;&nbsp;&nbsp;**Account Administrator**Administer the account  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Creates, deletes and assigns metastores to workspaces  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Creates, deletes and assigns users and groups to workspaces  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Integrates account with an identity provider  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Full access to all data objects  

&nbsp;&nbsp;&nbsp;&nbsp;**Metastore Administrator**Administer the metastore    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Creates and drops catalogs and other data objects  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Grant privileges on data objects  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Changes ownership of data objects  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Designated by an account administrator  

&nbsp;&nbsp;&nbsp;&nbsp;**Data Owner**Owns data objects they created  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Creates nested objects  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Grant privileges to others on owned objects  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Changes ownership of owned objects  


&nbsp;&nbsp;&nbsp;&nbsp;**Workspace Administrator**Administer a workspace  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Manage permissions on workspace assets  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Restricts access to cluster creation  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Add or remove users  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Elevate users permissions  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Grant privileges to others  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Change job ownership  


**Identities**

&nbsp;&nbsp;&nbsp;**User**
&nbsp;&nbsp;&nbsp;**Account administrator**
&nbsp;&nbsp;&nbsp;**Service Principal + Service Principal with administrative privileges**
&nbsp;&nbsp;&nbsp;**Groups** analyst, developers  

**Security Model** 
![](img/Security_Model.PNG)  


**Cluter Security Model** 
![](img/Cluster_Security_Model.PNG)  

**Matrix Security Model** 
![](img/Matrix_Security_Model.PNG)  

**Security Model Principals Privileges Securables** 
![](img/Principals_Privileges_Securables_Security_Model.PNG)

**Dynamic Views**
![](img/Dynamic_Views.PNG)


**Storage Credentials and External Locations**

![](img/Credentials_External_Locations.PNG)

**Identity Federation**Typically means integrating an exernal identitiy provider to allow for a single source of truth for user identities and a more streamline authentication process.

**Delta Sharing**Open protocol for sharing data across organizations in a secure and governed manner, regardless of which platform they are using.






