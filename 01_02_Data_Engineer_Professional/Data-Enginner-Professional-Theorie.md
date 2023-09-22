# Databricks Data Engineer Professional

Here we have the two learning path I followed for the Professional the Udemy and the Databricks curseware.

## Databricks 

### Architeching for the Lakehouse

**Data Lakehouse**  

`Data Lakes:`  Is a centralized repository designed to store, process, and secure large amounts of structured, semistructured, and unstructured data. They 
are good for Machine Learning and Big Data but are lacking in BI and face challenges in the Data Governance.  

on the oder side.

`Data Wharehouse` Is a centralized repository for storing large volumens of data from multiple sources. It is designed for query and analysis, often used for business Intelligence activities.


**Streaming Design Patterns**  

	

### Bronze Ingestions Patterns

**Bronze Layer**   
- Replaces the raditional data lake.  
- Represents the full, unprocessed hisotry of the data.  
- Captures the provenance(what,when and from where) of data loaded intoe the lakehouse.  
- Data is stored efficiently using Delta Lakehouse.  
- If downstream layers discover later they need to ingest more, they can come back to the Bronze source to obtain it.  

**Bronze Layer Principles**  
- The goal is data capture and provenance: Capture exactly what is ingested, without parsing or change.
- Typically a Delta Lake table with these fields in each row:
	- Date received/ingested  
	- Data source (filename,external system etc)  
	- Text field with raw unparsed JSON, CSV or other data  
	- Other metadata  
- Should be append only(batch or streaming)  
- Plan ahead if data must be deleted for regulatory purposes  
	- Retain all records when possible  
	- Soft-deletes if necessary  
	- Hard-deletes may be required by regulatory processes.  

**Bronze Inmgestion Patterns**  
- **Singleplex Ingestion**: Every Raw data to a Delta Lake   
- **Mutiplex Ingestion**: For nearly real-time data ingestion, normaly from a pop up system.  
	- Do not use the pop up system as bronze leyer as they are not real tables and have limited time of retention.  
	

### Promoting to Silver

**Silver Layer**  
- Easier to query than the non-curated Bronzed   
	- Data is clean  
	- Transactions have ACID guarantees  
- Represent the "Enterprise Data Model"  
- Captures the full history of business action modeled  
	- Each record processes is preserved  
	- All records can be efficiently queried  
- Reduces data stroage complexity, latency and redundancy  
	- Built for both ETL throughput AND analytic query performance.  
	
- Silver Layer guiding Principles  

	- Uses Delta Lake tables(with SQL table names)  
	- Preserves grain of original data(no aggregation)  
	- Eliminate duplicate records   
	- Production schema enforced   
	- Data quality checks passed  
	- Corrupt data guarantine   
	- Data stored to support production workloads  
	- Optimized for long-term retention and ad-hoch queries  
	


### Gold Query Layer

**Gold Layer**
- Powers ML applications, reporting, dashboards, ad hoch analytics
- Reduces costs associated with ad hoch queries on silver tables
- Allow fine grained permissions
- Reduces strain on production systems  
- Shifts query updates to production workloads

### Storing Data Securely

### Propagating Updated and Deletes

### Orchestration and Scheduling



## Udemy

## Data Modeling

## Data Processing

## Databricks Tooling

## Security and Governance

## Testing and Deployment

## Monitoring and logging

