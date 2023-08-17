# databricks  Associate and Professional Questions 

Some of the questions are just theortical concepts that we have to know.


#### Tables, Live Tables and Stream Live Tables, what are the difference ?

`Tables`: Made for data processing in batch mode

`Stream Table`: continuously ingest and update data from streaming sources, presenting a real-time view of data as it's being received. 


`Live Tables`: Reflects the results of the query that defines it, including when the query defining the table or view is updated,
 or an input data source is updated. Like a traditional materialized view, a live table or view may be entirely computed when possible to optimize computation resources and time.
 
 in a very very simple way to think about that could be a table that is automatically refresh, 
 
`streaming live table`: Processes data that has been added only since the last pipeline update.

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