# Database standard

This file is the database standard. A new project follows it from the first table. An existing database is audited against it. The rules are the Postgres practice shared by the Copinance family: one database per owner, schema-qualified names, and an index only for a measured access path. A project cites this path from `AGENTS.md` and lists exceptions. Do not paste these rules into a second style guide.

Postgres 18. Names are unquoted snake_case, so they fold to lower case. An identifier stays within 63 characters. A name that would be longer keeps a shorter spelling that still starts with its prefix and the table.

## D1. Contexts

A database has one owner. The database name is that owner. Three kinds of data stay apart when more than one exists.

| Context | Holds | Stays out |
|---------|-------|-----------|
| Person and access | The account, sessions, grants, invitations, the product list, prices | A product's ledger, world facts, document bytes |
| Product | The records a person decided inside this product | Another product's tables, writes of world facts |
| World facts | What a source published, and the collection state for those facts | User ids, portfolio ids, quantities, costs, scores |

One product with no shared fact store is one database. A later product gets its own database, its own role, and its own Alembic chain. It reads another product through that product's API, or through a contract whose copy then lives in the receiver's database.

Each dataset has one class, and the class decides the database.

| Class | Where it lives |
|-------|----------------|
| Source observation or reference | The fact database, once identity, units, provenance, and retention are decided |
| Derived value | The product that computes it. The fact database keeps the inputs |
| Product decision | That product's database |
| Operational cache or coordination | The service that uses it. A cache is a copy, and the source row remains |

A conversation or another document with its own expiry may live in a document store. The relational database remains the system of record for the three contexts. Keys in Redis or a document store start with the service name. A queue key has no TTL. A cache, a rate limit, and a session document have a TTL. Sessions, grants, and prices that are the system of record stay in Postgres.

## D2. Schemas

The application schema has the database's name and is owned by the owner role. `public` holds extensions and the Alembic version table `alembic_version_<db>`.

A second schema in the same database is a different class of payload, owned by the same role, and named for that class. Document bytes are that case. The row stores the source id, the content hash, the size, and the provenance. Bytes that are kept are stored by content hash, so the same file is stored once.

## D3. References across databases

A foreign key stays inside one database. A reference to one fixed other system is an opaque id named for that system (`identity_user_id`, `paddle_customer_id`). When the source varies, the columns are `source` and `external_id`.

A code that can be renamed or reused is a dated attribute. It is a primary key when it is permanent and is the lookup itself (`product_code`). A ticker, a symbol, or any other alias that changes over time is a row of its own, with a validity interval, and the entity it names has `id`.

## D4. Roles

The owner role is the writer. A second context that only reads receives `SELECT` on the tables it may see, and `USAGE` on the schema. A context that may ask the owner to do work receives `EXECUTE` on those functions and no table privileges. The function checks its arguments. The caller's identity is the database role, read from `session_user` when the row must record who asked.

Grants name the role. They are in the migration that introduces the second context. A new project with one writer adds the reader and the requester when that second context exists.

## D5. Tables and columns

Tables are plural snake_case. The name says what one row is. A per-day grain starts with `daily_`. A header row for one derived series names the series and ends in `_builds` when the days are a child table. Operational status rows end in `_states`. A table that belongs to one country or source family carries that prefix (`tr_`, `us_`).

| Kind | Column |
|------|--------|
| Foreign key | `<entity>_id` |
| Business code | Ends in `_code` |
| Rate or share | A fraction named `*_fraction`. A source percent is converted at the writer |
| Count | `*_count`, `integer` or `bigint` |
| Position in a parent | `line_index` or `item_index` |
| Closed set of our values | Lower-case `text` in a column named `*_type` |
| A source's own code | The source's spelling. The column is `kind` when it is the source's classification |
| Currency pair | `base_currency` and `quote_currency`, in the market's BASE/QUOTE order |
| ISO currency | `text` matching `^[A-Z]{3}$` |
| Free text | `text`. A maximum length is a `CHECK` when the limit is a business rule |

`NOT NULL` is on every column the row cannot do without. A server default covers a value the database knows (`now()`, `uuidv7()`). The application supplies a value the database cannot know.

## D6. Keys

An entity table has `id uuid DEFAULT uuidv7() NOT NULL`. The default lives in the database, so inserts stay clustered by time. The application mints the id only when the row must exist before the insert returns.

A table whose natural key is complete, non-null, and stable uses that key and has no surrogate `id`. A line table is keyed by its parent and its position, so one index serves the key and the lookup. A natural key with a nullable part keeps `id`. A null stays null. A guessed stand-in is a wrong row.

A dimension that is referenced by the largest fact tables may use `bigint GENERATED BY DEFAULT AS IDENTITY` when the extra bytes of a uuid were measured on those tables and their indexes. The migration records the measurement.

## D7. Constraint and index names

Every constraint and index has an explicit name.

| Object | Name |
|--------|------|
| Primary key | `pk_<table>` |
| Foreign key | `fk_<table>_<columns>` |
| Unique | `uq_<table>_<columns>`, every key column in key order |
| Unique expression | `uq_<table>_<what>`, as in `uq_users_email_lower` on `lower(email)` |
| Check | `ck_<table>_<condition>`. A check whose name ends in a column name tests that column |
| Exclusion | `ex_<table>_<what>` |
| Index | `ix_<table>_<columns>` |

A writer that uses `ON CONFLICT ON CONSTRAINT` names a constraint that exists in the migration. A renamed constraint is a failed write the first time it runs.

## D8. Types and invariants

An unknown value is `NULL`. A writer stores the source's amount, unit, and identity. A row that cannot be mapped is an error, counted and listed. It is not inserted with a filled-in identity.

Money, quantities, and rates are `NUMERIC`. Instants are `timestamptz`, stored in UTC. A calendar day is `date`. A closed set is `text` plus a named `CHECK`, so a later revision extends the list by replacing the constraint.

A `CHECK` refuses a row whose parts disagree. A price that cannot be negative says so. A range whose low is above its high is refused. Two columns that are a pair are both set or both null. The writer surfaces the refusal. It does not retry with a silent default.

Every foreign key is `ON UPDATE RESTRICT ON DELETE RESTRICT`. A parent that still has children cannot be deleted, and a key cannot be rewritten underneath them.

A rule that must hold no matter who writes is a constraint in the database. Application code detects a problem and records the evidence. A person confirms a fact the stored data cannot prove. Confirmation is a column the person sets, with its source and its time, and a `CHECK` requires all three together.

## D9. Time columns and versions

A fact read from a source has `fetched_at timestamptz NOT NULL` and no `created_at` or `updated_at`. Every update of that row is a re-read, so a second clock would repeat `fetched_at`. A line table has none of the three. Its parent carries the time.

A row written by a person or the product has `created_at timestamptz NOT NULL DEFAULT now()`. `updated_at` is present where such a row changes. One function, `<db>.set_updated_at`, assigns `now()`, and each of those tables has a `BEFORE UPDATE` trigger named `<table>_set_updated_at`. Statements leave `updated_at` alone.

A fact that is read again uses one policy. The table's comment or the migration docstring names it.

| Policy | Use | Key |
|--------|-----|-----|
| Overwrite | The newest reading is enough. This is the default | The fact's natural key. `fetched_at` shows when the source was read |
| Revisions | A reader needs the value that was known at an earlier time | `fetched_at` is part of the key. A new row is written only when the content differs from the newest row, under an advisory lock per fact |
| Snapshots | Each reading differs by nature | Each reading is a row. Retention removes rows outside the window |

A change that is later reverted is a new revision. A collector that skips a period it already holds does not see a restatement. That choice is the revisions policy with the skip written down, or it is overwrite.

## D10. Indexes

An index exists for one named access path. The primary key or a unique constraint that already starts with those columns is that path's index. A second index on the same leading columns is not created.

Every foreign-key column has an index, so a parent delete can find the children. A nullable foreign key that is null on most rows uses a partial index `WHERE <column> IS NOT NULL`. A foreign key whose parent row is never deleted may omit the index when `EXPLAIN` shows the index is only write cost. The omission and the measurement stay in the migration comment.

| Access path | Index |
|-------------|-------|
| Newest rows for one parent | `(parent_id, <time> DESC)` |
| One date across parents | A single column on that date, when the plan uses it |
| A rare state | Partial, `WHERE state = '…'` or `WHERE revoked_at IS NULL` |
| A lookup the partition key already prunes | No extra index |

Before an index is added, take the query from `pg_stat_statements` or from the call site and compare `EXPLAIN (ANALYZE, BUFFERS)` with and without it. Before an index is dropped, read `pg_stat_user_indexes.idx_scan` after a full cycle of real use. The change reports both numbers, and the size of the index next to the size of the table.

An index on a table that already serves traffic is created `CONCURRENTLY`, outside the migration's transaction. On an empty database the migration creates it inside the transaction.

## D11. Growth

A table that grows fastest and is read by time is range-partitioned by month on that time column. The primary key and every unique constraint include the partition key. There is no default partition. A row whose month has no partition fails the insert, so a missing month is an error. Readers query the parent table. A daily job creates the partitions for the coming months and drops month partitions that have aged out of the retention window. The same job runs `ANALYZE` on the parent, because autovacuum does not analyze a partitioned table.

Retention is a named job with a window per table. A table that exists to keep history has no window. Dropping a month partition is the delete. A row-by-row delete of an expired month is the path a partition was meant to avoid.

A table that is updated constantly sets a lower `fillfactor` and a lower autovacuum scale factor. A large append-mostly table sets a lower autovacuum scale factor than the server default. The migration records the numbers. A crash drops planner statistics, so a worker that reads a large table runs `ANALYZE` when that table reports no rows.

A derived table stores a fingerprint of the inputs it was built from. The reader uses the stored rows while the fingerprint matches and otherwise computes the same answer. The fact database does not gain a column for the derivation.

## D12. Migrations

Alembic is the schema authority. A running application does not call `create_all`. The version table is `alembic_version_<db>` in `public`, so two chains on one server do not share `alembic_version`.

The migration connection pins `search_path=public`. A login role whose name matches a schema would otherwise put that schema first on the path, and Alembic's comparison would miss it. Every object in a revision is schema-qualified (`<db>.<table>`).

Revisions are numbered from `0001`. An applied revision is immutable. The next change is the next file. One revision is one change, and its message says what and why. The upgrade takes a transaction-scoped advisory lock. The lock constant is recorded next to the version table name, and it is different per database.

When `alembic_version_<db>` names a revision this tree does not contain, the run stops and leaves the table as it is.

A revision that deletes or rewrites stored data states the predicate, counts the rows before it changes them, copies what it keeps before it drops a table, and refuses a row it cannot map. The docstring says what the downgrade cannot put back. A downgrade does not invent amounts, units, or identities. The init revision's downgrade drops the schema only on a throwaway database. It refuses while any application table holds rows, unless the docstring records that the drop itself is the downgrade and names the data it removes.

The init script creates the role, the database, and the schema, owned by the role, on an empty volume. The first revision also runs `CREATE SCHEMA IF NOT EXISTS <db> AUTHORIZATION <db>`, so the script and the migration agree in either order.

A function sets `search_path` to `pg_catalog` and the application schema. An extension the schema needs is created in `public` by the revision that needs it.

Autogenerate misses `NUMERIC` precision, server defaults, and check constraints. The generated file is read against this contract before it is applied. A proof on a clone is: upgrade, downgrade one step, upgrade, then `alembic check` reports no drift. A destructive proof uses a backup of that clone.

## D13. Connections

Each process uses a small pool. `(pool size + overflow) × processes` stays under `max_connections`, with headroom for the migration and an admin session. The project records the pool sizes.

A request path sets `statement_timeout`. A worker that runs a long read sets its own, higher, timeout. A migration sets `lock_timeout`, so a lock it cannot take fails the revision. Idle transactions are ended by `idle_in_transaction_session_timeout`. The project records the durations.

Application SQL uses bound parameters. A screen that needs many parents loads them in one query and groups them in the application. A page load reads stored rows. It does not call a provider, and it does not run the retention job.

## A new project's first database

The scaffold is one role, one database, one schema, and `alembic_version_<db>` in `public`. Reader and requester roles, a second schema, partitions, and retention arrive with the context or the table that needs them. D5 through D10 apply to the first table.

A project with no database records that under `## Exceptions`. It does not gain an empty schema to satisfy this contract.

## Evidence

D1–D4: the database list, the schemas, and the grants. D5–D10: the migration SQL. D11: the partition and retention job. D12: `alembic/env.py`, the version table, and an unknown-revision refusal. D13: pool settings and timeouts. A rule that passes still cites the file that shows it.
