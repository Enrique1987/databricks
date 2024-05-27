## Databricks Data Engineer Interview Questions.

These questions are based on my experience as a data engineer over several years in the industry.  They are related to Databricks

#### Question 1
**A new task arrives. A column needs to be changed from `timestamp` to `date`. This is a column that has been in the table for a long time.
It is a created column and the process that creates it is as follows**

`insert_values["valid_from"] = date_sub(current_timestamp(), 1)`

*Answer: 
we need to change 2 things
- 1) The function that generates this column and modify the code to convert that column to date.
`insert_values["valid_from"] = to_date(date_sub(current_timestamp(), 1))`

- 2) change the existing data in this column to Date type, otherwise the next time this data is generated,
 an inconsistency will be created, as the incoming data is date type and the existing data is timestap type.
 This only needs to be done once as it would be part of a script that would only be launched once on the system.
 - To finish the process we should simply check that the change has been made correctly.
 - Add a dummy data and check that it has been inserted correctly with the desired data type.
 - Delete the test dummy data.*

#### Question 2
**Related with question 1, so how would do change the data type already existing in a table ?**

*Answer

2 ways:

 `python`:
	- Select all table you are intereseted, 
	- Change data type 
	- Overwritte your df with already corrected values in the path where the delta table is.
	
	```python
	

# Define the path to the Delta table
delta_table_path = "my_path"

# Step 1: Read the existing Delta table
df = spark.read.format("delta").load(delta_table_path)

# Step 2: Create a temporary view with the date transformations
transformed_df = df.selectExpr("* EXCEPT(valid_from)", "valid_from") \
					withColumn("valid_from", to_date(df["valid_from"]))


# Step 3: Overwrite the existing Delta table with the transformed data
transformed_df.write.format("delta").mode("overwrite").save(delta_table_path)
```

  `sql`
  ```sql
		-- Step 1: Create a temporary view with the date transformations
		CREATE OR REPLACE TEMP VIEW transformed_my_table AS
		SELECT
			* EXCEPT(valid_from), 
			to_date(valid_from) AS valid_from
		FROM delta.`my_path`;

		-- Step 2: Overwrite the existing Delta table with the transformed data
		CREATE OR REPLACE TABLE delta.`my_path` AS
		SELECT * FROM transformed_my_table;
  ```