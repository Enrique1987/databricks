Yes. Taking our whole conversation into account, I would separate them like this.

Important: not all of these are technically “functions”. Some are **Databricks-specific SQL clauses or DDL commands**. But they are all things you should mentally mark as **Databricks-special / not normal ANSI SQL**.

## A. Databricks-special SQL clauses / commands

|  # | Feature                                  | Type                              | Simple meaning                                                   |
| -: | ---------------------------------------- | --------------------------------- | ---------------------------------------------------------------- |
|  1 | `MASK`                                   | Column clause                     | Applies a masking function to a column when rows are read.       |
|  2 | `ROW FILTER` / `WITH ROW FILTER`         | Table clause                      | Applies a row-level security filter when rows are read.          |
|  3 | `EXPECT`                                 | Lakeflow / DLT expectation clause | Data quality rule in pipelines.                                  |
|  4 | `CREATE SHARE`                           | Delta Sharing DDL                 | Creates an empty share/package.                                  |
|  5 | `ALTER SHARE`                            | Delta Sharing DDL                 | Adds/removes tables, views, schemas, volumes, etc. from a share. |
|  6 | `WITH HISTORY`                           | Delta Sharing option              | Shares table history so recipients can use time travel / CDF.    |
|  7 | `CREATE RECIPIENT`                       | Delta Sharing DDL                 | Creates the recipient identity for sharing.                      |
|  8 | `GRANT SELECT ON SHARE ... TO RECIPIENT` | Delta Sharing privilege           | Gives a recipient read access to a share.                        |

`MASK` and `ROW FILTER` are Unity Catalog governance features applied when data is fetched. `EXPECT` is used in Lakeflow Declarative Pipelines for data-quality rules. `CREATE SHARE` and `ALTER SHARE` are Unity Catalog / Delta Sharing commands. ([Databricks Dokumentation][1])

---

## B. Databricks-special / Spark-Databricks functions

|  # | Function                                        | Type                            | Use case                                                          |
| -: | ----------------------------------------------- | ------------------------------- | ----------------------------------------------------------------- |
|  9 | `window(timestamp_col, duration, slide, start)` | Time grouping function          | Group events into time buckets, for example CPU every 10 minutes. |
| 10 | `table_changes()`                               | Table-valued function           | Read Change Data Feed / CDF from a Delta table.                   |
| 11 | `is_member()`                                   | Identity function               | Check if current user belongs to a group.                         |
| 12 | `is_account_group_member()`                     | Unity Catalog identity function | Check account-level group membership.                             |
| 13 | `current_recipient()`                           | Delta Sharing function          | Get recipient-specific properties during sharing.                 |
| 14 | `current_metastore()`                           | Unity Catalog function          | Return current metastore ID.                                      |
| 15 | `current_version()`                             | Databricks version function     | Return Databricks SQL / Runtime version information.              |
| 16 | `secret()`                                      | Databricks secret function      | Read a secret from a Databricks secret scope.                     |
| 17 | `try_secret()`                                  | Databricks secret function      | Like `secret()`, but returns `NULL` instead of failing.           |

`table_changes()` returns changed rows from a Delta table with CDF enabled, including metadata like `_change_type`, `_commit_version`, and `_commit_timestamp`. `is_account_group_member()` is Unity-Catalog-only and checks account-level group membership. `current_recipient()` is specifically for Delta Sharing access logic. `secret()` reads from Databricks secret service. ([Databricks Dokumentation][2])

---

## C. Databricks file-ingestion / external-access functions

|  # | Function              | Type                  | Use case                                             |
| -: | --------------------- | --------------------- | ---------------------------------------------------- |
| 18 | `read_files()`        | Table-valued function | Read files directly from storage using SQL.          |
| 19 | `cloud_files_state()` | Table-valued function | Inspect Auto Loader / file-ingestion state.          |
| 20 | `read_statestore()`   | Table-valued function | Inspect Structured Streaming state store data.       |
| 21 | `remote_query()`      | Table-valued function | Query external databases via Databricks connections. |

These are very Databricks-platform-oriented. `read_files()` is especially important in modern Databricks SQL / Lakeflow examples because it can read cloud/object-storage files directly. `remote_query()` lets Databricks SQL query external systems through configured connections. ([Databricks Dokumentation][3])

---

## D. Databricks AI / Mosaic AI SQL functions

|  # | Function                 | Use case                                                            |
| -: | ------------------------ | ------------------------------------------------------------------- |
| 22 | `ai_query()`             | General-purpose call to model serving / foundation model endpoints. |
| 23 | `ai_classify()`          | Classify text into labels.                                          |
| 24 | `ai_extract()`           | Extract structured fields from text/documents.                      |
| 25 | `ai_forecast()`          | Forecast time series data.                                          |
| 26 | `ai_parse_document()`    | Parse document contents.                                            |
| 27 | `ai_summarize()`         | Summarize text.                                                     |
| 28 | `ai_translate()`         | Translate text.                                                     |
| 29 | `ai_analyze_sentiment()` | Sentiment analysis.                                                 |
| 30 | `ai_mask()`              | Mask entities in text using AI.                                     |
| 31 | `ai_fix_grammar()`       | Correct grammar.                                                    |
| 32 | `ai_similarity()`        | Semantic similarity between texts.                                  |
| 33 | `ai_gen()`               | Generate text from a prompt.                                        |
| 34 | `ai_prep_search()`       | Prepare parsed documents for search/RAG pipelines.                  |
| 35 | `vector_search()`        | Query a Mosaic AI Vector Search index from SQL.                     |

Databricks documents AI Functions as built-in SQL functions for applying LLMs or AI techniques directly on data in Databricks; `ai_query()` is the general-purpose one, while functions like `ai_classify`, `ai_extract`, `ai_translate`, and others are task-specific. `vector_search()` queries Mosaic AI Vector Search indexes from SQL. ([Databricks Dokumentation][4])

---

## E. Databricks `VARIANT` / semi-structured data functions

|  # | Function                  | Use case                                          |
| -: | ------------------------- | ------------------------------------------------- |
| 36 | `parse_json()`            | Parse a JSON string into Databricks `VARIANT`.    |
| 37 | `try_parse_json()`        | Safe version of `parse_json()`.                   |
| 38 | `variant_get()`           | Extract a typed value from a `VARIANT`.           |
| 39 | `try_variant_get()`       | Safe version of `variant_get()`.                  |
| 40 | `variant_explode()`       | Explode `VARIANT` arrays/objects.                 |
| 41 | `schema_of_variant()`     | Infer schema from one `VARIANT`.                  |
| 42 | `schema_of_variant_agg()` | Infer combined schema from many `VARIANT` values. |

These are not “classic SQL” functions. They belong to Databricks’ newer semi-structured data model around the `VARIANT` type. `parse_json()` returns a `VARIANT`, `variant_get()` extracts values from it, and `schema_of_variant_agg()` infers a combined schema over multiple `VARIANT` values. ([Databricks Dokumentation][5])

---

## F. Things we discussed that are **not Databricks-special**

These are important, but not Databricks-specific:

| Feature                                           | Category                                      |
| ------------------------------------------------- | --------------------------------------------- |
| `ROW_NUMBER() OVER (...)`                         | Standard SQL analytical window function       |
| `LAG() OVER (...)`                                | Standard SQL-style analytical window function |
| `RANK() OVER (...)`                               | Standard SQL-style analytical window function |
| `MIN()`, `MAX()`, `COUNT()`, `SUM()`              | Standard aggregate functions                  |
| `CASE WHEN ... THEN ... END`                      | Standard SQL conditional expression           |
| `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, `JOIN` | Standard SQL                                  |
| `EXCEPT`                                          | Standard SQL set operator                     |

So the clean mental classification is:

```text
Standard SQL:
  SELECT, JOIN, CASE, GROUP BY, EXCEPT, ROW_NUMBER() OVER (...)

Spark / Databricks SQL:
  window(event_time, '10 minutes'), explode(), from_json(), arrays, maps, structs

Databricks-special:
  MASK, ROW FILTER, EXPECT, CREATE SHARE, ALTER SHARE,
  table_changes(), read_files(), ai_query(), vector_search(),
  is_account_group_member(), current_recipient(), secret(), VARIANT functions
```

For your certification notes, the most important ones from this conversation are:

```text
1. MASK
2. ROW FILTER
3. EXPECT
4. CREATE SHARE
5. ALTER SHARE
6. WITH HISTORY
7. table_changes()
8. window(event_time, ...)
9. is_member()
10. is_account_group_member()
11. current_recipient()
12. read_files()
13. ai_query()
14. vector_search()
15. parse_json() / variant_get()
```

That is the practical list I would memorize first.

[1]: https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-column-mask?utm_source=chatgpt.com "Column mask clause | Databricks on AWS"
[2]: https://docs.databricks.com/aws/en/sql/language-manual/functions/table_changes?utm_source=chatgpt.com "table_changes table-valued function | Databricks on AWS"
[3]: https://docs.databricks.com/gcp/en/sql/language-manual/functions/read_files?utm_source=chatgpt.com "read_files table-valued function"
[4]: https://docs.databricks.com/aws/en/large-language-models/ai-functions?utm_source=chatgpt.com "Enrich data using AI Functions | Databricks on AWS"
[5]: https://docs.databricks.com/aws/en/sql/language-manual/functions/parse_json?utm_source=chatgpt.com "parse_json function | Databricks on AWS"
