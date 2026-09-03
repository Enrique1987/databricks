# Modeling Semi-Structured Data with `VARIANT`

Status: **Reviewed**

Last reviewed: 2026-09-03

## Purpose and scope

This guide helps data engineers choose between JSON stored as `STRING`, a fixed `STRUCT`, and the native `VARIANT` type in Databricks. It focuses on Bronze-to-Silver design for APIs, events, and logs. The examples use Databricks SQL and are illustrative; validate source-specific behavior, malformed-record handling, table protocol compatibility, and performance before production use.

## The architectural boundary

`VARIANT` improves how a flexible payload is represented and queried; it does not replace downstream data contracts.

```text
API or event source
        |
        v
Bronze: payload VARIANT
        |
        | extract, cast, validate, quarantine
        v
Silver: typed columns and explicit contracts
        |
        v
Gold: business-facing model
```

Schema drift can therefore be absorbed in Bronze without immediately changing the table shape. If a new source attribute becomes part of a business contract, Silver and its consumers still need a deliberate schema change.

## Choosing the representation

| Representation | Best fit | Main trade-off |
| --- | --- | --- |
| JSON as `STRING` | Byte-for-byte preservation, legacy pipelines, or systems that only transport the payload | Every consumer must interpret text before using fields |
| `STRUCT` | Stable, known schema with strongly typed fields | Schema evolution is explicit and heterogeneous events can become awkward |
| `VARIANT` | Flexible, nested, or evolving semi-structured payloads | Important fields still need typed extraction; several relational operations are restricted |

For a new flexible semi-structured workload, Databricks recommends `VARIANT` over JSON strings. Do not migrate a healthy `STRING` pipeline solely because a newer type exists: require a concrete benefit such as simpler exploration, lower parsing cost, or better handling of heterogeneous records.

## Minimal Bronze-to-Silver pattern

The table-level support documented for Delta Lake requires Databricks Runtime 15.4 LTS or later. Creating a `VARIANT` column enables the corresponding Delta table feature.

```sql
CREATE TABLE bronze.events (
  ingestion_time TIMESTAMP,
  source_file STRING,
  payload VARIANT
);

INSERT INTO bronze.events
VALUES (
  current_timestamp(),
  'illustrative.json',
  parse_json('{"event":"purchase","user_id":123,"amount":49.95}')
);
```

Path navigation is case-sensitive for `VARIANT`. Cast fields when promoting them into a stable contract:

```sql
CREATE OR REPLACE TABLE silver.purchases AS
SELECT
  payload:event::STRING AS event_name,
  payload:user_id::BIGINT AS user_id,
  payload:amount::DECIMAL(18, 2) AS amount,
  ingestion_time
FROM bronze.events
WHERE payload:event::STRING = 'purchase';
```

For untrusted input, use error-tolerant functions such as `try_parse_json`, `try_variant_get`, or `try_cast`, and route failed records to an observable quarantine path instead of silently discarding them.

## Schema-on-read and schema-on-write

- **Schema-on-read** stores raw or loosely structured data first and applies interpretation when data is consumed. A flexible Bronze `VARIANT` column fits this approach.
- **Schema-on-write** validates and types data as it enters a target model. Typed Silver columns are an example.

These approaches can coexist in one Medallion pipeline. Flexibility at ingestion does not remove schema enforcement from curated layers.

## Operational constraints

A `VARIANT` column cannot currently be used as a partition or clustering column, with `GROUP BY` or `ORDER BY`, with `DISTINCT`, or in SQL set operations. It also lacks minimum/maximum column statistics. Extract frequently filtered, joined, grouped, governed, or business-critical attributes into typed columns.

Enabling `VARIANT` on an existing Delta table upgrades its writer protocol and can affect external Delta clients. For Iceberg, `VARIANT` requires Iceberg v3; Iceberg v2 does not support it. Check interoperability before changing an existing table.

## Migration decision

Migrate JSON-as-`STRING` only when the expected value outweighs compatibility and change risk:

1. Identify repeated parsing, exploration friction, or performance issues.
2. Inventory readers and verify Delta protocol or Iceberg v3 compatibility.
3. Compare representative read/write workloads and malformed-input behavior.
4. Validate case-sensitive paths, JSON null semantics, and downstream casts.
5. Roll out as a contract change with monitoring and a rollback path.

## Validation query

After running the illustrative example, this query should return one row with `user_id = 123` and `amount = 49.95`:

```sql
SELECT user_id, amount
FROM silver.purchases
WHERE event_name = 'purchase';
```

## Primary sources

- [Databricks `VARIANT` type](https://docs.databricks.com/aws/en/sql/language-manual/data-types/variant-type)
- [How `VARIANT` differs from JSON strings](https://docs.databricks.com/aws/en/semi-structured/variant-json-diff)
- [Query `VARIANT` data](https://docs.databricks.com/aws/en/semi-structured/variant)
- [`VARIANT` support and limitations for Delta Lake and Iceberg](https://docs.databricks.com/aws/en/tables/features/variant)
