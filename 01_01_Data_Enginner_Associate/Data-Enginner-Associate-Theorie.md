## ETL with Spark

### Querying Files Directly

```
events_kafka = "dbfs:/mnt/path/"
files = dbutils.fs.ls(events_kafka)
display(files)


SELECT * FROM json.`dbfs:/mnt/my_path/`



data_path = "dbfs:/mnt/my_path//001.json"

data_json = spark.sql(f"SELECT * FROM json.`{data_path}`")

display(data_json)


%sql
CREATE OR REPLACE VIEW event_view
AS SELECT * FROM json.`dbfs:/mnt/my_path/`



CREATE OR REPLACE TEMP VIEW events_temp_view
AS SELECT * FROM json.`dbfs:/mnt/my_path/`

SELECT * FROM text.`dbfs:/mnt/my_path/`

SELECT * FROM binaryFile.`dbfs:/mnt/my_path/`

```

### Providing Options for External Sources

```
sales_csv_path = "dbfs:/mnt/my_path/"

display(spark.sql(f"select * from csv.`{sales_csv_path}`"))

```
#### External Table

- Location need to be added
- we cannot expect the performance guarantees associated with Delta Lake, example with DT you always guery the most recent version of your source data but it
it could not be the case with external tables.

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

**Running `DESCRIBE EXTENDED` on a table will show all of the metadata associate withthe table definition**

`DESCRIBE EXTENDED sales_csv`

#### Extracting Data from SQL Databases

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

### Extract Data Lab


#### assert - testing

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
	  
	  


from pyspark.sql.functions import col


usersDF = spark.read.table("users_dirty")

usersDF.selectExpr("count_if(email IS NULL)")
usersDF.where(col("email").isNull()).count()
	  
userDF.distinct().count()	  

%sql

from pyspark.sql.functions import col


usersDF = spark.read.table("users_dirty")

usersDF.selectExpr("count_if(email IS NULL)")
usersDF.where(col("email").isNull()).count()


%python
from pyspark.sql.functions import max

# remember  usersDF = spark.read.table("users_dirty")

dedupedDF = (usersDF
    .where(col("user_id").isNotNull())
    .groupBy("user_id", "user_first_touch_timestamp")
    .agg(max("email").alias("email"), 
         max("updated").alias("updated"))
    )

dedupedDF.count()


#### Validate Datasets

```
SELECT max(row_count) <= 1 no_duplicate_ids FROM (
  SELECT user_id, count(*) AS row_count
  FROM deduped_users
  GROUP BY user_id)
 
-- the results is True or False

%python
from pyspark.sql.functions import count

display(dedupedDF
    .groupby("user_id")
    .agg(count("*").alias("row_count"))
    .select((max("row_count") <= 1).alias("no_duplicate_ids"))) # true or false 

```

#### Date Format and Regex

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
  

%python
from pyspark.sql.functions import date_format, regexp_extract

display(dedupedDF
    .withColumn("first_touch", (col("user_first_touch_timestamp") / 1e6).cast("timestamp"))
    .withColumn("first_touch_date", date_format("first_touch", "MMM d, yyyy"))
    .withColumn("first_touch_time", date_format("first_touch", "HH:mm:ss"))
    .withColumn("email_domain", regexp_extract("email", "(?<=@).+", 0))
	.select("first_touch", "first_touch_date", "first_touch_time", "email_domain")
)

#### Complex Transformations

```

#@DBAcademyHelper.monkey_patch
def clone_source_table(table_name, source_path, source_name=None):
    #start = self.clock_start()

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



Let's use the JSON string example above to derive the schema, then parse the entire JSON column into struct types.

**schema_of_json()** returns the schema derived from an example JSON string.
**from_json()** parses a column containing a JSON string into a struct type using the specified schema.



CREATE OR REPLACE TEMP VIEW parsed_events AS SELECT json.* FROM (
SELECT from_json(value, schema_of_json('{"device":"Linux","ecommerce":{"purchase_revenue_in_usd":1075.5,
                                         "total_item_quantity":1,"unique_items":1},"event_name":"finalize",
										 "event_previous_timestamp":1593879231210816,"event_timestamp":1593879335779563,
										 "geo":{"city":"Houston","state":"TX"},
										 "items":[{"coupon":"NEWBED10","item_id":"M_STAN_K","item_name":"Standard King Mattress","item_revenue_in_usd":1075.5,"price_in_usd":1195.0,"quantity":1}],#
										 "traffic_source":"email","user_first_touch_timestamp":1593454417513109,"user_id":"UA000000106116176"}')) AS json 
FROM events_strings);



%python
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



#### Manipulate Arrays

**explode()** separates the elements of an array into multiple rows; this creates a new row  for each elemnt.
**size()** provides a count for the number of elements in an array for each row.


```

CREATE OR REPLACE TEMP VIEW exploded_events AS
SELECT *, explode(items) AS item
FROM parsed_events;

SELECT * FROM exploded_events WHERE size(items) > 2


%python
from pyspark.sql.functions import explode, size

exploded_eventsDF = (parsed_eventsDF
    .withColumn("item", explode("items"))
)

display(exploded_eventsDF.where(size("items") > 2))


%sql
CREATE OR REPLACE TEMP VIEW events_explode AS ( SELECT device, explode(items) as items from events_enrique_table limit 2);

select * from events_explode;


CREATE OR REPLACE TEMP VIEW events_external_items AS 
SELECT json.*
FROM (
    SELECT from_json(CAST(items AS STRING), 
        schema_of_json('{"coupon": "NEWBED10", "item_id": "M_STAN_F", "item_name": "Standard Full Mattress", "item_revenue_in_usd": 850.5, "price_in_usd": 945, "quantity": 1}')
    ) AS json 
    FROM events_explode
);

```

**collect_set()** collects unique values for a field, including fields within arrays.  
**flatten()** combines multiple arrays into a single array.  
**array_distinct()** removes duplicate elements from an array.  


```

SELECT user_id,
  collect_set(event_name) AS event_history,
  array_distinct(flatten(collect_set(items.item_id))) AS cart_history
FROM exploded_events
GROUP BY user_id



%python

from pyspark.sql.functions import array_distinct, collect_set, flatten

display(exploded_eventsDF
    .groupby("user_id")
    .agg(collect_set("event_name").alias("event_history"),
            array_distinct(flatten(collect_set("items.item_id"))).alias("cart_history"))
			
			
```


#### Join Tables

```

CREATE OR REPLACE TEMP VIEW item_purchases AS

SELECT * 
FROM (SELECT *, explode(items) AS item FROM sales) a
INNER JOIN item_lookup b
ON a.item.item_id = b.item_id;

SELECT * FROM item_purchases


%python
exploded_salesDF = (spark
    .table("sales")
    .withColumn("item", explode("items"))
)

itemsDF = spark.table("item_lookup")

item_purchasesDF = (exploded_salesDF
    .join(itemsDF, exploded_salesDF.item.item_id == itemsDF.item_id)
)

display(item_purchasesDF)

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


%python
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

### SQL and Control Flow 

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

#normal function

def first_letter_function(email):
    return email[0]

first_letter_function("annagray@kaufman.com")

```
create apply UDF, register the function as a UDF. This serializes the function and sends it to executors to be able to transofrm DataFrame records.

`first_letter_udf = udf(first_letter_function)`

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

```

%sql
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


Describe Extended vs detail vs history

- Extendes for Data types  
- Detail for metadata associate to the Table  
- Histry for the opertions where made in the Table


```

%sql
OPTIMIZE students
ZORDER BY id

DESCRIBE HISTORY students


#### Versions

%sql
select * from students c where c.id not in (SELECT a.id 
FROM (select * from students  VERSION AS OF 3) a
inner join (select * from students VERSION as OF 7) b
on a.id = b.id)



#### Roll Back

```
%sql
DELETE FROM students

%sql
RESTORE TABLE students TO VERSION AS OF 8



%python
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

Code Merge

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

select * from purchase_dates;



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

+ Provide the abilito to do fine-grained access control


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



