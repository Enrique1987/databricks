# databricks  Associate and Professional Questions 

Some of the questions are just theortical concepts that we have to know.


##### Tables, Live Tables and Stream Live Tables, what are the difference ?

`Tables`: Made for data processing in batch mode

`Live Tables`: Reflects the results of the query that defines it, including when the query defining the table or view is updated,
 or an input data source is updated. Like a traditional materialized view, a live table or view may be entirely computed when possible to optimize computation resources and time.
 
`streaming live table`: Processes data that has been added only since the last pipeline update.


##### Scenario of Live Table and Stream Live Table

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