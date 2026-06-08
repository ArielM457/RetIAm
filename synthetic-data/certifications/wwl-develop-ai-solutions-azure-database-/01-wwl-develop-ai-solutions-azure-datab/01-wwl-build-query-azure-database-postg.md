# Build and query with Azure Database for PostgreSQL

> Curso: Develop AI solutions with Azure Database for PostgreSQL (wwl-develop-ai-solutions-azure-database-postgresql) · Seccion: Develop AI solutions with Azure Database for PostgreSQL
> Duracion estimada: 89 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

AI applications and data\-driven services require reliable, scalable database solutions to store and retrieve information efficiently. This module guides you through building applications with Azure Database for PostgreSQL to enable persistent data storage, complex querying, and seamless application integration for your AI solutions.

Imagine you're a developer building an AI agent that assists users with research tasks. Your agent needs to maintain conversation history across sessions, track multi\-step task progress, and store structured data that informs its decision\-making. The client expects the system to handle thousands of concurrent users, maintain sub\-second query response times for context retrieval, and support complex queries across conversation histories.

You chose PostgreSQL for its rich feature set, including JSON support for flexible schemas, robust transactional guarantees, and an extensive extension ecosystem. However, managing database infrastructure, ensuring high availability, handling backups, and scaling to meet demand requires significant operational overhead. The client also requires enterprise\-grade security with Microsoft Entra integration for identity management.

Azure Database for PostgreSQL provides a fully managed PostgreSQL experience that eliminates infrastructure management while delivering the control and flexibility developers need. The service handles patching, backups, and high availability automatically, letting you focus on building your application logic rather than maintaining database infrastructure.

After completing this module, you'll be able to:

* Explain the architecture and key features of Azure Database for PostgreSQL
* Establish secure connections to PostgreSQL using Microsoft Entra authentication and TLS
* Create and manage database schemas including tables, indexes, and constraints
* Write efficient SQL queries for common data operations
* Integrate Azure Database for PostgreSQL into applications using Python

---

## Explore Azure Database for PostgreSQL

Azure Database for PostgreSQL is a fully managed database service for PostgreSQL workloads on Azure. Understanding the service architecture, compute tiers, and managed capabilities helps you make informed decisions about configuration and capacity planning for your AI applications.

### What is Azure Database for PostgreSQL?

Azure Database for PostgreSQL is a fully managed relational database service based on the open\-source PostgreSQL database engine. The service runs the community edition of PostgreSQL, providing full compatibility with existing PostgreSQL applications and tools. Microsoft manages the underlying infrastructure, including hardware provisioning, software patching, backup management, and high availability configuration.

The service provides granular control over database configuration while maintaining the benefits of a managed platform. You can customize maintenance windows, configure high availability options, and adjust compute resources to match your workload requirements.

For AI applications that need relational data storage alongside vector operations, PostgreSQL offers a compelling combination of transactional reliability, flexible data modeling with JSONB, and an extension ecosystem that includes vector similarity search capabilities.

### Architecture and deployment options

Azure Database for PostgreSQL separates compute and storage into independent components. The database engine runs on a Linux virtual machine, while data files reside on Azure managed storage. This separation enables independent scaling of compute and storage resources and provides built\-in data durability through locally redundant storage replicas.

The service offers three compute tiers to match different workload characteristics. Each provides different CPU and memory configurations:

* **Burstable:** Provides baseline CPU performance with the ability to burst above the baseline when needed. Best suited for development environments, small applications, and workloads that don't need continuous full CPU capacity. The B\-series virtual machines offer a cost\-effective option for intermittent workloads.
* **General Purpose:** Delivers balanced compute and memory resources for production workloads. The D\-series virtual machines provide consistent performance for applications requiring predictable response times. Choose General Purpose for typical web applications and backend services.
* **Memory Optimized:** Offers high memory\-to\-vCPU ratios for workloads that benefit from large in\-memory datasets. The E\-series virtual machines excel at caching\-heavy workloads, complex analytical queries, and applications that need to keep large working sets in memory. AI applications performing in\-memory computations often benefit from this tier.

You can change compute tiers after deployment with a brief restart, allowing you to adjust resources as your workload evolves.

### Managed service capabilities

Azure Database for PostgreSQL handles operational tasks that would otherwise require dedicated database administration effort.

The service automatically creates backups of your database and stores them on zone\-redundant storage in regions that support availability zones, or locally redundant storage in regions that don't. Default backup retention is seven days, which you can extend up to 35 days based on your recovery requirements. Backups include both full snapshots and transaction logs, enabling point\-in\-time restore to any second within the retention period. Azure encrypts all backups using AES 256\-bit encryption, with platform\-managed keys by default or customer\-managed keys for additional control.

Point\-in\-time restore lets you recover your database to any moment within the backup retention period. The restore operation creates a new server instance with data recovered to the specified timestamp, which is useful for recovering from accidental data modifications or testing against a historical database state.

Azure Database for PostgreSQL includes built\-in PgBouncer, a lightweight connection pooler that reduces the overhead of establishing new database connections by maintaining a pool of reusable connections. You can enable PgBouncer through server configuration and connect on port 6432 instead of the standard PostgreSQL port 5432\. Connection pooling is valuable for AI applications that make many short\-lived database calls, such as storing individual messages or retrieving context for each inference request.

Important

PgBouncer is only available on General Purpose and Memory Optimized compute tiers. The Burstable tier doesn't support the built\-in PgBouncer feature.

Connection optimization strategies are covered in depth in the "Optimize performance, indexing, and scaling" module.

### Supported PostgreSQL versions and extensions

Azure Database for PostgreSQL supports multiple major PostgreSQL versions concurrently. The service typically supports the current major version and several previous versions, following PostgreSQL's community support timeline. You can check available versions when creating a new server or query the `server_version` setting on an existing server.

PostgreSQL's extension mechanism allows you to add functionality beyond the core database engine. Extensions can add new data types, functions, operators, and index types without modifying the core PostgreSQL code. Several extensions are relevant for AI applications:

* **pgvector:** Enables vector data types and similarity search operations. You can store embeddings alongside relational data and perform approximate nearest neighbor searches. The "Implement vector search with Azure PostgreSQL" module covers pgvector in detail.
* **pg\_trgm:** Provides trigram\-based text similarity functions. Useful for fuzzy text matching, autocomplete features, and finding similar strings without exact matches.
* **hstore:** Adds a key\-value data type for storing sets of key\-value pairs within a single PostgreSQL value. Useful for semi\-structured data that doesn't require the full flexibility of JSONB.

You can enable extensions using the `CREATE EXTENSION` command after confirming the extension is available on your server instance.

### Developer decision points

When configuring Azure Database for PostgreSQL for your application, consider these key decisions:

* **Choosing a compute tier:** Select based on your workload's CPU and memory requirements. Start with Burstable for development, testing, and proof\-of\-concept work where cost optimization matters more than consistent performance. Use General Purpose for production workloads with steady, predictable resource requirements. Choose Memory Optimized when your application benefits from large in\-memory caches or performs complex analytical queries. You can monitor CPU and memory utilization after deployment and adjust the tier if needed.
* **Evaluating extensions:** Review available extensions early in your application design. Determine whether your application needs vector similarity search (pgvector), full\-text search, or geospatial capabilities (PostGIS). Verify that required extensions are available on Azure Database for PostgreSQL before committing to a design. Plan for extension upgrades as part of your database maintenance strategy.

### Additional resources

* [Azure Database for PostgreSQL documentation](/en-us/azure/postgresql/)
* [Service overview](/en-us/azure/postgresql/flexible-server/service-overview)
* [Compute and storage options](/en-us/azure/postgresql/flexible-server/concepts-compute-storage)
* [High availability concepts](/en-us/azure/postgresql/high-availability/concepts-high-availability)

---

## Connect to PostgreSQL

Establishing secure connections to Azure Database for PostgreSQL requires understanding connection string components, authentication options, and transport layer security configuration. For AI applications that frequently read and write data, getting connection configuration right from the start prevents authentication failures and security vulnerabilities in production.

### Connection fundamentals

PostgreSQL connections require several parameters that identify the server, database, and user credentials. Azure Database for PostgreSQL uses a specific endpoint format and enforces secure transport by default.

Your server endpoint follows the pattern `<server-name>.postgres.database.azure.com`, where `<server-name>` is the unique name you specified when creating the server. The fully qualified domain name (FQDN) resolves to the server's public IP address when using public access, or a private IP address when using VNet integration.

A PostgreSQL connection requires these core parameters: the host (server FQDN), port (5432 for direct connections or 6432 for PgBouncer), database name, username (for Entra auth, use `username@servername` format), password (static or Entra token), and SSL mode. Different client libraries and tools accept these parameters in various formats, including connection strings, keyword\-value pairs, or individual parameters.

### Authentication methods

Azure Database for PostgreSQL supports two authentication approaches: Microsoft Entra authentication provides stronger security through token\-based access, while PostgreSQL native authentication uses traditional username and password credentials.

Microsoft Entra authentication uses OAuth 2\.0 tokens instead of passwords. This approach integrates with Azure's identity platform and provides centralized identity management, eliminates password storage (tokens are short\-lived), supports managed identities for Azure\-hosted applications, and creates audit trails in Entra sign\-in logs. To use Entra authentication, configure a Microsoft Entra administrator on your server (a user account, group, or service principal). Once configured, Entra identities connect by obtaining a token from the `https://ossrdbms-aad.database.windows.net` resource.

The connection process works as follows:

1. Your application requests an access token from Microsoft Entra ID.
2. Entra validates the identity and returns a token.
3. Your application connects to PostgreSQL using the token as the password.
4. PostgreSQL validates the token against the configured Entra administrator.

In Python, you can use the `azure-identity` library to obtain tokens:

```
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
token = credential.get_token("https://ossrdbms-aad.database.windows.net/.default")
## Use token.token as the password in your connection string

```

The `DefaultAzureCredential` class automatically tries multiple authentication methods in order, including managed identity (when running on Azure), Azure CLI credentials (for local development), and other options.

PostgreSQL native authentication stores usernames and encrypted passwords in the database. This approach is appropriate when applications can't use Entra authentication (legacy applications), you need to grant access to identities outside your Entra tenant, or you're running in an environment without Azure connectivity during development. When using PostgreSQL authentication, store passwords in Azure Key Vault rather than application configuration, rotate passwords regularly, use strong randomly generated passwords, and limit the permissions of each database user. The administrator username and password you specify during server creation use PostgreSQL authentication.

### TLS/SSL configuration

Azure Database for PostgreSQL encrypts all connections using Transport Layer Security (TLS). The server requires TLS by default and supports TLS 1\.2 and 1\.3\. Connections using older TLS versions are rejected.

PostgreSQL clients use the `sslmode` parameter to control encryption and certificate validation. The available modes are:

* **disable:** No encryption. Azure rejects connections using this mode.
* **allow:** Encrypts if the server requires it, but doesn't validate certificates.
* **prefer:** Encrypts if the server supports it, but doesn't validate certificates.
* **require:** Enforces encryption but doesn't validate certificates.
* **verify\-ca:** Enforces encryption and validates the server certificate against trusted certificate authorities.
* **verify\-full:** Enforces encryption, validates the CA, and confirms the certificate hostname matches the server.

For production applications, use `verify-full` to ensure you're connecting to the genuine Azure PostgreSQL server. This mode validates that the server presents a certificate signed by a trusted certificate authority, and that the certificate's common name or subject alternative name matches the server hostname.

The `verify-ca` and `verify-full` modes require your client to have access to the root CA certificates that signed the server's certificate. Most operating systems and Azure hosting environments already include the DigiCert and Microsoft root CAs that Azure Database for PostgreSQL uses. If certificate validation fails, you might need to download the root certificates from Microsoft's PKI repository and configure your client to use them.

### Connection pooling with PgBouncer

Azure Database for PostgreSQL includes built\-in PgBouncer, which you can enable through the server's configuration settings in the Azure portal or using the Azure CLI. Once enabled, connect on port 6432 instead of 5432\.

Important

PgBouncer is only available on General Purpose and Memory Optimized compute tiers. If your server uses the Burstable tier, you can't enable built\-in PgBouncer.

PgBouncer maintains a pool of connections to the database server and multiplexes client connections onto this pool. This reduces the overhead of connection establishment, which is valuable for applications that make many short\-lived connections.

To enable PgBouncer using the Azure CLI:

```
az postgres flexible-server parameter set \
    --resource-group myResourceGroup \
    --server-name myserver \
    --name pgbouncer.enabled \
    --value true

```

After enabling, update your connection string to use port 6432:

```
postgresql://user@myserver.postgres.database.azure.com:6432/mydb?sslmode=require

```

Connection pooling optimization strategies, including pool sizing and transaction vs. session modes, are covered in the "Optimize performance, indexing, and scaling" module.

### Network access considerations

Azure Database for PostgreSQL supports two networking models: public access with firewall rules, and private access with VNet integration. Your platform or operations team typically configures these settings, but understanding them helps you troubleshoot connection issues.

With **public access**, the server has a public IP address and firewall rules control which client IPs can connect. If you can't connect from your development machine, verify that your IP address is allowed in the firewall rules.

With **private access**, the server has only a private IP address within an Azure Virtual Network. You can only connect from resources within the same VNet, peered networks, or through VPN/ExpressRoute. Private access is common in production environments where network isolation is required.

### Connection string examples

The following examples show common connection string patterns for Azure Database for PostgreSQL.

```
## Basic connection with SSL required
postgresql://myuser:mypassword@myserver.postgres.database.azure.com/mydb?sslmode=require

## Connection with certificate verification
postgresql://myuser:mypassword@myserver.postgres.database.azure.com/mydb?sslmode=verify-full&sslrootcert=/etc/ssl/certs/ca-certificates.crt

## Connection through PgBouncer (note port 6432)
postgresql://myuser:mypassword@myserver.postgres.database.azure.com:6432/mydb?sslmode=require

```

### Additional resources

* [Connect with TLS to Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/how-to-connect-tls-ssl)
* [Microsoft Entra authentication with PostgreSQL](/en-us/azure/postgresql/flexible-server/concepts-azure-ad-authentication)
* [Networking overview](/en-us/azure/postgresql/flexible-server/concepts-networking)
* [PgBouncer in Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/concepts-pgbouncer)

---

## Create and manage schemas

Database schema design determines how effectively your application stores and retrieves data. A well\-designed schema enforces data integrity through constraints, enables efficient queries through appropriate data types, and supports application evolution through thoughtful structure. For AI applications that store conversation history, task state, and metadata, schema design choices directly affect both performance and maintainability.

### Database and schema organization

PostgreSQL organizes objects in a hierarchy: a server instance contains databases, databases contain schemas, and schemas contain tables and other objects. Understanding this hierarchy helps you structure your application's data appropriately.

When you provision Azure Database for PostgreSQL, you create a server that can host multiple databases. Each database is an isolated container with its own tables, functions, and other objects. Connections target a specific database, and queries can't directly access objects in other databases on the same server. Within a database, schemas provide a namespace for organizing objects. The default schema is `public`, which contains objects when you don't specify a schema name. You can create more schemas to separate logical components of your application, isolate tenants in a multitenant application, or group related objects for easier permission management.

Use separate databases when you need complete isolation between datasets, when different applications share the same server but shouldn't access each other's data, or when you want independent backup and restore capabilities. Use separate schemas within a database when related objects need to reference each other through foreign keys, when you want to run queries that join data across the namespaces, or when you're implementing logical separation without full isolation. For most AI applications, a single database with the default `public` schema is sufficient.

### Create tables

Tables store your application's data in rows and columns. The `CREATE TABLE` statement defines the table structure, including column names, data types, and constraints.

A table definition specifies each column's name and data type, along with optional constraints that enforce data integrity rules. When you design tables for AI applications, consider what data you need to store, how you query that data, and what relationships exist between different entities:

```
CREATE TABLE conversations (
    id BIGSERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb
);

```

This example creates a table for storing AI agent conversation sessions with an auto\-incrementing primary key (`BIGSERIAL PRIMARY KEY`), required fields that can't be null, timestamp fields with automatic defaults, and a JSONB column for flexible metadata storage.

Every table should have a primary key that uniquely identifies each row. Serial columns auto\-generate sequential integers (`SERIAL` for 32\-bit, `BIGSERIAL` for 64\-bit). UUID columns provide universally unique identifiers with `DEFAULT gen_random_uuid()`. Composite keys combine multiple columns when no single column is unique. For AI applications with high insert volumes, `BIGSERIAL` provides simple, sequential identifiers. Use UUIDs when you need to generate identifiers outside the database or merge data from multiple sources.

Constraints enforce rules about what data can be stored. `NOT NULL` prevents null values. `DEFAULT` provides a value when none is specified. `CHECK` validates values against a condition (like `CHECK (status IN ('pending', 'completed'))`). `UNIQUE` ensures no duplicate values. PostgreSQL checks these rules whenever you insert or update data, catching errors at the database level.

### Data types for AI applications

Choosing appropriate data types affects storage efficiency, query performance, and application flexibility. Several data types are relevant for AI workloads:

* **JSONB:** Stores JSON data in a binary format that supports indexing and efficient querying. Use JSONB when data structure varies between records, you need to store nested objects or arrays, or schema flexibility is more important than strict typing. You can query JSONB fields using PostgreSQL's JSON operators.
* **TEXT and VARCHAR:** Both store variable\-length character strings. `TEXT` has no length limit, while `VARCHAR(n)` enforces a maximum. In PostgreSQL, there's no performance difference between `TEXT` and unconstrained `VARCHAR`. Use `VARCHAR(n)` when you want the database to enforce a maximum length.
* **TIMESTAMP WITH TIME ZONE:** Always use `TIMESTAMPTZ` for temporal data in applications that might operate across time zones. PostgreSQL stores timestamps in UTC and converts them based on the session's time zone setting when displaying.
* **BYTEA:** Stores binary data as a byte array. Use it for small binary objects that need to be stored alongside relational data. For large binary files, consider Azure Blob Storage with a reference in the database.
* **SERIAL and BIGSERIAL:** Pseudo\-types that create auto\-incrementing integer columns. PostgreSQL automatically creates a sequence and sets the default. Use `BIGSERIAL` for tables that might exceed two billion rows.

### Define relationships

Foreign keys establish relationships between tables and enforce referential integrity. When you define a foreign key, PostgreSQL ensures that values in the referencing column exist in the referenced table.

A one\-to\-many relationship connects a single row in one table to multiple rows in another. This pattern appears frequently in AI applications: one conversation has many messages; one user has many sessions; one task has many checkpoints. Implement this using a foreign key in the "many" table that references the primary key in the "one" table:

```
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    conversation_id BIGINT NOT NULL REFERENCES conversations(id),
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

```

Referential actions define what happens when you delete or update a referenced row. `RESTRICT` (the default) prevents the operation if referenced rows exist. `CASCADE` automatically deletes or updates all referencing rows. `SET NULL` sets the foreign key to NULL. `SET DEFAULT` sets it to the default value. Use `ON DELETE CASCADE` carefully—deleting a conversation automatically deletes all messages, which can remove more data than intended if relationships are complex.

Many\-to\-many relationships require a junction table that references both related tables. For example, conversations can have multiple tags, and tags can apply to multiple conversations:

```
CREATE TABLE conversation_tags (
    conversation_id BIGINT REFERENCES conversations(id) ON DELETE CASCADE,
    tag_id BIGINT REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (conversation_id, tag_id)
);

```

The composite primary key ensures each combination appears only once.

### Index basics

Indexes are data structures that speed up data retrieval at the cost of more storage and slower writes. PostgreSQL creates indexes automatically for primary keys and unique constraints. You create other indexes to optimize specific queries.

B\-tree is the default index type and works well for equality and range comparisons on most data types. These indexes organize data in a sorted tree structure, enabling fast lookups for exact matches and range queries. Create indexes on columns that appear frequently in `WHERE` clauses, `JOIN` conditions, and `ORDER BY` clauses:

```
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);

```

The order of columns in a composite index matters. The index can satisfy queries that filter on the leading columns but not queries that filter only on trailing columns.

Indexes improve read performance but come with costs. Every index consumes disk space and adds overhead to inserts, updates, and deletes. For AI applications that write frequently (storing every message, for example), be selective about which indexes you create. Monitor query performance and add indexes when you identify slow queries that would benefit. For information on optimizing vector indexes, visit [Optimize vector search in Azure Database for PostgreSQL](/en-us/training/modules/optimize-vector-search-azure-database-postgresql/).

### Schema management commands

As your application evolves, you need to modify table structures without losing existing data.

The `ALTER TABLE` command modifies existing tables. You can add columns (`ADD COLUMN`), add constraints (`ALTER COLUMN ... SET NOT NULL`), or remove columns (`DROP COLUMN`). Some operations acquire locks that block other operations, so plan schema changes carefully for production databases. Adding a column with a default value is efficient in PostgreSQL—the database stores the default in the system catalog rather than updating every existing row.

The `DROP TABLE` command permanently removes a table and all its data. This operation can't be undone outside of a transaction. PostgreSQL protects you from breaking relationships by preventing drops when other tables reference the target through foreign keys. Use `CASCADE` to automatically drop foreign key constraints, but do so carefully—it might affect tables you didn't intend to modify.

Wrap schema changes in transactions when you need to make multiple related changes atomically:

```
BEGIN;
ALTER TABLE conversations ADD COLUMN category VARCHAR(100);
CREATE INDEX idx_conversations_category ON conversations(category);
COMMIT;

```

If any statement fails, you can `ROLLBACK` to leave the schema unchanged. Most DDL statements in PostgreSQL are transactional, unlike some other databases.

### Additional resources

* [PostgreSQL data types documentation](https://www.postgresql.org/docs/current/datatype.html)
* [CREATE TABLE reference](https://www.postgresql.org/docs/current/sql-createtable.html)
* [Indexes in PostgreSQL](https://www.postgresql.org/docs/current/indexes.html)

---

## Query data

This unit covers PostgreSQL\-specific query features and patterns that are essential for AI applications. The unit focuses on PostgreSQL's unique capabilities and advanced patterns for managing conversation history, processing state, and application metadata.

This unit assumes familiarity with standard SQL concepts like `SELECT`, `WHERE`, joins, and aggregation. If you need a refresher, the [Get started querying with Transact\-SQL](/en-us/training/paths/get-started-querying-with-transact-sql/) learning path is a good resource.

### Query execution and alias scope

Even experienced SQL developers get tripped up by execution order, particularly when using column aliases. SQL statements execute in a specific logical order that differs from how you write them, and understanding this order helps you troubleshoot cryptic "column doesn't exist" errors.

| Order | Clause | Purpose |
| --- | --- | --- |
| 1 | `FROM` | Identify source tables |
| 2 | `WHERE` | Filter rows |
| 3 | `GROUP BY` | Group rows for aggregation |
| 4 | `HAVING` | Filter groups |
| 5 | `SELECT` | Choose columns and compute expressions |
| 6 | `ORDER BY` | Sort results |
| 7 | `LIMIT` / `OFFSET` | Restrict result count |

**Alias scope rule:** Column aliases defined in `SELECT` are only visible to clauses that execute *after* `SELECT`—namely `ORDER BY` and `LIMIT`/`OFFSET`. Clauses that execute earlier (`WHERE`, `GROUP BY`, `HAVING`) can't reference these aliases because they aren't defined yet.

This means you can't filter by an alias in `WHERE`, but you can sort by one in `ORDER BY`:

```
-- This FAILS: WHERE executes before SELECT, so 'msg_date' doesn't exist yet
SELECT DATE(created_at) AS msg_date, content
FROM messages
WHERE msg_date > '2024-01-01';  -- Error: column "msg_date" does not exist

-- This WORKS: repeat the expression in WHERE
SELECT DATE(created_at) AS msg_date, content
FROM messages
WHERE DATE(created_at) > '2024-01-01';

-- This also WORKS: ORDER BY executes after SELECT, so aliases are available
SELECT DATE(created_at) AS msg_date, content
FROM messages
WHERE DATE(created_at) > '2024-01-01'
ORDER BY msg_date;

```

### PostgreSQL\-specific filtering

PostgreSQL extends standard SQL with operators that simplify common filtering tasks. These features are useful for AI applications that need flexible text search and structured metadata queries.

The `ILIKE` operator provides case\-insensitive pattern matching without requiring functions like `LOWER()`. This is useful for user\-facing search features where you want to match regardless of capitalization: `SELECT * FROM messages WHERE content ILIKE '%error%'`.

PostgreSQL lets you control where `NULL` values appear in sorted results using `NULLS FIRST` or `NULLS LAST`. By default, `NULL` values sort as if larger than any other value. Use `ORDER BY ended_at NULLS LAST` to keep incomplete conversations at the end, or `ORDER BY completed_at NULLS FIRST` to show unprocessed tasks first.

The `COALESCE` function returns the first non\-null value from its arguments. Use it to provide default values in query results (`COALESCE(title, 'Untitled')`) or to handle nullable columns in expressions.

### Query JSONB data

PostgreSQL's JSONB type stores structured data that doesn't fit a fixed schema. AI applications commonly use JSONB for metadata, configuration, model parameters, and variable response structures. PostgreSQL provides specialized operators for extracting values, checking structure, and filtering based on JSON content.

Use `->` to extract a JSON element as JSON, or `->>` to extract it as text (for comparisons and display). For nested paths, use `#>` (returns JSON) or `#>>` (returns text). For example, `metadata->>'status'` extracts the status field as text, while `checkpoint_data#>>'{results,0,score}'` navigates a nested path to get a specific value.

Existence and containment operators enable efficient filtering. The `?` operator checks for key existence (`WHERE metadata ? 'priority'`), while `@>` tests containment (`WHERE checkpoint_data @> '{"status": "completed"}'`). These operators can use GIN indexes for efficient filtering on large tables.

When JSONB columns contain arrays, use `jsonb_array_elements` to expand them for filtering or aggregation:

```
-- Find conversations tagged with 'support'
SELECT DISTINCT c.*
FROM conversations c,
     jsonb_array_elements_text(c.metadata->'tags') AS tag
WHERE tag = 'support';

```

### Efficient pagination with keyset pagination

Traditional `OFFSET`\-based pagination becomes slow on large tables because PostgreSQL must scan and discard all skipped rows. Page 1,000 with 20 rows per page requires scanning 20,000 rows and discarding 19,980\. Keyset pagination (also called cursor\-based pagination) uses `WHERE` clauses to skip rows, which performs consistently regardless of how deep you paginate.

Instead of tracking page numbers, track the last value you saw and filter from there. This approach requires a unique, sortable column (or combination of columns):

```
-- First page: get the 20 most recent messages
SELECT id, conversation_id, content, created_at
FROM messages
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Next page: filter by the last seen timestamp and id
SELECT id, conversation_id, content, created_at
FROM messages
WHERE (created_at, id) < ('2024-06-15 10:30:00', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;

```

Including `id` in both the `ORDER BY` and `WHERE` clauses handles ties when multiple rows have the same timestamp. Your application stores the last row's sort values and passes them to the next query. For ascending order, change `<` to `>` and `DESC` to `ASC`.

### Common Table Expressions (CTEs)

CTEs define named temporary result sets that exist only during the execution of a query. They improve readability by letting you build complex queries step by step, and they enable recursive queries for hierarchical data.

Use CTEs to break complex queries into logical steps. Each CTE can reference previously defined CTEs, creating a pipeline of transformations:

```
WITH recent_conversations AS (
    SELECT id, user_id, started_at
    FROM conversations
    WHERE started_at > CURRENT_DATE - INTERVAL '7 days'
),
message_stats AS (
    SELECT conversation_id, COUNT(*) AS message_count, MAX(created_at) AS last_message_at
    FROM messages
    GROUP BY conversation_id
)
SELECT rc.user_id, rc.started_at, COALESCE(ms.message_count, 0) AS message_count
FROM recent_conversations rc
LEFT JOIN message_stats ms ON rc.id = ms.conversation_id;

```

Recursive CTEs query tree structures like task hierarchies, organizational charts, or threaded conversations. They consist of a base case (anchor) and a recursive case that references the CTE itself. Always include a depth limit or other termination condition to prevent infinite loops if your data contains cycles:

```
WITH RECURSIVE task_tree AS (
    -- Base case: start with the parent task
    SELECT id, parent_id, title, 1 AS depth
    FROM tasks WHERE id = 1
    UNION ALL
    -- Recursive case: find children of current level
    SELECT t.id, t.parent_id, t.title, tt.depth + 1
    FROM tasks t
    INNER JOIN task_tree tt ON t.parent_id = tt.id
    WHERE tt.depth < 10
)
SELECT * FROM task_tree ORDER BY depth, id;

```

AI applications often need to retrieve conversation threads where messages reference parent messages:

```
WITH RECURSIVE thread AS (
    -- Start with the root message
    SELECT id, parent_id, content, role, 0 AS depth
    FROM messages
    WHERE id = :root_message_id

    UNION ALL

    -- Get all replies
    SELECT m.id, m.parent_id, m.content, m.role, t.depth + 1
    FROM messages m
    INNER JOIN thread t ON m.parent_id = t.id
    WHERE t.depth < 50
)
SELECT * FROM thread ORDER BY depth, id;

```

### INSERT with RETURNING

PostgreSQL's `RETURNING` clause retrieves values from inserted, updated, or deleted rows in a single round trip. This is essential for getting autogenerated IDs, timestamps, or computed defaults without a separate query.

```
-- Get the generated ID after inserting a conversation
INSERT INTO conversations (user_id, session_id)
VALUES ('user123', 'sess_abc')
RETURNING id;

-- Get multiple generated values
INSERT INTO messages (conversation_id, role, content)
VALUES (1, 'user', 'Hello')
RETURNING id, created_at;

-- Use RETURNING with UPDATE
UPDATE tasks SET status = 'completed', completed_at = CURRENT_TIMESTAMP
WHERE id = 5
RETURNING id, status, completed_at;

```

### Upserts with ON CONFLICT

The `INSERT ... ON CONFLICT` clause handles unique constraint violations, enabling "upsert" operations that insert new rows or update existing ones. This pattern is valuable for idempotent operations and state management in AI applications.

When a conflict occurs on a unique constraint, you can update the existing row with new values using `DO UPDATE`. The `EXCLUDED` pseudo\-table references the values that would have been inserted:

```
INSERT INTO user_preferences (user_id, preference_key, preference_value)
VALUES ('user123', 'theme', 'dark')
ON CONFLICT (user_id, preference_key)
DO UPDATE SET
    preference_value = EXCLUDED.preference_value,
    updated_at = CURRENT_TIMESTAMP;

```

Use `DO NOTHING` to silently skip rows that would violate constraints: `INSERT INTO tags (name) VALUES ('important') ON CONFLICT (name) DO NOTHING`.

You can add a `WHERE` clause to `DO UPDATE` for conditional logic, updating only when the new value differs from the existing one. Combine `ON CONFLICT` with `RETURNING` to know whether a row was inserted or updated—the expression `(xmax = 0)` returns `true` for newly inserted rows and `false` for updated rows.

### Practical patterns for AI applications

These patterns combine the features covered earlier into solutions for common AI application requirements. The following query retrieves conversation history with metadata for context building:

```
WITH conversation_context AS (
    SELECT c.id, c.session_id, c.metadata->>'model' AS model
    FROM conversations c
    WHERE c.session_id = :session_id AND c.ended_at IS NULL
)
SELECT cc.session_id, cc.model, m.role, m.content, m.created_at
FROM conversation_context cc
INNER JOIN messages m ON cc.id = m.conversation_id
ORDER BY m.created_at
LIMIT 50;

```

The following example shows recording task checkpoints with state management using upsert:

```
INSERT INTO task_checkpoints (task_id, step_number, checkpoint_data)
VALUES (:task_id, :step_number, :checkpoint_json::jsonb)
ON CONFLICT (task_id, step_number)
DO UPDATE SET checkpoint_data = EXCLUDED.checkpoint_data, updated_at = CURRENT_TIMESTAMP
RETURNING id, created_at, (xmax = 0) AS is_new;

```

The following example shows a paginated search with JSONB filters:

```
SELECT c.id, c.session_id, c.started_at, c.metadata->>'status' AS status
FROM conversations c
WHERE c.user_id = :user_id
  AND c.metadata @> :filter_json::jsonb
  AND (c.started_at, c.id) < (:last_started_at, :last_id)
ORDER BY c.started_at DESC, c.id DESC
LIMIT 20;

```

### Additional resources

* [PostgreSQL JSON functions and operators](https://www.postgresql.org/docs/current/functions-json.html)
* [PostgreSQL INSERT documentation](https://www.postgresql.org/docs/current/sql-insert.html)
* [PostgreSQL WITH queries (CTEs)](https://www.postgresql.org/docs/current/queries-with.html)

---

## Integrate SDKs and applications

Integrating Azure Database for PostgreSQL into your applications requires choosing appropriate client libraries, managing connections effectively, and handling errors gracefully. This unit covers SDK integration patterns for Python, along with best practices that apply across programming languages.

Note

Code examples in this unit demonstrate patterns for integrating PostgreSQL with your applications. The `psycopg` library is updated frequently. Visit the [psycopg documentation](https://www.psycopg.org/psycopg3/docs/) for the most current API details and best practices.

### Python integration with psycopg

The `psycopg` library (version 3\) is the recommended PostgreSQL adapter for Python. It provides both synchronous and asynchronous interfaces, connection pooling, and full support for PostgreSQL features.

Install psycopg using pip with the binary extra for the simplest setup: `pip install "psycopg[binary]"`. The binary distribution includes pre\-compiled dependencies, which avoids the need to install PostgreSQL client libraries on your development machine. For production deployments where you need to compile against specific PostgreSQL client libraries, install without the binary extra and ensure `libpq` development headers are available.

Create connections using `psycopg.connect()` with either a connection string or individual parameters. Connection strings are convenient for configuration files, while individual parameters offer flexibility for computing values programmatically, such as retrieving passwords from Key Vault:

```
import psycopg

## Connection string format
conn = psycopg.connect("postgresql://user:password@myserver.postgres.database.azure.com/mydb?sslmode=require")

## Individual parameters
conn = psycopg.connect(host="myserver.postgres.database.azure.com", dbname="mydb",
                       user="myuser", password="mypassword", sslmode="require")

```

Context managers ensure connections are properly closed, even when exceptions occur. The outer `with` block manages the connection, and the inner `with` block manages the cursor:

```
with psycopg.connect(connection_string) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM conversations WHERE id = %s", (conversation_id,))
        row = cur.fetchone()

```

Always use parameterized queries to prevent SQL injection attacks. Parameterized queries separate the SQL structure from the data values, letting the database driver handle proper escaping. Use `%s` placeholders for positional parameters or `%(name)s` for named parameters. Never use string formatting or concatenation to build queries with user input.

Retrieve query results using cursor methods that match your needs. Use `fetchone()` when you expect a single row, `fetchall()` for small result sets, and iterate directly over the cursor for large results to avoid loading everything into memory at once.

### Connection management best practices

Effective connection management improves application reliability and performance regardless of the programming language you use.

Set appropriate timeouts to prevent your application from hanging when the database is unreachable or queries run longer than expected. Connection timeouts control how long the client waits to establish a connection, while statement timeouts limit query execution time. Choose timeout values based on your application's tolerance for latency—web applications typically use shorter timeouts (five to 30 seconds) than batch processing jobs.

```
conn = psycopg.connect(
    connection_string,
    connect_timeout=10,
    options="-c statement_timeout=30000"  # milliseconds
)

```

Implement retry logic with exponential backoff to handle transient failures from network issues, server restarts, or resource contention. Catch `OperationalError` for connection and timeout failures. Don't retry on constraint violations or syntax errors—those require code changes, not retries.

Always close connections when you're done with them. Leaked connections exhaust the connection pool and can prevent new connections. Context managers provide automatic cleanup that works even when exceptions occur.

### Error handling strategies

Database operations can fail for various reasons. Handling errors appropriately improves user experience and simplifies debugging.

Connection failures occur when the server is unreachable or rejects the connection—network problems, incorrect credentials, firewall rules, or server maintenance can all be causes. Handle connection failures by logging details for troubleshooting while presenting user\-friendly messages to end users.

Unique constraints, foreign keys, and check constraints raise specific errors when violated. Catch `UniqueViolation`, `ForeignKeyViolation`, and `CheckViolation` to provide meaningful feedback. Always roll back the transaction after a constraint violation.

Deadlocks occur when two transactions wait for each other's locks, creating a circular dependency. PostgreSQL automatically detects deadlocks and terminates one transaction. Your application should catch `DeadlockDetected`, roll back, and retry. To minimize deadlock risk, design transactions to acquire locks in a consistent order. Handle `LockNotAvailable` similarly when queries time out waiting for locks.

### Performance considerations

Application\-level patterns can significantly affect database performance.

Insert multiple rows in a single statement instead of executing individual inserts in a loop. Batch operations reduce network round trips, significantly improving throughput for bulk data operations. Use `executemany` for inserting hundreds to a few thousand rows. For larger datasets (10,000\+ rows), the `COPY` command provides the highest performance, often two to 10 times faster than individual inserts:

```
with cur.copy("COPY messages (conversation_id, role, content) FROM STDIN") as copy:
    for record in records:
        copy.write_row(record)

```

Prepared statements can improve performance for queries executed repeatedly with different parameters. The database parses and plans the query once, then reuses that plan. Most PostgreSQL drivers automatically use prepared statements for parameterized queries.

Creating new database connections is expensive—each requires network handshakes, authentication, and server\-side resource allocation. Use connection pools to maintain reusable connections that your application can borrow and return:

```
from psycopg_pool import ConnectionPool

pool = ConnectionPool(connection_string, min_size=1, max_size=10)

with pool.connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM messages WHERE conversation_id = %s", (id,))

```

### Additional resources

* [psycopg 3 documentation](https://www.psycopg.org/psycopg3/docs/)
* [Azure Identity client library for Python](/en-us/python/api/overview/azure/identity-readme)

---

## Exercise \- Build an agent tool backend on Azure Database for PostgreSQL

In this exercise, you create an Azure Database for PostgreSQL instance that serves as a tool backend for an AI agent. The database stores conversation context and task state that an agent can read and write during operation. You design a schema for agent memory, build Python functions that serve as agent tools, and test the complete workflow. This pattern provides a foundation for building AI agents that maintain persistent memory across sessions and can resume interrupted tasks.

Tasks performed in this exercise:

* Download project starter files and configure the deployment script
* Deploy an Azure Database for PostgreSQL Flexible Server with Microsoft Entra authentication
* Build Python tool functions for conversation and task state management
* Create a database schema for agent memory with tables for conversations, messages, and task checkpoints
* Test the agent memory workflow using a provided test script
* Query conversation context using SQL

This exercise takes approximately **30** minutes to complete.

### Before you start

To complete the exercise, you need:

* An Azure subscription with the permissions to deploy the necessary Azure services. If you don't already have one, you can [sign up for one](https://azure.microsoft.com/).
* [Visual Studio Code](https://code.visualstudio.com/) on one of the [supported platforms](https://code.visualstudio.com/docs/supporting/requirements#_platforms).
* The latest version of the [Azure CLI](/en-us/cli/azure/install-azure-cli).
* [Python 3\.12](https://www.python.org/downloads/) or greater.
* [PostgreSQL command\-line tools](https://www.postgresql.org/download/) (**psql**)

### Get started

Select the **Launch Exercise** button to open the exercise instructions in a new browser window. When you're finished with the exercise, return here to:

* Complete the module
* Earn a badge for completing this module

---

## Summary

In this module, you learned how to use Azure Database for PostgreSQL as a data foundation for AI applications. You explored the service architecture, including compute tiers, high availability options, and managed capabilities such as automated backups, PgBouncer connection pooling, and server extensions. You established secure connections using Microsoft Entra authentication with DefaultAzureCredential and configured TLS encryption for data in transit. You designed database schemas with tables, constraints, and data types suited for AI workloads, including JSONB for flexible structured data and appropriate indexes for query performance.

You also learned SQL techniques for querying and manipulating data, including filtering with WHERE clauses and JSONB operators, joining tables, using aggregation with GROUP BY, and building reusable queries with Common Table Expressions. You integrated PostgreSQL into Python applications using the psycopg library, implementing parameterized queries, connection management, and error handling. Finally, you built a practical AI agent tool backend that persists conversation history and task state, demonstrating how these concepts work together in a real scenario.

### Additional resources

Use the following resources to learn more about Azure Database for PostgreSQL and related topics:

* [Azure Database for PostgreSQL documentation](/en-us/azure/postgresql/)
* [Connect and query with Python (psycopg)](/en-us/azure/postgresql/flexible-server/connect-python)
* [Microsoft Entra authentication with Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/how-to-configure-sign-in-azure-ad-authentication)
* [PostgreSQL data types documentation](https://www.postgresql.org/docs/current/datatype.html)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/_

## Fuentes
- [Build and query with Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/?WT.mc_id=api_CatalogApi)
