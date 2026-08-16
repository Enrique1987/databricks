# Databricks-Specific SQL Reference

Status: **Reviewed**  
Last reviewed: 2026-08-16

This page separates Databricks platform extensions from standard SQL and Apache Spark SQL. It is a navigation aid, not a substitute for the runtime-specific documentation.

## Governance and sharing

| Feature | Purpose | Important constraint |
| --- | --- | --- |
| `MASK` | Apply a Unity Catalog column mask at query time | Requires a SQL UDF and supported compute |
| `ROW FILTER` | Filter rows through a Unity Catalog SQL UDF | Test performance and permissions before production use |
| `CREATE SHARE` / `ALTER SHARE` | Manage OpenSharing objects | Unity Catalog and sharing privileges are required |
| `is_account_group_member()` | Test account-level group membership | Prefer this to workspace-local group checks for Unity Catalog policies |
| `current_recipient()` | Read recipient properties in a shared object | Intended for recipient-aware OpenSharing logic |

Sources: [column masks](https://docs.databricks.com/aws/en/tables/row-and-column-filters), [OpenSharing SQL commands](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-sharing), and [identity functions](https://docs.databricks.com/aws/en/sql/language-manual/functions/is_account_group_member).

## Ingestion, streaming, and change data

| Feature | Purpose | Important constraint |
| --- | --- | --- |
| `read_files()` | Read supported files as a table-valued function | Use Unity Catalog external locations or volumes and explicit schemas in production |
| `cloud_files_state()` | Inspect file-level Auto Loader or `read_files` stream state | Permissions and available fields depend on runtime version |
| `table_changes()` | Read Delta Change Data Feed records | Change Data Feed must be enabled; retention limits available history |
| `read_statestore()` | Inspect Structured Streaming state-store data | Use for diagnosis, not as an application contract |
| `remote_query()` | Execute a query through a Unity Catalog connection | Public Preview as of this review; validate connector support and pushdown behavior |

Sources: [`read_files`](https://docs.databricks.com/aws/en/sql/language-manual/functions/read_files), [`cloud_files_state`](https://docs.databricks.com/aws/en/sql/language-manual/functions/cloud_files_state), [`table_changes`](https://docs.databricks.com/aws/en/sql/language-manual/functions/table_changes), and [`remote_query`](https://docs.databricks.com/aws/en/sql/language-manual/functions/remote_query).

## AI functions

| Feature | Purpose | Important constraint |
| --- | --- | --- |
| `ai_query()` | Query a serving endpoint from SQL | Permission, model availability, cost, latency, and error behavior matter |
| `ai_parse_document()` | Parse document content into structured output | Availability and supported formats can vary by region and runtime |
| `ai_prep_search()` | Prepare parsed documents for search and RAG | Beta as of this review |
| `vector_search()` | Query an AI Search index from SQL | Public Preview and specific compute requirements as of this review |

The product is now called **AI Search**; older material may call it Mosaic AI Vector Search or Databricks Vector Search. The SQL function remains `vector_search()`.

Source: [AI Functions](https://docs.databricks.com/aws/en/large-language-models/ai-functions) and [`vector_search`](https://docs.databricks.com/aws/en/sql/language-manual/functions/vector_search).

## Semi-structured data

| Feature | Purpose |
| --- | --- |
| `parse_json()` / `try_parse_json()` | Convert JSON text to `VARIANT` |
| `variant_get()` / `try_variant_get()` | Extract and cast a value at a JSON path |
| `variant_explode()` | Expand a `VARIANT` array or object |
| `schema_of_variant()` / `schema_of_variant_agg()` | Infer the schema of one or many `VARIANT` values |

Check runtime support before using `VARIANT`; some features remain in Preview.

Source: [`VARIANT` type](https://docs.databricks.com/aws/en/sql/language-manual/data-types/variant-type).

## Pipeline syntax is a separate category

Data-quality expectations and declarative flow definitions belong to **Lakeflow Spark Declarative Pipelines**, not general ANSI SQL. The former product and Python module were called Delta Live Tables and `dlt`.

Current Python examples should prefer:

```python
from pyspark import pipelines as dp

@dp.materialized_view
@dp.expect_or_drop("valid_id", "id IS NOT NULL")
def valid_records():
    return spark.read.table("main.raw.records")
```

Existing `dlt` code remains supported, but Databricks recommends the `pyspark.pipelines` names for new work. See [What happened to Delta Live Tables?](https://docs.databricks.com/aws/en/ldp/concepts/where-is-dlt).

## Not Databricks-specific

The following are important but should not be presented as proprietary Databricks functions:

- Standard SQL: `SELECT`, `JOIN`, `CASE`, `GROUP BY`, `EXCEPT`, `ROW_NUMBER()`, `LAG()`, and aggregate functions.
- Apache Spark SQL: higher-order array functions, structs, maps, `explode()`, `from_json()`, and event-time `window()`.

Always verify the current availability, cloud support, runtime requirement, and Preview status in the linked documentation before production use.
