# Row Access Based on Project Membership

Status: **Reviewed** documentation; illustrative SQL, workspace execution pending.

Last reviewed: 2026-10-03

For data engineers learning how a project-to-user mapping can control table access. This example targets a Unity Catalog SQL warehouse on Databricks on AWS. It uses synthetic projects and identities; it is not a deployed security policy.

## Remember first

**The mapping records who belongs to a project; the row filter enforces that relationship when someone queries project data.**

| Object | Responsibility |
| --- | --- |
| Project data table | Stores the business rows and their project IDs |
| Membership table | Stores one approved project/user pair per membership |
| Boolean SQL function | Checks the querying identity against those memberships |
| Attached row filter | Applies that function to queries on the protected table |

A normal join in one notebook does not protect users who can query the underlying table directly. In this example, the rule is attached to the table. For a curated interface across several tables, compare a [dynamic view](../reference/databricks-views.md#dynamic-views). For centrally managed policies across many assets, consider [Unity Catalog ABAC](https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/).

## Set up the synthetic case

Use an existing disposable `study_lab` catalog. Run setup as an owner authorized to create two fresh schemas, tables, and a function. Keep consumer access disabled until the policy is attached. Replace the example identities with real test-account identities before conducting access tests.

```sql
CREATE SCHEMA study_lab.project_security_demo;
CREATE SCHEMA study_lab.project_data_demo;

CREATE TABLE study_lab.project_security_demo.memberships (
  project_id STRING NOT NULL,
  principal STRING NOT NULL
) USING DELTA;

INSERT INTO study_lab.project_security_demo.memberships VALUES
  ('P100', 'alex@example.com'),
  ('P100', 'sam@example.com'),
  ('P200', 'sam@example.com');

CREATE TABLE study_lab.project_data_demo.project_records (
  project_id STRING NOT NULL,
  record_id INT NOT NULL,
  description STRING
) USING DELTA;

INSERT INTO study_lab.project_data_demo.project_records VALUES
  ('P100', 1, 'Synthetic planning record'),
  ('P200', 2, 'Synthetic delivery record'),
  ('P300', 3, 'Synthetic unassigned record');
```

One row per membership makes grants and revocations easy to inspect. Enforce uniqueness in the membership-maintenance process. The `EXISTS` check below does not duplicate business rows if a membership is accidentally repeated.

## Define and attach the rule

```sql
CREATE FUNCTION study_lab.project_security_demo.can_read_project(
  requested_project_id STRING
)
RETURNS BOOLEAN
RETURN EXISTS (
  SELECT 1
  FROM study_lab.project_security_demo.memberships AS membership
  WHERE membership.project_id = requested_project_id
    AND membership.principal = SESSION_USER()
);

ALTER TABLE study_lab.project_data_demo.project_records
SET ROW FILTER study_lab.project_security_demo.can_read_project
ON (project_id);
```

The declared and attached function names must match. The function parameter and project column both use `STRING`. There is no privileged-group bypass in this example: a user with no matching membership receives no rows.

Databricks documents mapping-table UDFs and states that identity functions such as `SESSION_USER()` use the invoking user's context, while other filter operations use the definer's rights. See [manual row filters and mapping tables](https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/manually-apply).

The function owner must retain the required access to the membership table. Table-policy assignment also needs the relevant ownership/management and function privileges described in that reference. After attachment, give test consumers only catalog/schema usage and `SELECT` on the protected table; do not give them membership-table write access or policy-management privileges.

## Verify as different users

Run this query in separately authenticated sessions. Changing a string parameter in an administrator's notebook is not an identity test.

```sql
SELECT SESSION_USER() AS querying_identity;

SELECT project_id, record_id
FROM study_lab.project_data_demo.project_records
ORDER BY project_id, record_id;
```

| Authenticated test user | Expected visible projects |
| --- | --- |
| Alex, mapped only to P100 | P100 |
| Sam, mapped to P100 and P200 | P100, P200 |
| User with table access but no membership | None |
| Alex after an authorized owner revokes the P100 mapping | None on the next query |

Additional checks: consumers cannot edit memberships, detach the filter, or access an unprotected copy or underlying storage with separate credentials. Test normal query results and permission-denied paths. A filtered table does not retroactively protect data already copied elsewhere.

## Operational boundaries

- Keep the mapping table outside circular policy dependencies and do not attach another active row filter or mask to it in this example.
- Evaluate performance with realistic membership size and query shapes; a lookup is more work than a simple constant predicate.
- Restrict and audit membership changes: editing a mapping is changing authorization.
- Runtime and API support differ. Do not assume time travel, cloning, sharing, streaming, or write paths behave like unrestricted tables; check the [current limitations](https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/).

The local historical note used an array of emails and inconsistent function references. This version preserves the project-membership idea, normalizes the mapping, and specifies the expected access outcomes. It does not assert that a row filter alone establishes regulatory compliance.

## Validation and cleanup

The SQL pattern and source documentation were reviewed; the multi-user checks above have **not** been executed in a Databricks workspace. Do not mark those outcomes as observed until they have been tested with real test identities.

After revoking consumer access, remove only the disposable objects created for this exercise, as their owner:

```sql
DROP TABLE study_lab.project_data_demo.project_records;
DROP FUNCTION study_lab.project_security_demo.can_read_project;
DROP TABLE study_lab.project_security_demo.memberships;
DROP SCHEMA study_lab.project_data_demo;
DROP SCHEMA study_lab.project_security_demo;
```

Dropping the protected demo table first avoids leaving an accessible unfiltered table during cleanup. Do not use this teardown on shared schemas or production objects.

## Check your understanding

**Why is permission to edit the membership table more sensitive than permission to query the protected table?**

<details>
<summary>Show reasoning</summary>

A reader can see the rows already authorized for them. A membership editor can change which identities the policy authorizes. Separate membership administration from consumption and test that separation.

</details>

## Sources and related reading

- [Apply row filters and use mapping tables](https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/manually-apply)
- [Row filters, masks, alternatives, and limitations](https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/)
- [Databricks-specific SQL reference](../reference/databricks-specific-sql.md)
- [Views and semantic objects](../reference/databricks-views.md)
