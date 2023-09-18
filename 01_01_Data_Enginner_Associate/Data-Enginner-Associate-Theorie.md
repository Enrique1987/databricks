


## ETL with Spark SQL and Python

### External Table

- Location need to be added
- We cannot expect the performance guarantees associated with Delta Lake, example with DT you always guery the most recent version of your source data but it
it could not be the case with external tables.


### External Tables: Querying Files Directly

**Python**

```
events_kafka = "dbfs:/mnt/path/"
files = dbutils.fs.ls(events_kafka)
display(files)


data_path = "dbfs:/mnt/my_path//001.json"
data_json = spark.sql(f"SELECT * FROM json.`{data_path}`")
display(data_json)


sales_csv_path = "dbfs:/mnt/my_path/"
display(spark.sql(f"select * from csv.`{sales_csv_path}`"))

```

### External Tables: Querying different types of data

`json` `text` `binaryFile` `csv`



```

CREATE OR REPLACE VIEW event_view
AS SELECT * FROM json.`dbfs:/mnt/my_path/`

CREATE OR REPLACE TEMP VIEW events_temp_view
AS SELECT * FROM json.`dbfs:/mnt/my_path/`

SELECT * FROM text.`dbfs:/mnt/my_path/`

SELECT * FROM binaryFile.`dbfs:/mnt/my_path/`

SELECT * FROM csv.`dbfs:/mnt/my_path/`

```

### External Tables - Providing Options for External Sources

**SQL**
```
DROP TABLE IF EXISTS books_csv;

CREATE TABLE  if not exists books_csv
  (book_id STRING, title STRING, author STRING, category STRING, price DOUBLE)
USING CSV
OPTIONS (
  header = "true",
  delimiter = ";"
)
LOCATION "${dataset.bookstore}/books-csv"

```

**Python**
```
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

- Convert a external location in a DELTA table.

```
CREATE TABLE my_delta_table
USING DELTA
LOCATION '/my_path/'
```


**Running `DESCRIBE EXTENDED` on a table will show all of the metadata associate withthe table definition**

`DESCRIBE EXTENDED sales_csv`



### Extracting Data from SQL Databases

```
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

```
assert spark.table("events_json"), "Table named `events_json` does not exist"
assert spark.table("events_json").columns == ['key', 'offset', 'partition', 'timestamp', 'topic', 'value'], "Please name the columns in the order provided above"

assert spark.table("events_json").dtypes == [('key', 'binary'), ('offset', 'bigint'), ('partition', 'int'), ('timestamp', 'bigint'), ('topic', 'string'), ('value', 'binary')], "Please make sure the column types are identical to those provided above"

total = spark.table("events_json").count()
assert total == 2252, f"Expected 2252 records, found {total}"

```

### Cleaning Data



```
from pyspark.sql import functions as F


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
```

```
from pyspark.sql.functions import col


usersDF = spark.read.table("users_dirty")
usersDF.selectExpr("count_if(email IS NULL)")
usersDF.where(col("email").isNull()).count()  
userDF.distinct().count()	  
```

```
from pyspark.sql.functions import max

# remember  usersDF = spark.read.table("users_dirty")

dedupedDF = (usersDF
    .where(col("user_id").isNotNull())
    .groupBy("user_id", "user_first_touch_timestamp")
    .agg(max("email").alias("email"), 
         max("updated").alias("updated"))
    )
dedupedDF.count()
```


#### Validate Datasets

The result should be True or False

**SQL**
```
SELECT max(row_count) <= 1 no_duplicate_ids FROM (
  SELECT user_id, count(*) AS row_count
  FROM deduped_users
  GROUP BY user_id)
 

**Python**
```
from pyspark.sql.functions import count

display(dedupedDF
    .groupby("user_id")
    .agg(count("*").alias("row_count"))
    .select((max("row_count") <= 1).alias("no_duplicate_ids"))) # true or false 
```

#### Date Format and Regex

**SQL**

```
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
**Python**

```
from pyspark.sql.functions import date_format, regexp_extract

display(dedupedDF
    .withColumn("first_touch", (col("user_first_touch_timestamp") / 1e6).cast("timestamp"))
    .withColumn("first_touch_date", date_format("first_touch", "MMM d, yyyy"))
    .withColumn("first_touch_time", date_format("first_touch", "HH:mm:ss"))
    .withColumn("email_domain", regexp_extract("email", "(?<=@).+", 0))
	.select("first_touch", "first_touch_date", "first_touch_time", "email_domain")
)

```

#### Complex Transformations

```

# function to make shallow clone table.

def clone_source_table(table_name, source_path, source_name=None):
    

    source_name = table_name if source_name is None else source_name
    print(f"Cloning the \"{table_name}\" table from \"{source_path}/{source_name}\".", end="...")
    
    spark.sql(f"""
        CREATE OR REPLACE TABLE {table_name}
        SHALLOW CLONE delta.`{source_path}/{source_name}`
        """)
		
data_path_2_5 = "dbfs:/mnt/my_path/"	
clone_source_table("sales", f"{data_path_2_5}/ecommerce/delta", "sales_hist")





df = spark.table("events_raw")
for col, dtype in df.dtypes:
    print(f"{col}: {dtype}")
	


CREATE OR REPLACE TEMP VIEW events_strings AS 
SELECT string(key), string(value) FROM events_raw;

```

#### Work with Nested Data

**Note**: Spark SQL has a built-in functionality to directly interact with nested data stored as JSON string or struct types

Use `:` syntax in queries to access subfiels in JSON strings
Use `.` syntax in queries to access subfiesl in struct types


```
SELECT * FROM events_strings WHERE value:event_name = "finalize" ORDER BY key LIMIT 1


%python
display(events_stringsDF
    .where("value:event_name = 'finalize'")
    .orderBy("key")
    .limit(1)
)

```

Let's use the JSON string example above to derive the schema, then parse the entire JSON column into struct types.

**schema_of_json()** returns the schema derived from an example JSON string.
**from_json()** parses a column containing a JSON string into a struct type using the specified schema.


**SQL**
```
CREATE OR REPLACE TEMP VIEW parsed_events AS SELECT json.* FROM (
SELECT from_json(value, schema_of_json('{"device":"Linux","ecommerce":{"purchase_revenue_in_usd":1075.5,
                                         "total_item_quantity":1,"unique_items":1},"event_name":"finalize",
										 "event_previous_timestamp":1593879231210816,"event_timestamp":1593879335779563,
										 "geo":{"city":"Houston","state":"TX"},
										 "items":[{"coupon":"NEWBED10","item_id":"M_STAN_K","item_name":"Standard King Mattress","item_revenue_in_usd":1075.5,"price_in_usd":1195.0,"quantity":1}],#
										 "traffic_source":"email","user_first_touch_timestamp":1593454417513109,"user_id":"UA000000106116176"}')) AS json 
FROM events_strings);

```

**Python**
```
from pyspark.sql.functions import from_json, schema_of_json

json_string = """
{"device":"Linux","ecommerce":{"purchase_revenue_in_usd":1047.6,"total_item_quantity":2,"unique_items":2},"event_name":"finalize","event_previous_timestamp":1593879787820475,
"event_timestamp":1593879948830076,"geo":{"city":"Huntington Park","state":"CA"},"items":[{"coupon":"NEWBED10","item_id":"M_STAN_Q","item_name":"Standard Queen Mattress",
"item_revenue_in_usd":940.5,"price_in_usd":1045.0,"quantity":1},{"coupon":"NEWBED10","item_id":"P_DOWN_S","item_name":"Standard Down Pillow","item_revenue_in_usd":107.10000000000001,
"price_in_usd":119.0,"quantity":1}],"traffic_source":"email","user_first_touch_timestamp":1593583891412316,"user_id":"UA000000106459577"}
"""
parsed_eventsDF = (events_stringsDF
    .select(from_json("value", schema_of_json(json_string)).alias("json"))
    .select("json.*")
)

display(parsed_eventsDF)

```

#### Manipulate Arrays

**explode()** separates the elements of an array into multiple rows; this creates a new row  for each elemnt.
**size()** provides a count for the number of elements in an array for each row.


**SQL**
```
CREATE OR REPLACE TEMP VIEW exploded_events AS
SELECT *, explode(items) AS item
FROM parsed_events;

SELECT * FROM exploded_events WHERE size(items) > 2



CREATE OR REPLACE TEMP VIEW events_explode AS ( SELECT device, explode(items) AS items FROM events_enrique_table limit 2);

SELECT * FROM events_explode;


CREATE OR REPLACE TEMP VIEW events_external_items AS 
SELECT json.*
FROM (
    SELECT from_json(CAST(items AS STRING), 
        schema_of_json('{"coupon": "NEWBED10", "item_id": "M_STAN_F", "item_name": "Standard Full Mattress", "item_revenue_in_usd": 850.5, "price_in_usd": 945, "quantity": 1}')
    ) AS json 
    FROM events_explode
);

```


**Python**
```
from pyspark.sql.functions import explode, size

exploded_eventsDF = (parsed_eventsDF
    .withColumn("item", explode("items"))
)

display(exploded_eventsDF.where(size("items") > 2))
```




```

**collect_set()** collects unique values for a field, including fields within arrays.  
**flatten()** combines multiple arrays into a single array.  
**array_distinct()** removes duplicate elements from an array.  

**SQL**  
```
SELECT user_id,
  collect_set(event_name) AS event_history,
  array_distinct(flatten(collect_set(items.item_id))) AS cart_history
FROM exploded_events
GROUP BY user_id
```



**python**

```
from pyspark.sql.functions import array_distinct, collect_set, flatten

display(exploded_eventsDF
    .groupby("user_id")
    .agg(collect_set("event_name").alias("event_history"),
            array_distinct(flatten(collect_set("items.item_id"))).alias("cart_history"))		
```


#### Join Tables

**SQL**

```
CREATE OR REPLACE TEMP VIEW item_purchases AS

SELECT * 
FROM (SELECT *, explode(items) AS item FROM sales) a
INNER JOIN item_lookup b
ON a.item.item_id = b.item_id;

SELECT * FROM item_purchases
```


**Python**
```
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

#### Pivot

**SQL**

```
SELECT *
FROM (select item_id, name, count(item_id) as count_item from table_name_item group by item_id, name order by item_id desc) purchases_curated
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


**python**

```
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

SQL user-defined functions:
 - Persist between execution environments  
 - Exist as objects in the metastore and are governed by the same Table ACLs as databases, tables or views.  
 - Require **USAGE** and **SELECT** permision to use the SQL UDF  
 - These functions are registered natively in SQL and maintain all of the optimizations of Spark when applying custom logic to large datasets. 
 - We can use **DESCRIBE FUNCTION** to see where a function was registerd and basic information about expected inputs and what is returned  

`DESCRIBE FUNCTIONS EXTENDED sale_announcement`

```
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

#### UDF

- Can´t be optimized by Catalyst Optimizer
- Function is serialized ans sent to executors
- Row data is deserializd from Spark´s native binary format to pass to the UDF, and the results are serialized back into Spark´s native format.
- For Python UDF´s additional interprocess communication overhead between the executor and a Python interpreter running on each worked node.



```

#Python function

def first_letter_function(email):
    return email[0]

first_letter_function("annagray@kaufman.com")

```
create apply UDF, register the function as a UDF. This serializes the function and sends it to executors to be able to transofrm DataFrame records.

`first_letter_udf = udf(first_letter_function)`

So once you create a UDF functions you would pass from a Python function to a Pyspark function


```

from pyspark.sql.functions import col

display(sales_df.select(first_letter_udf(col("email"))))

```

**How to make a Register UDF function availabe in SQL ?**

Using `spark.udf.register`


```
sales_df.createOrReplaceTempView("sales")

first_letter_udf = spark.udf.register("sql_udf", first_letter_function)

display(sales_df.select(first_letter_udf(col("email"))))

```

#### UDF with decoratos

```

@udf("string")
def first_letter_udf_decorator(email: str) -> str:
    return email[0]
	
	
```


**Apache Arrow**, an in-memory columnar data format that is used in Spark to efficiently transfer data between JVM and Python processes with near-zero (de)serializationcosts

```
import pandas as pd
from pyspark.sql.functions import pandas_udf

# We have a string input/output
@pandas_udf("string")
def vectorized_udf(email: pd.Series) -> pd.Series:
    return email.str[0]
```

We can alsro register Pandas UDF to the SQL namespaces

`spark.udf.register("sql_vectorized_udf", vectorized_udf)`


### Higher Oder Functions in Sapark SQL

- **`FILTER()`** filters an array using the given lambda function.
- **`EXIST()`** tests whether a statement is true for one or more elements in an array. 
- **`TRANSFORM()`** uses the given lambda function to transform all elements in an array.
- **`REDUCE()`** takes two lambda functions to reduce the elements of an array to a single value by merging the elements into a buffer, and the apply a finishing function on the final buffer.

```

SELECT
    items,
    FILTER (items, i -> i.item_id LIKE "%K") AS king_items
FROM sales


SELECT items,
  TRANSFORM (
    items, i -> CAST(i.item_revenue_in_usd * 100 AS INT)
  ) AS item_revenues
FROM sales limit 3


SELECT 
    items,
    EXISTS(SELECT 1 WHERE regexp_replace(CAST(items.item_name as STRING), '\\[|\\]', '') LIKE '%Mattress') AS mattress,
    EXISTS(SELECT 1 WHERE regexp_replace(CAST(items.item_name as STRING), '\\[|\\]', '') LIKE '%Pillow') AS pillow
FROM sales 
LIMIT 3;


## ETL

## MERGE

**target_table**: The table into which you want to merge data.

**source_table**: The table from which you want to insert or update data.

**merge_condition**: The condition to determine a match between the two tables.

**WHEN MATCHED THEN**: Describes how rows from the target table should be updated or deleted if they match rows from the source table.

**WHEN NOT MATCHED THEN**: Describes how rows from the source table should be inserted into the target table if they don't match any rows in the target table.

Inside the **THEN**

**THEN UPDATE SET**

**THEN DELETE**

**THEN INSERT** * 

**SQL**

```

drop TABLE IF exists students;

CREATE TABLE IF NOT EXISTS students
  (id INT, name STRING, value DOUBLE);
  
INSERT INTO students VALUES (1, "Yve", 1.0);
INSERT INTO students VALUES (2, "Omar", 2.5);
INSERT INTO students VALUES (3, "Elia", 3.3);

INSERT INTO students
VALUES 
  (4, "Ted", 4.7),
  (5, "Tiffany", 5.5),
  (6, "Vini", 6.3);

-- That isnstruction doesnt make anything 
UPDATE students 
SET value = value + 1
WHERE name LIKE "T%";

-- That instruction doesnt make anything
DELETE FROM students 
WHERE value > 6;

CREATE OR REPLACE TEMP VIEW updates(id, name, value, type) AS VALUES
  (2, "Omar", 15.2, "update"),
  (3, "", null, "delete"),
  (7, "Blue", 7.7, "insert"),
  (11, "Diya", 8.8, "update");
  
MERGE INTO students b
USING updates u
ON b.id=u.id
WHEN MATCHED AND u.type = "update"
  THEN UPDATE SET *
WHEN MATCHED AND u.type = "delete"
  THEN DELETE
WHEN NOT MATCHED AND u.type = "insert"
  THEN INSERT *;

select * from students;  -- the only conditin that match is the last one and insert the value "blue"
```


#### Describe Extended vs detail vs history

- DESCRIBE EXTENDED for Data types  
- DESCRIBE DETAIL for metadata associate to the Table  
- DESCRIBE HISTORY for the opertions where made in the Table


```

%sql
OPTIMIZE students
ZORDER BY id

DESCRIBE HISTORY students


#### Versions

%sql
SELECT * FROM students c WHERE c.id not in (SELECT a.id 
FROM (select * from students  VERSION AS OF 3) a
INNER JOIN (select * from students VERSION as OF 7) b
on a.id = b.id)



#### Roll Back

```
DELETE FROM students
RESTORE TABLE students TO VERSION AS OF 8
```

The Idea here is that when we have a error in a SQL command there is not a way to just continue as we can do in Python, so my Idea is 
take the advantages of "try", "except" of Python and combine it with the SQL code that I wanted to insert.

# that would fail --> cause drop doesnt admit Rollback
queries_fail1 = [
    "DROP TABLE students;",
    "select * from students;",
    "RESTORE TABLE students TO VERSION AS OF 8;",
    "select * from students;"
]

for query in queries_fail1:
    try:
        spark.sql(query)
    except Exception as e:
        print(f"Query failed: {query}")
        print(f"Error: {str(e)}")
        continue
```

**Using Merge**

```

%sql
drop table if exists beans;
drop View if exists new_beans;
CREATE TABLE beans 
(name STRING, color STRING, grams FLOAT, delicious BOOLEAN);

INSERT INTO beans VALUES
("black", "black", 500, true),
("lentils", "brown", 1000, true),
("jelly", "rainbow", 42.5, false);

INSERT INTO beans VALUES
('pinto', 'brown', 1.5, true),
('green', 'green', 178.3, true),
('beanbag chair', 'white', 40000, false);

UPDATE beans
SET delicious = true
WHERE name = "jelly";

UPDATE beans
SET grams = 1500
WHERE name = 'pinto';

DELETE FROM beans
WHERE delicious = false;

CREATE OR REPLACE TEMP VIEW new_beans(name, color, grams, delicious) AS VALUES
('black', 'black', 60.5, true),
('lentils', 'green', 500, true),
('kidney', 'red', 387.2, true),
('castor', 'brown', 25, false);

MERGE INTO beans a
USING new_beans b
ON a.name=b.name AND a.color = b.color
WHEN MATCHED THEN
  UPDATE SET grams = a.grams + b.grams
WHEN NOT MATCHED AND b.delicious = true THEN
  INSERT *;
  
```

#### VACUUM 
Perfoms garbage cleanup on the table directoy. By default, a retention threshold of 7 days will be enforced

**DRY RUN** allows you to see which files would be deleted by the VACUUM operation without actually deleting them. Its essentially a way to preview the effects of the VACUUM operation


```
SET spark.databricks.delta.retentionDurationCheck.enabled = false;
SET spark.databricks.delta.vacuum.logging.enabled = true;


VACUUM beans RETAIN 0 HOURS DRY RUN

```


**`CREATE TABLE AS SELECT(CTAS)`** statements create and populate Delta tables using data retrieved from an input query.

```
CREATE OR REPLACE TABLE purchases AS
SELECT order_id AS id, transactions_timestamp, purchase_revenue_in_usd AS price
-- FROM sales
FROM sales_delta;

SELECT * FROM purchases limit 2;

```
**Generate always**

CREATE OR REPLACE TABLE purchase_dates (
  id STRING, 
  transactions_timestamp STRING, 
  price STRING,
  date DATE GENERATED ALWAYS AS (
    cast(cast(transactions_timestamp/1e6 AS TIMESTAMP) AS DATE))
    COMMENT "generated based on `transactions_timestamp` column");

SELECT * FROM purchase_dates;



SET spark.databricks.delta.schema.autoMerge.enabled=true; 

MERGE INTO purchase_dates a
USING purchases b
ON a.id = b.id
WHEN NOT MATCHED THEN
  INSERT *
  
```

**CONSTRAINTS**

```
%sql
ALTER TABLE purchase_dates ADD CONSTRAINT valid_date CHECK (date > '2020-01-01');
DESCRIBE EXTENDED purchase_dates; -- show in TBLPROPERTIES
```

#### Enrich Tables wit Additiona Info
- Using **current_timestamp()**
- **Input_file_name()**


```

%sql
CREATE OR REPLACE TABLE users_pii
COMMENT "Contains PII"
--LOCATION "${da.paths.working_dir}/tmp/users_pii"
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

#### Deep Clone vs Shallow Clone

**Deep Clone** Full metadata and data copie from source table.
**Shallow clone** create a copy of table quickly to test out applying changes without the risk of modifying the current table.

```
%sql
CREATE OR REPLACE TABLE purchases_clone
DEEP CLONE purchases
```


**COPY INTO** Provides SQL engineers and idempotent option to incrementally ingest data form external systems.

### Delta Live Tables

#### DAG
- execution flow is graphed
- The results are reported in the **Data Quality** section
- With each triggered update, all newly arriving data will be processed through your pipeline. Metrics will always be reported for current run.

```
@dlt.table(comment = "Python comment",table_properties = {"quality": "silver"})

COMMENT "SQL comment" TBLPROPERTIES ("quality" = "silver")
```


####  Exploring the Results of a DLT Pipeline


DLT uses Delta Lake to store all tables, each witme a query is executed, we will always return the most recent version of the table. But queries outside of DLT.  
But queries outside of DLT will return snapshot results from DLT tables, regardless of how they were defined.


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

#### Examine Lineage

- DLT provides built-in lineage information for how data flows through your table.

While the query below only indicates the direct predecessors for each table, this information can easily be combined to trace data in any table back to the point it entered the lakehouse

```
SELECT details:flow_definition.output_dataset, details:flow_definition.input_datasets 
FROM event_log_raw 
WHERE event_type = 'flow_definition' AND 
      origin.update_id = '${latest_update.id}'
```


#### Examine Data Quality Metrics

```
%sql
SELECT row_expectations.dataset as dataset,
       row_expectations.name as expectation,
       SUM(row_expectations.passed_records) as passing_records,
       SUM(row_expectations.failed_records) as failing_records
FROM
  (SELECT explode(
            from_json(details :flow_progress :data_quality :expectations,
                      "array<struct<name: string, dataset: string, passed_records: int, failed_records: int>>")
          ) row_expectations
   FROM event_log_raw
   WHERE event_type = 'flow_progress' AND 
         origin.update_id = '${latest_update.id}'
  )
GROUP BY row_expectations.dataset, row_expectations.name

```


### Creating and Governing Data with UC

**Unity Catalog´s** three-level namespace
`SELECT * FROM mycatalog.myschema.mytable;`

This can be handy in many use cases.

* Separating data relating to business units within your organization (sales, marketing )
* Satisfying SDLC requirements (dev, staging, prod, etc)
* Establishing sandboxes containing temporary datasets for internal use


#### Create and use Catalog

```
CREATE CATALOG IF NOT EXISTS ${DA.my_new_catalog}

USE CATALOG ${DA.my_new_catalog}


CREATE SCHEMA IF NOT EXISTS example;
USE SCHEMA example

```

#### Grant access to datga objects

```
GRANT USAGE ON CATALOG ${DA.my_new_catalog} TO analysts;
GRANT USAGE ON SCHEMA example TO analysts;
GRANT SELECT ON VIEW agg_heartrate to analysts
```

#### Dynamic Views

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

#### Explore objects

```
SHOW TABLES
SHOW VIEWS
SHOW SCHEMAS
SHOW CATALOGS
```


#### Explore permisions


```

SHOW GRANTS ON VIEW

SHOW GRANTS ON TABLE

SHOW GRANTS ON SCHEMA

SHOW GRANTS ON CATALOG

```


#### Revoke Access

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


````
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

```
dataset_bookstore = 'dbfs:/mnt/demo-datasets/bookstore'
spark.conf.set(f"dataset.bookstore", dataset_bookstore)
files = dbutils.fs.ls(f"{dataset_bookstore}/customers-json")
```

### 3 different ways to query from a Directory

```
SELECT * FROM json.`${dataset.bookstore}/customers-json/export_001.json` 
UNION ALL
SELECT * FROM json.`${dataset.bookstore}/customers-json/export_*.json` 
UNION ALL
SELECT * FROM json.`${dataset.bookstore}/customers-json/` 
```

```

%sql
-- input_file_name and time_s
 SELECT email,
    input_file_name() source_file,
    cast(current_timestamp() as DATE) day_of_insertion
  FROM json.`${dataset.bookstore}/customers-json` limit 3;
  

```


Reading from Binaty, CSV, text

```
SELECT * FROM text.`${dataset.bookstore}/customers-json` limit 3

SELECT * FROM binaryFile.`${dataset.bookstore}/customers-json`

SELECT * FROM csv.`${dataset.bookstore}/books-csv`

CREATE OR REPLACE TABLE orders AS
SELECT * FROM parquet.`${dataset.bookstore}/orders`
```


```
%sql

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

%sql
REFRESH TABLE books_csv;
SELECT COUNT(*) FROM books_csv;  --> retrun the actual status, External data will need to be refreshed, that does not happend with Delta Tables.
		
		
```


#### Writing to Tables

```
CREATE OR REPLACE TABLE orders AS
SELECT * FROM parquet.`${dataset.bookstore}/orders`;

INSERT OVERWRITE orders
SELECT * FROM parquet.`${dataset.bookstore}/orders`;

INSERT INTO orders
SELECT * FROM parquet.`${dataset.bookstore}/orders-new`;

DESCRIBE HISTORY orders;



%sql
CREATE OR REPLACE TEMP VIEW customers_updates AS 
SELECT * FROM json.`${dataset.bookstore}/customers-json-new`;

MERGE INTO customers c
USING customers_updates u
ON c.customer_id = u.customer_id
WHEN MATCHED AND c.email IS NULL AND u.email IS NOT NULL THEN
  UPDATE SET email = u.email, updated = u.updated
WHEN NOT MATCHED THEN INSERT *



%sql

-- we can use ":" as the Json formant of profile its not parsed, when is parsed then we have to use "."
SELECT customer_id, profile:first_name, profile:address:country 
FROM customers


```

**schema_of_json** We cann add a example of how your json-data look likes and it would parsche the schema.

```
CREATE OR REPLACE TEMP VIEW parsed_customers AS
  SELECT customer_id, from_json(profile, schema_of_json('{"first_name":"Thomas","last_name":"Lane","gender":"Male","address":{"street":"06 Boulevard Victor Hugo","city":"Paris","country":"France"}}')) AS profile_struct
  FROM customers;
  
SELECT * FROM parsed_customers limit 3;

SELECT order_id, customer_id, explode(books) as book
FROM orders  WHERE order_id = '000000000004243';

-- books look like {"book_id": "B07", "quantity": 1, "subtotal": 33}, {"book_id": "B06", "quantity": 1, "subtotal": 22}]
-- now  {"book_id": "B07", "quantity": 1, "subtotal": 33}
--      {"book_id": "B06", "quantity": 1, "subtotal": 22}

%sql
SELECT customer_id,
  collect_set(order_id) AS orders_id_set
FROM orders
WHERE customer_id = "C00002"
GROUP BY customer_id

%sql

SELECT customer_id,
  collect_set(books.book_id) As before_flatten,
  flatten(collect_set(books.book_id)) AS after_flatten,
  array_distinct(flatten(collect_set(books.book_id))) AS after_flatten_distinct
FROM orders
WHERE customer_id = "C00002"
GROUP BY customer_id ;

%sql
CREATE OR REPLACE VIEW orders_enriched AS
SELECT *
FROM (
  SELECT *, explode(books) AS book 
  FROM orders) o
INNER JOIN books b  -- default join is "inner join"
ON o.book.book_id = b.book_id;


CREATE OR REPLACE TABLE transactions AS

SELECT * FROM (
  SELECT
    customer_id,
    book.book_id AS book_id,
    book.quantity AS quantity
  FROM orders_enriched
) PIVOT (
  sum(quantity) FOR book_id in (
    'B01', 'B02', 'B03', 'B04', 'B05', 'B06',
    'B07', 'B08', 'B09', 'B10', 'B11', 'B12'
  )
);

SELECT * FROM transactions;


%sql

SELECT
  order_id,
  books,
  books.subtotal[0] as subtotal_number,
 CAST(books.subtotal[0]* 0.8  AS INT) AS subtotal_after_discount,
 ARRAY(CAST(books.subtotal[0] * 0.8 AS INT)) AS subtotal_after_discount_array,
 TRANSFORM ( books, b -> CAST(b.subtotal * 0.8 AS INT)) AS subtotal_after_discount -- TRANSFORM is a kind of MAP funktion in python.

FROM orders;


%sql

CREATE OR REPLACE FUNCTION get_url(email STRING)
RETURNS STRING

RETURN concat("https://www.", split(email, "@")[1]);

-- In that case we cann apply the function directly without use TRANSFORM cause we have just one record in our  cell
SELECT email, get_url(email) domain
FROM customers

```

## Incremental Data Processing


**Introduction**  

In previous chapters we have about ELT operations, ETL is more for DWH
ELT for Data Lake, but both have a sense of Batch processing.

To process streaming data (close to real time) we need some new structures  


`Process streaming data`: DataStreamReader + DataStreamWriter  

**Data Stream:** Any data source that grows over time, new files landing in cloud, updates to a databae capture in a CDC feed, Events queued in a pub/sub messaging feed.

**Approaches** Reprocess the entire source dataset etach tieme vs only process those new data added since last update.




#### COPY INTO vs Auto Loader

**copy into**: Thousand of files, less efficient at scale  
**Auto Loader**: Millions of Files, efficient at scale.  --> its always active and lisening so obviously would cost much more money

#### Multi-hop Architecture 

Bronce --> Silver --> Gold

```
%sql

(spark.readStream
      .table("books")
      .createOrReplaceTempView("books_streaming_tmp_vw")
)

-- that temp view is a streaming temp view as its generate from a streaming view
CREATE OR REPLACE TEMP VIEW author_counts_tmp_vw AS (
  SELECT author, count(book_id) AS total_books
  FROM books_streaming_tmp_vw
  GROUP BY author
)
-- we can write from a streaming temp view to a dataframe (author_counts), what will be running forevern every 4 secons
(spark.table("author_counts_tmp_vw")                               
      .writeStream  
      .trigger(processingTime='4 seconds')
      .outputMode("complete")
      .option("checkpointLocation", "dbfs:/mnt/demo/author_counts_checkpoint")
      .table("author_counts")
)

-- If we insert data in our original table Books its will be move to author_counts
-- books --> have a Stream_table, the stream table check the origin every 4 seconds and write in destination.

```

**Auto Loader**

Ading in format "cloudFiles" it already asume that we need a Auto Loader

```

%sql
(spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "parquet")
        .option("cloudFiles.schemaLocation", "dbfs:/mnt/demo/orders_checkpoint")
        .load(f"{dataset_bookstore}/orders-raw")
      .writeStream
        .option("checkpointLocation", "dbfs:/mnt/demo/orders_checkpoint")
        .table("orders_updates")
)
```

#### Medallon Architecture

```
%sql
CREATE OR REPLACE TEMPORARY VIEW orders_enriched_tmp AS (
  SELECT order_id, quantity, o.customer_id, c.profile:first_name as f_name, c.profile:last_name as l_name,
         cast(from_unixtime(order_timestamp, 'yyyy-MM-dd HH:mm:ss') AS timestamp) order_timestamp, books
  FROM orders_bronze_tmp o
  INNER JOIN customers_lookup c
  ON o.customer_id = c.customer_id
  WHERE quantity > 0)
  
(spark.table("orders_enriched_tmp")
      .writeStream
      .format("delta")
      .option("checkpointLocation", "dbfs:/mnt/demo/checkpoints/orders_silver")
      .outputMode("append")
      .table("orders_silver"))
	  
(spark.table("daily_customer_books_tmp")
      .writeStream
      .format("delta")
      .outputMode("complete")
      .option("checkpointLocation", "dbfs:/mnt/demo/checkpoints/daily_customer_books")
      .trigger(availableNow=True)
      .table("daily_customer_books"))
	  
```

#### Kind of Triggers

**Fixed Interval Micro-batches (using trigger(Trigger.ProcessingTime(interval)))**

This option allows you to process the data at fixed time intervals, regardless of when the data arrived.
interval could be a string like "1 minute" or a duration in milliseconds.
Use Case: When you want regular, predictable processing intervals, like processing every 10 minutes.

```
from pyspark.sql.streaming import Trigger

(spark.table("your_table")
.writeStream
.format("delta")
... # other configurations
.trigger(Trigger.ProcessingTime("1 minute"))
.table("output_table"))

```

**Once Trigger (using trigger(Trigger.Once()))**

Processes the available data in the stream just once and then stops the query.  
Use Case: When you have a backlog of data and you want to process it once to bring your output table up to date.  

```
from pyspark.sql.streaming import Trigger

(spark.table("your_table")
.writeStream
.format("delta")
... # other configurations
.trigger(Trigger.Once())
.table("output_table"))
```


**Continuous Processing (using trigger(Trigger.Continuous(interval)))**

This option will continuously process the data with a low-latency.
interval specifies the checkpoint interval.
Note: Continuous processing is an experimental feature and has some limitations.
Use Case: When low-latency is more important than throughput and you need near real-time processing.

```
from pyspark.sql.streaming import Trigger

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

## Production Pipelines


##### CDC

Change Data Capture

**Row-Level changes**: Inserring new records, Updating existing records, Deleting existing records

**Batch**  
`Table`: For Batch processing

**Streaming**  
`Live Table`: Allways updated, as alive and consuming resources, properly for streaming data, a live table may be entirely computed when possible to optimized.  
`Streamling live tables` : Processes data  that has been added only since the last pipeline update.
```
CREATE OR REFRESH STREAMING LIVE TABLE orders_raw
COMMENT "The raw books orders, ingested from orders-raw"
AS SELECT * FROM cloud_files("${datasets_path}/orders-json-raw", "json",
                             map("cloudFiles.inferColumnTypes", "true"))
							 
-- Silver

CREATE OR REFRESH STREAMING LIVE TABLE orders_cleaned (
  CONSTRAINT valid_order_number EXPECT (order_id IS NOT NULL) ON VIOLATION DROP ROW
)
COMMENT "The cleaned books orders with valid order_id"
AS
  SELECT order_id, quantity, o.customer_id, c.profile:first_name as f_name, c.profile:last_name as l_name,
         cast(from_unixtime(order_timestamp, 'yyyy-MM-dd HH:mm:ss') AS timestamp) order_timestamp, o.books,
         c.profile:address:country as country
  FROM STREAM(LIVE.orders_raw) o
  LEFT JOIN LIVE.customers c
    ON o.customer_id = c.customer_id
	


-- Gold

CREATE OR REFRESH LIVE TABLE cn_daily_customer_books
COMMENT "Daily number of books per customer in China"
AS
  SELECT customer_id, f_name, l_name, date_trunc("DD", order_timestamp) order_date, sum(quantity) books_counts
  FROM LIVE.orders_cleaned
  WHERE country = "China"
  GROUP BY customer_id, f_name, l_name, date_trunc("DD", order_timestamp)
  
-- What I dont uderstand is 1) why the gold table is live and not Streaming live, 
-- 2 why when readin from silver table 
  
```

User
ok I will formulate my question again.

I have a the following SparkSQL code

CREATE OR REFRESH STREAMING LIVE TABLE bronze_table
AS SELECT * FROM cloud_files(some_path)
							 
-- Silver

CREATE OR REFRESH STREAMING LIVE TABLE silver_table (
AS
  SELECT some_columns 
        
  FROM STREAM(LIVE.bronze_table) 

-- gold
CREATE OR REFRESH LIVE TABLE Gold_table

AS
  SELECT some_columns
  FROM LIVE.silver_table

Apparently that pseudo code is correct but I do not understand 2 things

+ 1) why bronze and silver tables are stream live and gold is just live
+ 2) why gold table read from "LIVE.silver_table" and not from "STREAM(LIVE.silver_table)

Answer


**Why are bronze and silver tables "streaming live" and gold is just "live"?**

The distinction typically aligns with the modern data architecture patterns, particularly the Delta Lake architecture. The pattern involves refining raw data in stages:

`Bronze:` This is often the raw, unrefined layer. Data lands in the bronze layer as it arrives. It's the most granular form of the data and is often not suitable for direct
querying due to inconsistencies, missing values, or its verbose nature. The "streaming live" designation means data is continuously streamed into this layer in real-time.

`Silver:` This is the cleaned and enriched version of the bronze layer. It may undergo operations like filtering, formatting, joining with other datasets,
or even some aggregations. Again, the "streaming live" designation means data from the bronze layer is being continuously processed and streamed into the silver layer in real-time.

`Gold:` This layer is optimized for consumption, often by business users. It might contain aggregated data, pre-joined datasets, 
or data reshaped into a specific format ideal for BI tools or final consumption. The data in this layer may not need to be updated in real-time, which is why it's a
"live" table without the streaming aspect. This could mean the Gold layer is built in periodic batches from the Silver layer, rather than as a continuous stream.
It provides a snapshot that is updated less frequently, which might be preferable for some reporting or analysis tasks.

**Why does the gold table read from "LIVE.silver_table" and not from "STREAM(LIVE.silver_table)"?**
This aligns with the above explanation. The "Gold" layer doesn't necessarily operate on a real-time stream from the "Silver" layer.
Instead, it might operate on periodic batches or snapshots from the "Silver" layer. By reading from "LIVE.silver_table", 
it's essentially working with the current state of the "Silver" table. On the other hand, using "STREAM(LIVE.silver_table)"
would imply real-time, continuous processing of the data from the "Silver" layer, which might not be the intention for the "Gold" layer in your architecture.

In summary, the distinction between "streaming live" and "live" and the choice of reading methods represents different stages of data refinement
and the associated processing cadence.



Question

**Can a table that have been create as `CREATE OR REFRESH STREAMING LIVE TABLE silver_table` be later reference as LIVE.silver_table ?**


Yes, once a STREAMING LIVE TABLE is created in Databricks, it acts like a Delta table with a continuously updating view of the data.
The underlying data is stored in Delta format, and you can query it like any other table in Databricks using the LIVE keyword.

The STREAM(LIVE.<table_name>)  syntax is used when you want to treat the table as a streaming source and operate on it in a streaming fashion.
So:

- When you declare a table using CREATE OR REFRESH STREAMING LIVE TABLE, it sets up a continuous ingestion process to keep updating that table with new data.

- When you query this table using SELECT ... FROM LIVE.<table_name>, you're querying its current state, getting a snapshot of the table as it is at the time of the query.

When you use the table in another streaming context with STREAM(LIVE.<table_name>), you're setting up another streaming operation on top of the continuously updating table.
Therefore, even if a table is created as a STREAMING LIVE TABLE, you can indeed query it just like a LIVE table.


