# Implement vector search with Azure Database for PostgreSQL

> Curso: Develop AI solutions with Azure Database for PostgreSQL (wwl-develop-ai-solutions-azure-database-postgresql) · Seccion: Develop AI solutions with Azure Database for PostgreSQL
> Duracion estimada: 94 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

AI applications require efficient storage and retrieval of vector embeddings to power semantic search, recommendations, and retrieval\-augmented generation. This module guides you through implementing vector search capabilities in Azure Database for PostgreSQL using the pgvector extension, enabling you to build AI solutions that find semantically similar content from your data.

Imagine you're a developer building a knowledge base search system for a legal services firm. The system needs to help attorneys find relevant case documents, contracts, and legal precedents based on the meaning of their queries rather than exact keyword matches. When an attorney searches for "breach of fiduciary duty in corporate merger," the system must return documents that discuss similar concepts even if they use different terminology.

Your team has chosen Azure Database for PostgreSQL because the firm already stores document metadata and client information there. Rather than introducing a separate vector database and managing data synchronization, you want to add vector search capabilities directly to the existing PostgreSQL instance. The system must handle hundreds of thousands of legal documents, support real\-time queries with sub\-second response times, and update embeddings as new documents arrive daily.

You need to enable the pgvector extension, design a schema that stores embeddings alongside document metadata, create indexes that balance search speed against accuracy, and build queries that retrieve the most relevant documents for RAG\-powered legal research assistants.

After completing this module, you'll be able to:

* Store and query vector embeddings using the pgvector extension in Azure Database for PostgreSQL
* Execute vector similarity searches using different distance metrics and operators
* Create and manage vector indexes to optimize search performance
* Implement embedding update and refresh strategies for evolving datasets
* Build retrieval patterns that integrate PostgreSQL vector search with RAG pipelines

---

## Store and query embeddings with pgvector

Vector embeddings transform text, images, and other content into numerical representations that capture semantic meaning. Azure Database for PostgreSQL supports storing and querying these embeddings through the pgvector extension, allowing you to add vector search capabilities to your existing PostgreSQL database without managing a separate vector store.

This unit covers enabling the pgvector extension, designing schemas for vector storage, inserting and updating embeddings, and performing basic similarity queries. These foundational operations form the basis for building semantic search and retrieval features in your AI applications.

### Enable the pgvector extension

The pgvector extension adds vector data types and similarity search operators to PostgreSQL. Before you can store embeddings, you must enable the extension in your database. Azure Database for PostgreSQL includes pgvector as one of the supported extensions, making it available without additional installation.

To enable pgvector, connect to your database and run the `CREATE EXTENSION` command. You need the appropriate permissions to create extensions, typically granted to the server administrator or users with the `azure_pg_admin` role.

```
CREATE EXTENSION IF NOT EXISTS vector;

```

After enabling the extension, you can verify it's available by querying the installed extensions:

```
SELECT * FROM pg_extension WHERE extname = 'vector';

```

The pgvector extension introduces the `vector` data type, which stores embeddings as arrays of single\-precision floating\-point numbers. Each vector has a fixed number of dimensions that you specify when creating a column. The extension also provides operators for calculating distances between vectors and index types for fast similarity search.

### Design schemas for vector storage

Effective schema design for vector storage combines embeddings with the metadata your application needs for filtering and display. When you define a vector column, you specify the number of dimensions using the `vector(n)` syntax, where `n` must match the output dimension of your embedding model.

Common embedding dimensions vary by model. Sentence transformer models typically produce 384\-dimensional vectors. OpenAI's text\-embedding\-ada\-002 model outputs 1,536 dimensions, while text\-embedding\-3\-large can produce up to 3,072 dimensions. Using the wrong dimension count causes insertion errors, so verify your model's output dimension before creating tables.

The following example creates a table that stores legal documents with embeddings alongside metadata useful for filtering and display:

```
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    category TEXT,
    practice_area TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    embedding vector(1536)
);

```

This schema stores the document embedding in the same row as its metadata. This approach simplifies queries because you don't need joins to retrieve both the similar documents and their details. For large content fields, consider storing the full text in a separate table and keeping only summaries or titles in the main table to reduce the data transferred during similarity searches.

When designing for multiple embedding models or embedding different content types (such as titles versus full content), you can add multiple vector columns:

```
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    title_embedding vector(384),
    content_embedding vector(1536)
);

```

### Insert and update embeddings

After creating your schema, you insert embeddings using standard SQL `INSERT` statements. Vectors are represented as string literals in array format and cast to the `vector` type. Your application code generates the embedding using an embedding API (such as Azure OpenAI) and passes it to the database as a parameter.

```
INSERT INTO documents (title, content, category, practice_area, embedding)
VALUES (
    'Corporate Merger Agreement Template',
    'This agreement outlines the terms and conditions for the merger of...',
    'contracts',
    'corporate',
    '[0.0123, -0.0456, 0.0789, -0.0321, ...]'::vector
);

```

For batch insertions when loading large datasets, use multi\-row `INSERT` statements or the `COPY` command for better performance:

```
INSERT INTO documents (title, content, category, embedding)
VALUES
    ('Document 1', 'Content...', 'legal', '[...]'::vector),
    ('Document 2', 'Content...', 'legal', '[...]'::vector),
    ('Document 3', 'Content...', 'legal', '[...]'::vector);

```

When document content changes, update the embedding to reflect the new semantic meaning:

```
UPDATE documents
SET content = 'Updated document content...',
    embedding = '[0.0234, -0.0567, ...]'::vector,
    updated_at = NOW()
WHERE id = 42;

```

For applications with frequent updates, consider batching embedding regeneration during off\-peak hours rather than updating embeddings synchronously with content changes. This approach reduces latency for content updates and consolidates calls to the embedding API.

### Query vectors with distance operators

The pgvector extension provides three distance operators for measuring similarity between vectors. Each operator calculates a different type of distance, and choosing the right one depends on your embedding model and use case.

**L2 distance (Euclidean distance)** measures the straight\-line distance between two vectors in the embedding space. Use the `<->` operator for L2 distance. Smaller values indicate more similar vectors. This metric works well when the magnitude of vectors carries meaning.

```
SELECT id, title, embedding <-> '[0.0123, -0.0456, ...]'::vector AS distance
FROM documents
ORDER BY distance
LIMIT 10;

```

**Cosine distance** measures the angle between two vectors, ignoring their magnitudes. Use the `<=>` operator for cosine distance. Values range from 0 (identical direction) to 2 (opposite directions). Cosine distance is the most common choice for text embeddings because it focuses on the direction of meaning rather than the length of the vector.

```
SELECT id, title, embedding <=> '[0.0123, -0.0456, ...]'::vector AS distance
FROM documents
ORDER BY distance
LIMIT 10;

```

**Negative inner product** calculates the dot product of two vectors and negates it. Use the `<#>` operator. This metric is useful for maximum inner product search, where larger dot products indicate more similar vectors. The negation converts it to a distance where smaller values are better, matching the behavior of the other operators.

```
SELECT id, title, embedding <#> '[0.0123, -0.0456, ...]'::vector AS distance
FROM documents
ORDER BY distance
LIMIT 10;

```

Most embedding models, including OpenAI's embeddings, are optimized for cosine similarity. Check your embedding model's documentation to confirm which distance metric it recommends.

### Vector data types and precision

The pgvector extension offers three data types for storing vectors, each with different storage and performance characteristics.

The **vector** type stores elements as single\-precision (32\-bit) floating\-point numbers. This is the standard type for most use cases and provides a good balance of precision and storage efficiency. A 1536\-dimensional vector uses approximately 6 KB of storage.

The **halfvec** type stores elements as half\-precision (16\-bit) floating\-point numbers. This type reduces storage by half compared to `vector` while maintaining sufficient precision for most similarity search tasks. Use `halfvec` when storage is a concern and you verified that reduced precision doesn't significantly impact your search quality.

```
CREATE TABLE documents_compact (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    embedding halfvec(1536)
);

```

The **sparsevec** type stores sparse vectors where most elements are zero. Instead of storing all dimensions, it stores only the nonzero values and their positions. This type is useful for models that produce sparse embeddings, such as certain document representations. Specify the maximum dimension count when creating the column.

```
CREATE TABLE sparse_documents (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    embedding sparsevec(10000)
);

```

Note

HNSW indexes on `sparsevec` columns support up to 1,000 non\-zero elements. If your sparse vectors exceed this limit, consider dimensionality reduction or alternative indexing strategies.

For most AI applications using dense embeddings from models like OpenAI or sentence transformers, use the standard `vector` type. Consider `halfvec` only after benchmarking confirms that half\-precision provides acceptable search quality for your specific use case.

---

## Perform fast vector similarity search

As your vector dataset grows, similarity queries that scan every row become too slow for production use. A table with one million vectors requires one million distance calculations for each query, resulting in latency measured in seconds rather than milliseconds. Vector indexes solve this problem by organizing embeddings into structures that enable fast approximate search.

This unit covers the indexing strategies available in pgvector: IVFFlat and HNSW. You learn how each algorithm works, when to use each type, and how to configure indexes for your performance requirements.

Note

Azure Database for PostgreSQL also supports **DiskANN** (Disk Approximate Nearest Neighbor) indexes, which offer a balance of high accuracy and fast build times. For details on DiskANN configuration and usage, see [Optimize performance when using pgvector](/en-us/azure/postgresql/flexible-server/how-to-optimize-performance-pgvector).

### Understand exact versus approximate search

Without an index, pgvector performs **exact nearest\-neighbor search**. The database calculates the distance between your query vector and every vector in the table, then returns the rows with the smallest distances. This approach guarantees to find the true nearest neighbors, but the computational cost grows linearly with the number of rows.

For small tables (under 10,000 rows), exact search often provides acceptable performance. However, as tables grow larger, query times increase proportionally. A table with 100,000 vectors might take 500 milliseconds per query, while a table with one million vectors could take several seconds.

**Approximate nearest\-neighbor (ANN)** search trades perfect accuracy for dramatic speed improvements. ANN algorithms organize vectors into structures that enable the database to examine only a subset of vectors during queries. The results might occasionally miss some true nearest neighbors, but queries complete in milliseconds regardless of table size.

The key metric for ANN quality is **recall**: the percentage of true nearest neighbors that appear in the approximate results. For example, 95% recall means that on average, 95 out of 100 true nearest neighbors appear in the approximate results. Most AI applications achieve excellent results with 95\-99% recall, making the speed trade\-off worthwhile.

### IVFFlat indexes

The **Inverted File Flat (IVFFlat)** algorithm partitions vectors into clusters during index creation. When you query, the database identifies the clusters closest to your query vector and searches only within those clusters instead of the entire table.

Understanding IVFFlat's internal mechanics helps you choose appropriate parameters and troubleshoot performance issues. During index creation, IVFFlat performs k\-means clustering on your vectors, grouping them into a specified number of lists (clusters). Each cluster has a centroid—the average position of all vectors in that cluster. When you run a query, pgvector calculates distances from your query vector to each centroid, identifies the closest clusters (determined by the `probes` setting), and searches only within those clusters. This reduces the number of distance calculations from the total row count to approximately `(rows / lists) * probes`.

Creating an IVFFlat index requires choosing parameters that balance query speed against search accuracy. The `lists` parameter controls the number of clusters: more lists mean each cluster contains fewer vectors, which speeds up queries but can reduce recall if clusters split semantically similar vectors. For tables up to one million rows, use `rows / 1000`; for larger tables, use `sqrt(rows)`.

```
CREATE INDEX documents_embedding_idx ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

```

The operator class must match the distance operator you use in queries: `vector_l2_ops` for L2 distance (`<->`), `vector_cosine_ops` for cosine distance (`<=>`), or `vector_ip_ops` for inner product (`<#>`).

The `probes` parameter controls how many clusters to search at query time. Higher values improve recall but increase latency. Set this at the session level with `SET ivfflat.probes = 10`. Start with `probes = sqrt(lists)` and adjust based on your recall and latency requirements.

IVFFlat indexes require existing data to train the clustering algorithm. Creating an index on an empty table produces an index that isn't usable for queries—load your initial data before creating the index. When data distribution changes significantly after adding data from a new domain, the clusters might no longer optimally partition your vectors. Monitor recall and rebuild the index if quality degrades.

### HNSW indexes

**Hierarchical Navigable Small World (HNSW)** indexes use a multi\-layer graph structure for similarity search. This approach typically provides better query performance than IVFFlat, though with higher memory usage and longer build times.

HNSW uses a fundamentally different approach than IVFFlat, building a navigable graph structure instead of partitioning vectors into clusters. The algorithm builds a graph where each vector is a node connected to its nearest neighbors, organized into multiple layers: the top layer contains the fewest nodes spaced far apart, each lower layer contains more nodes with denser connections, and the bottom layer contains all nodes. When you query, the algorithm starts at the top layer and navigates through the graph, moving to lower layers as it gets closer to the query vector. This coarse\-to\-fine approach quickly narrows down the search space. The design enables incremental index updates and typically achieves higher recall at the same query latency compared to IVFFlat.

```
CREATE INDEX documents_embedding_idx ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

```

Unlike IVFFlat, HNSW indexes can be created on empty tables—the graph structure updates incrementally as you insert new rows.

The `m` parameter sets the maximum number of connections per node in the graph. Higher values improve recall but increase memory usage and build time. The default of 16 works well for most use cases; consider increasing to 32 or 64 for datasets where high recall is critical. The `ef_construction` parameter controls the search width during index building: higher values create higher\-quality indexes but slow down construction. For production indexes where query quality matters more than build time, consider values of 100\-200\.

The `ef_search` parameter controls the search width during queries—set this at the session level with `SET hnsw.ef_search = 100`. Start with the default of 40 and increase if you need higher recall. Values of 100\-200 typically achieve 99%\+ recall.

### Choose between IVFFlat and HNSW

Both index types enable fast approximate search, but they have different characteristics that make each better suited for specific scenarios.

| Factor | IVFFlat | HNSW |
| --- | --- | --- |
| Query performance | Good | Better |
| Build time | Faster | Slower |
| Memory usage | Lower | Higher |
| Empty table support | No | Yes |
| Insert performance | Fast | Moderate |
| Recall at same latency | Lower | Higher |

**Choose HNSW when:**

* Query performance is your primary concern
* You need high recall (99%\+) with low latency
* Your dataset doesn't change frequently
* Memory constraints aren't severe

**Choose IVFFlat when:**

* Memory usage is a concern
* You need faster index builds for frequently changing data
* You're willing to trade some query performance for lower resource usage
* You can tolerate slightly lower recall

For most production AI applications, HNSW provides the best user experience due to its superior query performance and recall characteristics. Start with HNSW unless you have specific constraints that favor IVFFlat.

### Match index operators to distance functions

The operator class you specify when creating an index must match the distance operator in your queries. If they don't match, PostgreSQL won't use the index, falling back to a slow sequential scan.

Each operator class corresponds to a specific distance operator:

| Operator class | Distance operator | Use case |
| --- | --- | --- |
| `vector_l2_ops` | `<->` | L2 (Euclidean) distance |
| `vector_cosine_ops` | `<=>` | Cosine distance |
| `vector_ip_ops` | `<#>` | Negative inner product |

To verify that your queries use the index, run `EXPLAIN ANALYZE`:

```
EXPLAIN ANALYZE
SELECT id, title
FROM documents
ORDER BY embedding <=> '[0.0123, -0.0456, ...]'::vector
LIMIT 10;

```

The output should show an index scan using your vector index:

```
Limit  (cost=40.02..44.27 rows=10 width=44) (actual time=0.512..0.518 rows=10 loops=1)
  ->  Index Scan using documents_embedding_idx on documents  (cost=40.02..2138.02 rows=4932 width=44) (actual time=0.510..0.515 rows=10 loops=1)
        Order By: (embedding <=> '[...]'::vector)

```

If you see "Seq Scan" instead of "Index Scan," check that:

1. The operator class matches the distance operator
2. The index exists and is valid
3. The table has enough rows (PostgreSQL might choose a sequential scan for small tables)
4. The LIMIT clause is present (indexes are most effective with ORDER BY and LIMIT)

---

## Manage index lifecycle and embedding updates

Vector indexes and embeddings require ongoing maintenance as your data evolves. New documents shift the distribution of vectors, content updates invalidate existing embeddings, and embedding model upgrades require regenerating all vectors. Understanding how to manage these changes keeps your vector search performing well over time.

This unit covers monitoring index health, rebuilding indexes when needed, updating embeddings efficiently, and handling embedding model migrations.

### Monitor index health and performance

Effective maintenance starts with understanding your current index state. PostgreSQL provides system views and functions that reveal whether indexes are being used, how much space they consume, and whether queries perform as expected.

The `pg_stat_user_indexes` view shows usage patterns for your indexes. If a vector index shows zero scans, queries might not be using it—often because the operator class doesn't match the distance operator in your queries, or because the query planner chose a sequential scan for a small table. High scan counts confirm the index is working as expected.

```
SELECT
    schemaname,
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan AS times_used,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE indexrelname LIKE '%embedding%'
ORDER BY idx_scan DESC;

```

Beyond usage statistics, query performance reveals index health over time. Run `EXPLAIN ANALYZE` periodically on representative queries and track the execution times. If queries that took 10 milliseconds now take 50 milliseconds without a corresponding increase in data volume, the index structure might have degraded. This commonly happens after adding significant new data, especially from a different domain or with different characteristics than the original dataset.

Large index builds can take minutes or hours. Monitor progress using `pg_stat_progress_create_index`, which shows the current phase and completion percentage. HNSW builds progress through `initializing` and `loading tuples` phases, while IVFFlat shows additional phases for k\-means clustering. The percentage completion is most meaningful during the final `loading tuples` phase.

### Rebuild indexes when data distribution changes

ANN indexes optimize their internal structures based on the data distribution at creation time. When you add significant new data, especially data from a different domain or with different characteristics, the index might no longer partition vectors optimally. This degradation manifests as increased query latency, decreased result quality, or both.

Several signals indicate that an index needs rebuilding. Query latency increases without a corresponding increase in data volume suggest structural degradation. Users reporting less relevant search results points to recall problems. Adding more than 20\-30% new data, especially from a new source or domain, often warrants proactive reindexing even before you notice problems.

For production systems that can't tolerate downtime, use `CREATE INDEX CONCURRENTLY` to build a replacement index without blocking queries. This approach takes longer and uses more resources than a regular build, but your application continues serving requests throughout the process. Create the new index with a temporary name, verify it works with `EXPLAIN ANALYZE`, drop the old index, then rename the new one to take its place.

```
-- Create new index concurrently (doesn't block queries)
CREATE INDEX CONCURRENTLY documents_embedding_new_idx
ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Verify the new index works, then swap
DROP INDEX documents_embedding_idx;
ALTER INDEX documents_embedding_new_idx RENAME TO documents_embedding_idx;

```

For systems that can tolerate brief interruptions, `REINDEX INDEX documents_embedding_idx` is simpler but blocks writes during the rebuild. Schedule this during low\-traffic periods.

### Update embeddings efficiently

When source content changes, the associated embedding no longer accurately represents the content's meaning. Keeping embeddings synchronized with content is essential for search quality, but the approach you choose depends on your update frequency and latency requirements.

For occasional updates, updating the embedding in the same transaction as the content keeps everything consistent. Your application calls the embedding API, gets the new vector, and writes both the content and embedding together. This approach is simple and guarantees consistency, but it adds latency to every content update and tightly couples your content workflow to the embedding service's availability.

Applications with frequent content changes benefit from a batch approach that decouples content updates from embedding generation. Mark documents as needing embedding updates using a flag column or timestamp comparison, then process pending updates asynchronously in batches. This pattern reduces API costs through batching, improves content update latency, and makes your system more resilient to embedding service outages.

```
-- Add a column to track embedding status
ALTER TABLE documents ADD COLUMN embedding_stale BOOLEAN DEFAULT FALSE;

-- When content changes, mark for embedding update (fast)
UPDATE documents
SET content = 'New content...', embedding_stale = TRUE, updated_at = NOW()
WHERE id = 42;

-- Background job processes stale embeddings in batches
SELECT id, content FROM documents WHERE embedding_stale = TRUE LIMIT 100;

-- After generating embeddings externally, update in bulk
UPDATE documents
SET embedding = data.embedding, embedding_stale = FALSE
FROM (VALUES (1, '[...]'::vector), (2, '[...]'::vector)) AS data(id, embedding)
WHERE documents.id = data.id;

```

Some applications benefit from periodically regenerating all embeddings, not just those with content changes. This catches subtle updates that don't trigger the stale flag, ensures consistency across all embeddings, and helps when testing different embedding parameters. Implement this as a scheduled job that processes documents ordered by their last update time, refreshing older embeddings first.

### Handle embedding model changes

Upgrading to a new embedding model or switching providers requires regenerating all embeddings. Because different models produce vectors with different dimensions and semantic relationships, you can't mix embeddings from different models in the same column.

#### Migration strategy

Migrating to a new embedding model requires careful planning because you can't simply overwrite existing embeddings—your application would return inconsistent results while the migration is in progress. The safest approach uses a parallel column strategy that lets you populate new embeddings alongside existing ones, validate search quality, and switch over atomically. This strategy adds temporary storage overhead but avoids downtime and lets you roll back if the new model underperforms.

1. **Add a new vector column** for the new embeddings:

```
ALTER TABLE documents ADD COLUMN embedding_v2 vector(3072);

```
2. **Create an index on the new column**:

```
CREATE INDEX documents_embedding_v2_idx
ON documents USING hnsw (embedding_v2 vector_cosine_ops);

```
3. **Backfill embeddings in batches** to avoid overwhelming the embedding API:

```
-- Process in batches, application code generates embeddings
UPDATE documents
SET embedding_v2 = '[...]'::vector
WHERE id BETWEEN 1 AND 10000
  AND embedding_v2 IS NULL;

```
4. **Update application queries** to use the new column. You can run both columns in parallel during testing:

```
-- Compare results from both models
SELECT id, title,
       embedding <=> $1 AS v1_distance,
       embedding_v2 <=> $2 AS v2_distance
FROM documents
ORDER BY embedding_v2 <=> $2
LIMIT 10;

```
5. **Drop the old column and index** after validating the new embeddings:

```
DROP INDEX documents_embedding_idx;
ALTER TABLE documents DROP COLUMN embedding;
ALTER TABLE documents RENAME COLUMN embedding_v2 TO embedding;
ALTER INDEX documents_embedding_v2_idx RENAME TO documents_embedding_idx;

```

#### Estimate migration time

Plan your migration timeline based on:

* **Row count:** More rows means more embedding API calls
* **API rate limits:** Most embedding APIs have requests\-per\-minute limits
* **Batch size:** Larger batches are more efficient but might time out

For example, with 500,000 documents, an API rate limit of 3,000 requests per minute, and batches of 100 documents, the backfill would take approximately 28 hours of continuous processing.

### Manage storage and cleanup

Vector columns consume significant storage. A 1536\-dimensional vector uses approximately 6 KB per row. A table with one million documents and embeddings requires about 6 GB just for the vector data, plus additional space for indexes.

#### Estimate storage requirements

Vector data consumes significantly more storage than typical relational columns, so planning capacity before loading large datasets prevents surprises. Understanding the relationship between dimension count, row count, and index overhead helps you choose appropriate Azure Database for PostgreSQL compute tiers and storage configurations. You can query existing tables to understand current usage and extrapolate for growth.

```
SELECT
    pg_size_pretty(pg_relation_size('documents')) AS table_size,
    pg_size_pretty(pg_indexes_size('documents')) AS index_size,
    pg_size_pretty(pg_total_relation_size('documents')) AS total_size;

```

For planning purposes, estimate:

* Vector column storage: `dimensions * 4 bytes * row_count`
* HNSW index overhead: approximately 1\.5\-2x the vector column size
* IVFFlat index overhead: approximately 1\-1\.5x the vector column size

#### Reclaim space after updates

PostgreSQL uses a multiversion concurrency control (MVCC) system that keeps old row versions until they're no longer needed by any transaction. When you update or delete rows, PostgreSQL doesn't immediately reclaim the disk space. For vector tables with frequent embedding updates, dead tuples accumulate faster than typical relational tables because each embedding change creates a new row version. This bloat can significantly impact query performance and storage costs if not managed proactively. Run `VACUUM` to reclaim space:

```
-- Standard vacuum (runs concurrently)
VACUUM documents;

-- Full vacuum (reclaims more space but locks the table)
VACUUM FULL documents;

```

For tables with heavy update activity, configure autovacuum to run more frequently:

```
ALTER TABLE documents SET (
    autovacuum_vacuum_scale_factor = 0.05,
    autovacuum_analyze_scale_factor = 0.02
);

```

These settings trigger autovacuum when 5% of rows are modified, rather than the default 20%.

---

## Run vector similarity search for semantic retrieval

Semantic retrieval finds documents based on meaning rather than exact keyword matches. This capability powers applications like knowledge base search, document discovery, and recommendation systems. Effective semantic retrieval combines vector similarity with metadata filtering, distance thresholds, and query patterns that return contextually relevant results.

This unit covers practical query patterns for semantic retrieval scenarios. You learn to filter results by metadata, set quality thresholds, handle complex queries, and combine vector search with full\-text search for hybrid retrieval.

### Combine vector search with metadata filters

Real\-world queries rarely search the entire document corpus. Users typically want results filtered by category, date range, author, or other attributes. The challenge is combining vector similarity with these filters while maintaining acceptable query performance.

Adding `WHERE` clauses to filter documents before similarity calculation works intuitively: PostgreSQL first identifies rows matching your filters, then calculates distances only for those rows. For highly selective filters (matching a small percentage of rows), this dramatically reduces the search space. A query filtering to "contracts" in the "corporate" practice area might eliminate 95% of documents before any vector math happens.

```
SELECT id, title, embedding <=> $1 AS distance
FROM documents
WHERE category = 'contracts'
  AND practice_area = 'corporate'
  AND created_at > '2024-01-01'
ORDER BY embedding <=> $1
LIMIT 10;

```

To maintain performance with filtered queries, create B\-tree indexes on columns you frequently filter. For queries that always combine specific columns, composite indexes can be more efficient than multiple single\-column indexes. PostgreSQL's query planner decides whether to use the vector index, metadata indexes, or both based on filter selectivity and table statistics. Run `ANALYZE` after loading data to ensure accurate statistics that help the planner make good decisions.

Filter selectivity affects which execution strategy PostgreSQL chooses. When filters match a large portion of the table (low selectivity), the vector index dominates query performance. When filters are highly selective, PostgreSQL might scan matching rows without using the vector index at all. Neither approach is wrong—the planner optimizes for total query cost. Monitor query plans with `EXPLAIN ANALYZE` to understand how PostgreSQL handles your specific filter combinations.

### Implement distance thresholds

Using only `LIMIT` returns the top N most similar documents regardless of their actual similarity. For some applications, returning irrelevant results is worse than returning no results. A legal research assistant that surfaces unrelated contracts when no relevant ones exist erodes user trust. Distance thresholds ensure a minimum quality level by filtering out results that fall below a similarity standard.

Adding a `WHERE` clause that filters by distance creates this quality floor. The query returns at most N documents, but only if they meet the threshold. If no documents are similar enough, the query returns empty results—which might be the right answer.

```
SELECT id, title, embedding <=> $1 AS distance
FROM documents
WHERE embedding <=> $1 < 0.4
ORDER BY embedding <=> $1
LIMIT 10;

```

Choosing the right threshold requires understanding your data. Start by analyzing distance distributions: calculate distances between queries and documents you know are relevant (these should cluster at low distances) and between queries and clearly unrelated documents (these should have higher distances). The threshold should fall in the gap between these distributions. For cosine distance with OpenAI embeddings, thresholds typically fall between 0\.3 (strict, high precision) and 0\.6 (lenient, high recall).

Most production queries combine both mechanisms: a distance threshold for quality and a limit for resource control. This returns up to five legal documents that are sufficiently similar, ordered by similarity, while avoiding the embarrassment of surfacing unrelated results when the knowledge base lacks relevant content.

### Retrieve documents with content for context

Semantic retrieval often serves as input to downstream processing, such as displaying results to users or providing context to an LLM. Your queries should return all the information needed for these purposes in a single round trip.

Retrieve the columns your application needs—title, content, metadata, distance score—in one query rather than fetching IDs first and making follow\-up queries for details. For large content fields, consider whether you need the full text or just a summary; limiting data transfer improves response time. When document metadata spans multiple tables, use joins to retrieve complete information, ensuring joined tables have appropriate indexes on the join columns.

```
SELECT
    d.id,
    d.title,
    d.content,
    d.embedding <=> $1 AS distance,
    a.name AS author_name
FROM documents d
JOIN authors a ON d.author_id = a.id
WHERE d.embedding <=> $1 < 0.5
ORDER BY d.embedding <=> $1
LIMIT 5;

```

### Handle multi\-vector queries

Some scenarios require finding documents similar to multiple examples rather than a single query vector. A user might provide several relevant documents as examples, or a complex query might have multiple distinct aspects that each need representation.

When example documents are semantically related—all describing the same concept from different angles—averaging their vectors produces a combined embedding that represents the "center" of those examples in embedding space. This works well for queries like "find more documents like these three merger agreements."

When examples represent different aspects of a query that shouldn't be averaged together, query each aspect separately and combine the results. A search for "documents about mergers AND environmental compliance" benefits from separate queries because averaging the merger embedding with the environmental embedding produces a point that might not be near either concept. Instead, retrieve candidates for each aspect and rank by combined relevance.

```
WITH
merger_results AS (
    SELECT id, embedding <=> $1 AS distance FROM documents ORDER BY embedding <=> $1 LIMIT 20
),
environmental_results AS (
    SELECT id, embedding <=> $2 AS distance FROM documents ORDER BY embedding <=> $2 LIMIT 20
)
SELECT d.id, d.title,
       (COALESCE(mr.distance, 1) + COALESCE(er.distance, 1)) / 2 AS combined_score
FROM documents d
LEFT JOIN merger_results mr ON d.id = mr.id
LEFT JOIN environmental_results er ON d.id = er.id
WHERE mr.id IS NOT NULL OR er.id IS NOT NULL
ORDER BY combined_score
LIMIT 10;

```

This finds documents similar to either aspect and ranks them by combined proximity to both queries.

### Implement hybrid search

Vector similarity excels at finding semantically related content but can miss documents with exact term matches that users expect. When an attorney searches for "Smith v. Jones," they expect that exact case name to appear in results even if the semantic meaning of their query points elsewhere. Hybrid search combines vector similarity with keyword\-based full\-text search to capture both semantic and lexical relevance.

PostgreSQL's built\-in full\-text search provides `ts_rank` for scoring keyword matches. Combine this with vector distance (converted to a similarity score) for a hybrid ranking. The weights determine how much each signal contributes: higher semantic weight works better for queries where meaning matters more than exact terms, while higher keyword weight serves queries with specific technical terms, names, or codes that must match exactly.

```
SELECT
    id,
    title,
    (1 - (embedding <=> $1)) * 0.7 +
        ts_rank(to_tsvector('english', content), plainto_tsquery('english', $2)) * 0.3 AS hybrid_score
FROM documents
WHERE to_tsvector('english', content) @@ plainto_tsquery('english', $2)
   OR embedding <=> $1 < 0.5
ORDER BY hybrid_score DESC
LIMIT 10;

```

To speed up keyword matching, create a GIN index on the full\-text search vector. For frequently searched columns, storing the tsvector in a generated column avoids recomputing it for every query.

Hybrid search adds complexity and computation. Use it when users search for specific terms that must match exactly, when your corpus includes technical jargon where synonyms don't capture the right meaning, or when you want to boost results that match both semantically and lexically. For pure semantic search where meaning matters more than specific words, vector\-only search is simpler and often sufficient.

---

## Implement retrieval patterns for RAG pipelines

Retrieval\-augmented generation (RAG) enhances language model responses by providing relevant context from your data. The retriever component searches your knowledge base and returns documents that the LLM uses to generate accurate, grounded answers. Azure Database for PostgreSQL with pgvector serves as an effective retriever, storing your document embeddings and executing similarity queries that feed the generation step.

This unit covers designing schemas for RAG workloads, implementing chunk retrieval queries, building document ingestion pipelines, returning citation metadata, and evaluating retrieval quality.

### Understand RAG architecture and the retriever role

RAG systems follow a three\-step pattern:

1. **Query embedding:** Convert the user's question into a vector using an embedding model
2. **Retrieval:** Search the vector store for documents similar to the query embedding
3. **Generation:** Pass the retrieved documents as context to an LLM, which generates a response

PostgreSQL acts as the retriever in this architecture. The quality of retrieval directly impacts generation quality. If the retriever returns irrelevant documents, the LLM lacks the context needed to answer correctly and might generate incorrect information. If the retriever misses relevant documents, the answer might be incomplete.

For a legal research assistant, effective retrieval means finding the case precedents, statutes, and contract clauses that address the attorney's question. The LLM then synthesizes these sources into a coherent answer with citations.

### Design schemas for RAG workloads

RAG applications typically work with document chunks rather than whole documents. Long documents exceed LLM context limits and might contain sections irrelevant to a specific query. Chunking splits documents into smaller, focused segments that can be retrieved independently.

#### Separate documents and chunks

Use two tables: one for source documents and one for chunks with embeddings:

```
CREATE TABLE source_documents (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    source_url TEXT,
    document_type TEXT,
    ingested_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES source_documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),
    token_count INTEGER,
    start_char INTEGER,
    end_char INTEGER,
    UNIQUE (document_id, chunk_index)
);

```

This design provides several benefits:

* **Flexible retrieval:** You can retrieve individual chunks or reconstruct document sections
* **Source tracking:** Every chunk links back to its source for citations
* **Efficient storage:** Document metadata is stored once, not duplicated per chunk
* **Easy updates:** Replacing a document means deleting its chunks and reingesting

#### Add metadata for filtering and context

Include metadata that helps with filtering and context reconstruction:

```
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES source_documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),
    token_count INTEGER,
    section_title TEXT,
    page_number INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

```

Section titles and page numbers help users verify retrieved information and help the LLM understand the context of each chunk.

#### Create indexes for RAG query patterns

Vector similarity indexes (HNSW or IVFFlat) enable fast embedding lookups, as covered earlier in this module. RAG workloads also benefit from B\-tree indexes that accelerate the joins and filters unique to chunk retrieval. When you retrieve chunks, you frequently join back to source documents for citation metadata and filter or order by chunk position within a document. Without these indexes, PostgreSQL scans the entire chunks table for every retrieval query.

```
-- B-tree index for document lookups (speeds up JOINs to source_documents)
CREATE INDEX document_chunks_document_id_idx
ON document_chunks (document_id);

-- Composite index for chunk ordering (supports context window queries)
CREATE INDEX document_chunks_doc_chunk_idx
ON document_chunks (document_id, chunk_index);

```

The composite index on `(document_id, chunk_index)` is particularly important for context\-window retrieval, where you fetch adjacent chunks to provide surrounding context. Without it, PostgreSQL must scan all chunks for a document to find neighbors.

### Implement chunk retrieval for context building

RAG queries retrieve chunks that become the LLM's context. The retrieval pattern you choose affects both answer quality and token efficiency. You need to balance three competing concerns: retrieving enough relevant content, staying within token limits, and providing sufficient context for the LLM to understand each chunk.

The simplest approach retrieves the top\-k most similar chunks directly. This works well when your chunks are self\-contained and your questions match single chunks cleanly. However, legal documents, technical specifications, and narrative content often spread concepts across multiple paragraphs. A chunk might reference "the foregoing conditions" or "as described above" without containing the referenced text.

For these cases, context\-window retrieval fetches adjacent chunks along with each match. If chunk 47 is most similar to the query, you also retrieve chunks 46 and 48\. This increases token usage but reduces the risk of incomplete answers. The trade\-off depends on your content structure: highly structured documents with clear section boundaries need less surrounding context than flowing narrative text.

Token limits add another constraint. LLMs have fixed context windows, and you need room for the system prompt, user question, and generated response. If you retrieve 10 chunks averaging 500 tokens each, you've consumed 5,000 tokens before the LLM writes a single word. Track cumulative token counts during retrieval to stay within budget.

The following query combines these patterns. It retrieves the most similar chunks with their neighbors, tracks cumulative tokens, and includes citation metadata:

```
WITH matched_chunks AS (
    -- Find the most similar chunks
    SELECT id, document_id, chunk_index, embedding <=> $1 AS distance
    FROM document_chunks
    ORDER BY embedding <=> $1
    LIMIT 3
),
context_window AS (
    -- Expand to include adjacent chunks for context
    SELECT DISTINCT dc.id, dc.document_id, dc.chunk_index, dc.content,
           dc.token_count, mc.distance
    FROM matched_chunks mc
    JOIN document_chunks dc ON dc.document_id = mc.document_id
        AND dc.chunk_index BETWEEN mc.chunk_index - 1 AND mc.chunk_index + 1
),
token_limited AS (
    -- Track cumulative tokens to respect LLM context limits
    SELECT cw.*, sd.title AS source_title, sd.source_url,
           SUM(cw.token_count) OVER (ORDER BY cw.distance, cw.chunk_index) AS cumulative_tokens
    FROM context_window cw
    JOIN source_documents sd ON cw.document_id = sd.id
)
SELECT id, content, source_title, source_url, distance
FROM token_limited
WHERE cumulative_tokens <= 3000
ORDER BY distance, chunk_index;

```

Adjust the parameters based on your use case. For a legal research assistant answering specific clause questions, you might retrieve five matches with no context window. For a customer support bot answering open\-ended questions about product documentation, you might retrieve three matches with two chunks of surrounding context each.

### Handle document ingestion pipelines

New documents must be processed before they're searchable. The ingestion pipeline splits documents into chunks, generates embeddings, and stores everything in PostgreSQL.

How you split documents directly affects retrieval quality. The right chunking strategy depends on your content structure and query patterns:

* **Fixed\-size chunks:** Split every N characters or tokens. This approach is simple to implement and produces predictable token counts, but it might cut sentences or paragraphs mid\-thought. Use fixed\-size chunking when your content lacks clear structural boundaries or when you need consistent chunk sizes for token budget planning.
* **Semantic chunks:** Split at natural boundaries like paragraphs, sections, or sentences. This preserves meaning within each chunk but produces variable sizes. Use semantic chunking for structured documents where sections represent complete thoughts, such as legal clauses, API documentation, or FAQ entries.
* **Overlapping chunks:** Include text from adjacent chunks to preserve context at boundaries. For example, a 200\-character overlap between 1,000\-character chunks ensures that concepts spanning chunk boundaries appear in at least one complete chunk. Use overlapping when your queries might match content near chunk boundaries.

For the legal research assistant scenario, semantic chunking at paragraph or section boundaries works well because legal text is organized into discrete clauses and arguments. Each chunk represents a complete legal concept that can stand alone in the LLM's context.

Once you've chunked your documents and generated embeddings, insert them efficiently using batch operations. The two\-table design requires inserting the source document first to obtain its ID, then inserting all chunks in a single multi\-row `INSERT`. This approach minimizes round trips to the database and keeps the document\-to\-chunk relationship intact. Most embedding APIs also accept multiple texts per request, so you can generate embeddings for an entire document's chunks in one API call before inserting.

Document updates require a decision: do you version documents or replace them? For most RAG applications, replacement is simpler. Delete the existing chunks (the `ON DELETE CASCADE` constraint handles this automatically when you delete the source document), then reingest the updated content. This approach ensures your retrieval results always reflect the current document state. If you need version history, add a `version` column to `source_documents` and keep old chunks alongside new ones, filtering by version at query time.

HNSW indexes handle deletions gracefully without rebuilding. IVFFlat indexes might accumulate fragmentation after significant changes, requiring periodic rebuilding to maintain query performance.

### Implement retrieval with citations

Citations transform RAG from a black box into a transparent research tool. When the legal research assistant quotes a contract clause, the attorney needs to verify that quote against the original document. Without citation metadata, users must trust the LLM's output blindly—a significant liability in legal, medical, or financial contexts where accuracy is critical.

Effective citations require more than just the chunk content. Your retrieval queries should return the source document title, URL or document ID, section heading, and page number when available. This metadata lets your application format citations that users can actually follow back to the source. The distance score also helps: you might display high\-confidence citations prominently while flagging lower\-confidence matches for user verification.

A common challenge arises when multiple chunks from the same document match a query. If chunks 12, 15, and 18 from "Employment Agreement Template" all appear in your top results, listing them as three separate citations clutters the response. Instead, group chunks by source document and present them as a single citation with multiple relevant excerpts. This approach produces cleaner output and helps users see the full context from each source.

The following query demonstrates document\-grouped retrieval. It ranks chunks within each document, limits to three chunks per document to avoid overwhelming the context, and aggregates the content for cleaner citation formatting:

```
WITH ranked_chunks AS (
    SELECT
        dc.*,
        sd.title AS document_title,
        sd.source_url,
        dc.embedding <=> $1 AS distance,
        ROW_NUMBER() OVER (PARTITION BY dc.document_id ORDER BY dc.embedding <=> $1) AS rank_in_doc
    FROM document_chunks dc
    JOIN source_documents sd ON dc.document_id = sd.id
    WHERE dc.embedding <=> $1 < 0.5
)
SELECT
    document_id,
    document_title,
    source_url,
    array_agg(content ORDER BY chunk_index) AS chunks,
    MIN(distance) AS best_distance
FROM ranked_chunks
WHERE rank_in_doc <= 3
GROUP BY document_id, document_title, source_url
ORDER BY best_distance
LIMIT 5;

```

Your application can then format this into user\-friendly citations:

> "The employer might terminate this agreement with 30 days notice."
> — *Employment Agreement Template*, Section 4\.2, Page 3

### Evaluate and improve retrieval quality

Retrieval quality determines RAG effectiveness. Poor retrieval leads to poor generation, regardless of how capable your LLM is. If the retriever returns irrelevant chunks, the LLM wastes context window capacity on useless text. If the retriever misses relevant chunks, the LLM lacks the information needed to answer correctly. Measuring retrieval quality separately from generation quality helps you diagnose where your RAG pipeline needs improvement.

Three metrics capture different aspects of retrieval performance:

* **Precision:** The fraction of retrieved chunks that are actually relevant. Low precision means the LLM receives irrelevant context that might confuse it or cause it to generate incorrect information. Improve precision by tightening distance thresholds or reducing the number of retrieved chunks.
* **Recall:** The fraction of relevant chunks that are retrieved. Low recall means the LLM misses important information, leading to incomplete or incorrect answers. Improve recall by loosening distance thresholds, increasing retrieved chunk count, or adjusting index parameters like `ef_search`.
* **Mean Reciprocal Rank (MRR):** How high the first relevant result appears in the ranked list. MRR matters because LLMs weight earlier context more heavily, and users scanning citations notice top results first. Improve MRR by refining your embedding model or query preprocessing.

To measure these metrics, you need an evaluation dataset: a set of representative queries paired with human judgments about which chunks are relevant. Building this dataset requires effort upfront—someone must run sample queries and label the results—but it pays off by letting you make data\-driven improvements rather than guessing. Start with 20\-50 queries that represent the types of questions your users actually ask. For each query, retrieve the top 10\-20 chunks and have a domain expert rate their relevance on a simple scale (irrelevant, somewhat relevant, highly relevant).

With this evaluation set in place, you can measure precision and recall at different cutoffs (precision@5, recall@10\) and track how changes to your pipeline affect these metrics. Run your retrieval queries against the evaluation set, compare the results to the human judgments, and calculate the metrics. Most teams automate this into a scoring script that runs whenever they change chunking strategies, embedding models, or index parameters.

When metrics fall below target, systematically experiment with parameters that affect the precision\-recall trade\-off:

* **Chunk size:** Smaller chunks improve precision by returning more focused content, but might hurt recall by fragmenting relevant information across multiple chunks. Larger chunks improve recall but dilute relevance.
* **Chunk overlap:** More overlap preserves context across boundaries, helping queries that match content near chunk edges. However, overlap increases storage requirements and might return redundant content.
* **Embedding model:** Different models capture different semantic relationships. A model trained on legal text might outperform a general\-purpose model for legal research. Consider domain\-specific or fine\-tuned models if general models underperform.
* **Index parameters:** Higher `ef_search` (HNSW) or `probes` (IVFFlat) improves recall by searching more candidates, at the cost of query latency. Start with default parameters and increase only if recall is insufficient.
* **Distance thresholds:** Tighter thresholds improve precision by excluding marginal matches. Looser thresholds improve recall by including more candidates. Use your evaluation dataset to find the threshold that balances both metrics for your use case.

---

## Exercise \- Implement vector search on Azure Database for PostgreSQL

In this exercise, you build a product similarity search application using Azure Database for PostgreSQL and the pgvector extension. You enable vector storage capabilities, create a database schema for products with embeddings, load sample data through a Flask web application, and perform similarity searches to find related products. This pattern provides a foundation for building recommendation systems, semantic search features, and other AI\-powered applications.

Tasks performed in this exercise:

* Download project starter files and configure the deployment script
* Deploy an Azure Database for PostgreSQL Flexible Server with Microsoft Entra authentication
* Complete the Flask application code while the server deploys
* Enable the pgvector extension and create the products table schema
* Run the Flask application to load products and perform similarity searches
* Add new products and observe how similarity results change

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

## Module assessment

Choose the best response for each of the following questions.

---

## Summary

In this module, you learned how to implement vector search capabilities using the pgvector extension in Azure Database for PostgreSQL. You started by enabling the extension and designing schemas with vector columns to store embeddings from different models, understanding how dimension size affects storage and performance. You explored the three distance operators—Euclidean distance, cosine distance, and inner product—and learned when to apply each based on your embedding model and use case.

You also learned how to create vector indexes using IVFFlat and HNSW algorithms to transform expensive sequential scans into fast approximate nearest neighbor searches. You discovered that IVFFlat requires existing data before index creation and uses lists and probes parameters to balance speed and recall, while HNSW can index data incrementally and offers better recall with the m, ef\_construction, and ef\_search parameters. You learned to verify index usage with EXPLAIN ANALYZE and match operator classes to your distance operators.

Additionally, you explored index lifecycle management strategies including monitoring index health with pg\_stat\_user\_indexes, determining when to rebuild indexes after significant data changes, and handling embedding model migrations that require updating all vectors. You implemented semantic retrieval patterns that combine vector similarity with metadata filtering, distance thresholds, and multi\-vector queries. Finally, you designed RAG pipeline schemas that separate source documents from chunks, enabling context retrieval with full citation metadata for LLM applications.

### Additional resources

* [Use pgvector on Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/how-to-use-pgvector)
* [Optimize performance when using pgvector](/en-us/azure/postgresql/flexible-server/how-to-optimize-performance-pgvector)
* [Integrate Azure Database for PostgreSQL with Azure AI Services](/en-us/azure/postgresql/flexible-server/generative-ai-azure-overview)
* [Generative AI with Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/generative-ai-overview)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/_

## Fuentes
- [Implement vector search with Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/?WT.mc_id=api_CatalogApi)
