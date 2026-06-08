# Optimize vector search in Azure Database for PostgreSQL

> Curso: Develop AI solutions with Azure Database for PostgreSQL (wwl-develop-ai-solutions-azure-database-postgresql) · Seccion: Develop AI solutions with Azure Database for PostgreSQL
> Duracion estimada: 111 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

AI applications require fast, reliable vector search to power features like semantic retrieval, recommendation engines, and RAG pipelines. Poorly tuned databases create latency bottlenecks that degrade user experience and limit throughput. This module guides you through optimizing Azure Database for PostgreSQL and pgvector to achieve the performance your AI solutions demand.

Imagine you're a developer building a product recommendation engine for an e\-commerce platform. The system uses vector embeddings to find similar products based on user behavior, product descriptions, and visual features. When users browse the site, recommendations must appear in under 100 milliseconds to avoid disrupting the shopping experience. During flash sales and holiday peaks, the platform handles tens of thousands of concurrent users requesting personalized recommendations.

Your initial deployment performs well with a catalog of 50,000 products, but as the inventory grows to two million items and traffic spikes during promotions, query latency climbs from 30 milliseconds to over one second. Conversion rates drop as users abandon slow\-loading pages. You need to tune the database, select the right vector index, and scale the infrastructure to deliver fast recommendations without overspending on compute resources.

This scenario represents challenges common across AI applications: vector search performance degrades as data grows, concurrent users strain connection limits, and the trade\-off between accuracy and speed becomes critical. The techniques you learn in this module apply whether you're building recommendation systems, semantic search, RAG pipelines, or other vector\-powered features.

After completing this module, you'll be able to:

* Tune PostgreSQL and pgvector configuration parameters to optimize query latency and memory usage for AI workloads
* Select and configure the appropriate vector index type based on dataset size, query patterns, and accuracy requirements
* Design data layouts that optimize vector storage and metadata filtering performance
* Scale Azure Database for PostgreSQL to handle high\-volume vector workloads
* Implement connection pooling and session management strategies for AI applications

---

## Tune PostgreSQL for pgvector

Vector search workloads place different demands on PostgreSQL compared to traditional transactional or analytical queries. Understanding these differences helps you tune configuration parameters to optimize query latency, memory usage, and compute efficiency for AI applications.

Note

Code examples in this unit demonstrate configuration patterns for PostgreSQL and pgvector. Parameter values shown are starting points for tuning. Optimal settings depend on your specific workload, dataset size, and hardware. Always benchmark changes in a test environment before applying them to production.

### Pgvector compute and memory requirements

Vector similarity search involves computing distances between a query vector and potentially millions of stored vectors. This computational pattern differs fundamentally from traditional database operations that filter rows based on indexed columns or join tables on key values.

When you execute a vector similarity query, pgvector must calculate the distance between your query vector and candidate vectors. For a 1536\-dimensional embedding (common with OpenAI models), each distance calculation involves 1,536 floating\-point operations. Searching one million vectors without an index requires over 1\.5 billion floating\-point operations per query. The three distance functions have different computational costs that affect your choice based on your data characteristics and performance requirements.

* **L2 (Euclidean) distance:** Uses the `<->` operator and calculates the square root of the sum of squared differences. This is the most computationally expensive option.
* **Cosine distance:** Uses the `<=>` operator and measures the angle between vectors. It normalizes vectors internally, adding computation but providing scale\-invariant similarity.
* **Inner product:** Uses the `<#>` operator and calculates the dot product. This is the fastest operation but requires pre\-normalized vectors for meaningful similarity comparisons.

For recommendation engines and semantic search, cosine distance is often preferred because it handles vectors of varying magnitudes consistently. If your embeddings are already normalized (many embedding APIs return normalized vectors), inner product provides equivalent results with less computation.

Vector columns consume substantial storage compared to traditional data types. A single 1536\-dimensional vector stored as `float4` (single precision) requires 6,144 bytes, plus overhead. A table with one million product embeddings needs approximately 6 GB just for the vector column. When PostgreSQL processes vector queries, it loads vector data into memory. The relationship between available memory and vector data size directly affects whether queries can execute efficiently in memory or must repeatedly read from disk.

Higher\-dimensional embeddings provide more semantic resolution but increase both storage and computation costs quadratically. A 3072\-dimensional vector (used by some newer embedding models) requires four times the distance calculation work and twice the storage of a 1536\-dimensional vector. Consider your accuracy requirements when choosing embedding dimensions. For many recommendation and search applications, 768 or 1,024 dimensions provide sufficient quality with meaningfully lower resource consumption.

### Memory configuration for vector workloads

PostgreSQL's memory parameters significantly affect vector query performance. Proper tuning ensures vector indexes and frequently accessed data remain in memory, reducing expensive disk operations.

The `shared_buffers` parameter controls PostgreSQL's shared memory cache, where frequently accessed data pages reside. For vector workloads, this cache should be large enough to hold your vector indexes and hot data. A cache hit ratio below 99% for vector\-heavy workloads indicates that `shared_buffers` might be too small. On Azure Database for PostgreSQL, this parameter is tuned automatically based on your compute tier, but you can adjust it within the allowed range for your tier. For dedicated vector search workloads, aim for `shared_buffers` large enough to hold your vector indexes plus a margin for other cached data. A starting point is 25% of available memory, with increases based on monitoring. The following queries help you check your current settings and cache performance.

```
-- Check current setting
SHOW shared_buffers;

-- View buffer cache hit ratio
SELECT
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS cache_hit_ratio
FROM pg_statio_user_tables;

```

The `work_mem` parameter controls memory available for individual query operations like sorts and hash joins. Vector similarity queries, especially those combining vector search with filtering and ordering, benefit from adequate `work_mem`. The default `work_mem` (typically 4 MB) is often too small for vector operations that must sort results by similarity. You can increase this value for sessions or queries that perform vector searches with large result sets using `SET work_mem = '256MB';`. Be cautious with global increases to `work_mem` because the setting applies per\-operation per\-connection, so a server handling 100 concurrent connections with complex queries could consume 100 × `work_mem` × operations\-per\-query in memory. For vector workloads, consider setting `work_mem` at the session level for specific queries rather than globally.

The `effective_cache_size` parameter tells the query planner how much memory is available for caching, including both PostgreSQL's `shared_buffers` and the operating system's file cache. This setting doesn't allocate memory but influences whether the planner chooses index scans over sequential scans. Set `effective_cache_size` to approximately 75% of total system memory on dedicated database servers. Higher values encourage the planner to use indexes, which is typically beneficial for vector search. On Azure Database for PostgreSQL, this is configured automatically based on your tier.

### Query planner settings for vector search

PostgreSQL's query planner makes decisions about how to execute queries based on cost estimates. Several parameters affect these estimates, and tuning them for modern SSD storage improves vector query planning.

The `random_page_cost` parameter estimates the cost of reading a random disk page relative to a sequential page. The default value of 4\.0 reflects spinning disk characteristics where random access is significantly slower than sequential access. Azure Database for PostgreSQL uses SSD storage where random and sequential access have similar performance. Lowering `random_page_cost` to 1\.1\-1\.5 encourages the planner to use index scans more readily, which benefits vector searches that access scattered data pages. You can adjust this setting with `SET random_page_cost = 1.1;`.

The `effective_io_concurrency` parameter tells PostgreSQL how many concurrent disk I/O operations the storage system can handle. Higher values enable bitmap heap scans to prefetch more pages in parallel. SSD storage handles concurrent I/O well, so set `effective_io_concurrency` to 200 for SSD\-based Azure Database for PostgreSQL instances. This improves performance for queries that combine vector similarity with metadata filtering.

The `parallel_tuple_cost` and `parallel_setup_cost` parameters control when PostgreSQL uses parallel query execution. Vector operations can benefit from parallelism, especially for sequential scans on large tables. Lower values for `parallel_tuple_cost` (default 0\.1\) and `parallel_setup_cost` (default 1000\) encourage parallel execution. For vector workloads with large tables, enabling parallelism can significantly reduce query time when indexes aren't being used. You can check your current parallel settings using `SHOW parallel_tuple_cost;`, `SHOW parallel_setup_cost;`, and `SHOW max_parallel_workers_per_gather;`.

### Configure pgvector\-specific parameters

The pgvector extension provides configuration parameters that control the accuracy\-speed trade\-off for index\-based searches. These parameters are critical for tuning vector query performance.

When using IVFFlat indexes, the `ivfflat.probes` parameter controls how many index partitions (lists) are searched for each query. Higher values increase recall (finding more of the true nearest neighbors) but slow queries. This trade\-off is central to IVFFlat performance tuning. You're balancing the risk of missing good matches against the cost of searching more partitions. The default value of **1** searches only the single most promising partition, which is fast but might miss relevant results stored in adjacent partitions. For recommendation engines where missing a good match degrades user experience, start with `ivfflat.probes` set to 5\-10% of your `lists` parameter and adjust based on measured recall.

```
-- Configure IVFFlat search depth
SET ivfflat.probes = 10;

-- Execute vector search
SELECT id, name, embedding <=> $1 AS distance
FROM products
ORDER BY embedding <=> $1
LIMIT 10;

```

For HNSW indexes, the `hnsw.ef_search` parameter controls the size of the dynamic candidate list during search. Larger values explore more of the graph, improving recall at the cost of speed. Unlike IVFFlat's discrete partitions, HNSW's graph structure means this parameter affects how thoroughly the algorithm explores neighbor connections before returning results. The default value of 40 provides a reasonable balance for many workloads. For high\-accuracy requirements (such as finding the true top\-10 matches), increase to 100\-200\. For latency\-critical applications where approximate results are acceptable, values as low as 20 can work. Configure `hnsw.ef_search` with `SET hnsw.ef_search = 100;` before executing your vector search. The optimal value depends on your accuracy requirements and latency budget. Benchmark with representative queries to find the right balance for your application.

### Monitor and measure performance

Tuning without measurement is guesswork. Use PostgreSQL's built\-in tools and Azure Monitor to understand query behavior and validate configuration changes.

The `EXPLAIN ANALYZE` command shows how PostgreSQL executes a query and provides actual timing information. For vector queries, this reveals whether indexes are being used and where time is spent. Understanding the execution plan helps you identify whether poor performance stems from missing indexes, suboptimal parameter settings, or data distribution issues. Run `EXPLAIN ANALYZE` before your vector query to see the execution plan. Look for **Index Scan using \[index\_name]** (indicates the vector index is being used), **Seq Scan** (indicates a sequential scan, which is slow for large tables), **actual time** values (show where execution time is spent), and **rows** counts (help identify if filtering is working efficiently). If you see sequential scans when you expect index usage, check that the query's distance operator matches the index's operator class (for example, using `<=>` with an index created using `vector_cosine_ops`).

Sometimes PostgreSQL chooses not to use an available index. Common reasons for vector queries include queries that return a large portion of the table (index overhead exceeds sequential scan), outdated statistics after significant data changes, or a distance operator that doesn't match the index's operator class. Run `ANALYZE products;` to update statistics for accurate planning. You can check index information with `SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'products';`.

Azure Database for PostgreSQL exposes metrics through Azure Monitor that help identify performance bottlenecks. Monitor **CPU percent** (high sustained CPU indicates compute\-bound vector operations), **Memory percent** (approaching limits suggests increasing compute tier or optimizing queries), **Storage IO percent** (high values indicate data isn't fitting in cache), and **Active connections** (approaching limits indicates connection pooling might help). Set up alerts for these metrics to catch performance degradation before it affects users.

### Best practices for pgvector tuning

Effective tuning follows a systematic approach rather than random parameter changes.

* **Establish baselines first:** Measure query latency and resource usage before making changes. Without baselines, you can't determine if changes help or hurt.
* **Change one parameter at a time:** Multiple simultaneous changes make it impossible to attribute improvements or regressions to specific settings.
* **Test with production\-like data:** Query performance varies dramatically with data size and distribution. Tuning on small test datasets often produces settings that fail at scale.
* **Monitor for regressions:** Parameters that improve vector search might negatively affect other workloads. Monitor overall system health after changes.
* **Document your settings:** Record what you changed, why, and what effect it had. This documentation is invaluable when troubleshooting future issues.

### Additional resources

* [Server parameters in Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/concepts-server-parameters)
* [pgvector on Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/how-to-use-pgvector)
* [Performance recommendations for Azure Database for PostgreSQL](/en-us/azure/postgresql/configure-maintain/concepts-azure-advisor-recommendations)

---

## Choose and configure vector indexes

Vector indexes enable fast similarity search by organizing vectors into data structures that eliminate the need to compare every stored vector against each query. Choosing the right index type and configuring its parameters correctly determines whether your AI application meets its performance targets.

Note

Code examples in this unit show index creation patterns for pgvector. Index parameter recommendations are starting points based on general guidance. Optimal values depend on your dataset characteristics, accuracy requirements, and performance constraints. Always benchmark with representative data before deploying to production.

### Vector index fundamentals

Without an index, vector similarity search requires a sequential scan that compares the query vector against every vector in the table. For a table with one million product embeddings, this means one million distance calculations per query, which takes seconds rather than milliseconds.

Sequential scans perform exact nearest neighbor (NN) search, guaranteeing that the returned results are the true closest vectors. This guarantee comes at the cost of query time that grows linearly with table size. Approximate nearest neighbor (ANN) indexes trade perfect accuracy for dramatically faster queries. Instead of examining every vector, ANN algorithms use clever data structures to find vectors that are likely (but not guaranteed) to be among the closest. Query time grows logarithmically or sublinearly with table size.

The accuracy of ANN search is measured as recall, the fraction of true nearest neighbors that appear in the returned results. For example, if you request 10 results and the index returns 8 of the actual 10 closest vectors (plus 2 that are close but not in the true top 10\), recall is 80%. For most AI applications, 95\-99% recall is acceptable because the difference between the eighth and tenth closest vectors is rarely meaningful to end users. The 100x\-1000x speed improvement from ANN indexes makes this trade\-off worthwhile.

The benefit of vector indexes depends on table size and query patterns:

| Table size | Index benefit |
| --- | --- |
| Under 10,000 rows | Limited; sequential scans might be fast enough |
| 10,000 \- 100,000 rows | Moderate; indexes reduce latency meaningfully |
| 100,000 \- 1 million rows | Significant; indexes are typically required for interactive use |
| Over 1 million rows | Essential; queries are unusably slow without indexes |

For the product recommendation scenario with two million products, indexes are essential for meeting the 100\-millisecond latency target.

### IVFFlat indexes

IVFFlat (Inverted File Flat) indexes partition vectors into clusters, then search only relevant clusters at query time. This approach reduces the search space while maintaining reasonable accuracy.

IVFFlat uses k\-means clustering to organize vectors into lists (also called partitions or cells). During index creation, pgvector clusters your vectors into a specified number of lists, with each list containing vectors that are similar to each other. When you query, pgvector identifies the lists whose centroids are closest to the query vector, then performs exact distance calculations only on vectors within those lists. If your query probes 10 lists out of 1000 total, you reduce the search space by 99%.

Create an IVFFlat index by specifying the number of lists and the operator class that matches your distance function. The operator class must match the distance operator you use in queries. Use `vector_cosine_ops` for cosine distance (`<=>`), `vector_l2_ops` for Euclidean distance (`<->`), and `vector_ip_ops` for negative inner product (`<#>`). Using a mismatched operator prevents index usage. For example, creating an index with `vector_cosine_ops` but querying with `<->` (L2 distance) forces a sequential scan.

```
-- Create IVFFlat index for cosine distance
CREATE INDEX ON products
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 1000);

```

The `lists` parameter determines how finely the vector space is partitioned. More lists create smaller partitions, which means fewer vectors to search per query but also more risk of missing relevant vectors in adjacent partitions. For datasets up to 100,000 rows, 100 lists are sufficient. For 100,000 to one million rows, use 1,000 lists. For one to ten million rows, use 4,000\-10,000 lists. For over ten million rows, use sqrt(rows). For two million products, start with lists between 1,500 and 2,000\.

The `ivfflat.probes` parameter controls how many lists are searched per query. Higher values improve recall but increase query time. Start with probes equal to sqrt(lists) and adjust based on measured recall. For 1,000 lists, begin with 30\-50 probes. If recall is too low (missing relevant results), increase probes. If queries are too slow, decrease probes. Configure probes with `SET ivfflat.probes = 20;` before executing your vector search.

IVFFlat indexes offer fast build times (k\-means clustering is efficient), lower memory usage (the index stores centroids and pointers, not duplicated vector data), and runtime tunability (adjust `probes` without rebuilding the index). However, they require training data (indexes built on small samples perform poorly), have a lower recall ceiling (even with high probes, recall might not reach 99%\+ for some data distributions), and need rebuilding when data distribution changes significantly.

### HNSW indexes

HNSW (Hierarchical Navigable Small World) indexes organize vectors into a multi\-layer graph structure that enables efficient navigation from any starting point to the nearest neighbors. HNSW builds a graph where each vector is a node connected to its nearest neighbors. The graph has multiple layers, with higher layers containing fewer nodes that serve as "express lanes" for navigation. When you query, HNSW starts at a fixed entry point in the top layer, greedily moves toward the query vector using the sparse upper layers, then refines the search in the dense bottom layer. This hierarchical navigation typically finds excellent results while visiting a small fraction of nodes.

Create an HNSW index by specifying the connections per node (`m`) and construction search width (`ef_construction`). The same operator class rules apply: use `vector_cosine_ops` for cosine distance (`<=>`), `vector_l2_ops` for L2 distance (`<->`), and `vector_ip_ops` for inner product (`<#>`).

```
-- Create HNSW index for cosine distance
CREATE INDEX ON products
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

```

The `m` parameter controls how many connections each node maintains to other nodes. Higher values create a denser graph with better recall but higher memory usage and longer build times. Start with `m = 16` for most workloads. Increase to 32 if you need higher recall and can accept the memory and build time costs. The `ef_construction` parameter controls the search width during index building. Higher values create a better\-quality graph but increase build time. Set `ef_construction` to at least `2 * m`. For high\-quality indexes, use `4 * m` or higher. This parameter doesn't affect index size or query time, only build time and resulting graph quality.

The `hnsw.ef_search` parameter controls the search width at query time, similar to how `probes` works for IVFFlat. The default value of 40 works well for many applications. For high\-accuracy requirements, increase to 100\-200\. The value should be at least as large as the number of results you request (the `LIMIT` clause). Configure ef\_search with `SET hnsw.ef_search = 100;` before executing your vector search.

HNSW indexes offer higher recall (typically achieves 99%\+ with appropriate parameters), no training dependency (index quality doesn't depend on data distribution), and consistent performance (query time is predictable regardless of where results fall in the vector space). However, they require higher memory usage (the graph structure requires significant storage, approximately 1\.5x the vector data size for m\=16\), longer build times (building the graph is computationally expensive), and fixed parameters (changing `m` or `ef_construction` requires rebuilding the index)

### Choose an index type

The choice between IVFFlat and HNSW depends on your requirements and constraints.

Note

Azure Database for PostgreSQL also supports [DiskANN indexes](/en-us/azure/postgresql/flexible-server/how-to-use-pgdiskann), which offer high recall, fast build times, and excellent performance for large datasets (100 million\+ vectors). DiskANN is an Azure\-specific feature worth considering for enterprise\-scale workloads.

Choosing between IVFFlat and HNSW indexes includes several factors based on your specific constraints and requirements. Memory availability, acceptable build times, recall requirements, and how frequently your data changes all affect which index type works best. Choose IVFFlat when memory budget is limited, build time tolerance is low, 90\-95% recall is acceptable, or data update frequency involves frequent bulk updates. Choose HNSW when memory is ample, you can tolerate longer build times, 99%\+ recall is needed, or the workload is mostly reads with small updates.

For a high\-traffic recommendation engine (the module scenario), HNSW is typically the better choice because the higher recall ensures users see the most relevant products, and the consistent sub\-10ms query latency supports high concurrency. For large catalogs with frequent updates, IVFFlat might be more practical if you frequently add or update large batches of products. For memory\-constrained environments, IVFFlat's lower memory footprint makes it viable when HNSW would exceed available memory. For development and testing, IVFFlat's faster build times make iteration quicker.

Sequential scans without indexes might be acceptable when tables have fewer than 10,000 rows, queries already filter to small subsets before vector search, you need guaranteed exact results (100% recall), or data changes so frequently that index maintenance overhead exceeds query savings.

### Create and maintain indexes

Proper index creation and maintenance ensures consistent performance as your data evolves.

Index creation locks the table for writes by default. For production systems, use `CONCURRENTLY` to allow writes during index building. Concurrent index creation takes longer and requires more resources, but prevents application downtime. Monitor the build progress with `SELECT phase, blocks_total, blocks_done, tuples_total, tuples_done FROM pg_stat_progress_create_index;`.

```
-- Build index without blocking writes
CREATE INDEX CONCURRENTLY idx_products_embedding
ON products USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

```

Build times vary with hardware, but these rough estimates help with planning: IVFFlat (lists\=1000\) takes 5\-15 minutes for one million vectors and 30\-60 minutes for ten million vectors. HNSW (m\=16, ef\=64\) takes 15\-45 minutes for one million vectors and 2\-6 hours for ten million vectors. HNSW build times increase more than linearly with data size. Plan accordingly for large datasets.

Index quality degrades when data distribution changes significantly. Signs that reindexing might help include query latency that has increased without data growth explaining it, recall measurements showing degradation, or large portions of data that have been replaced or updated. Reindex using `REINDEX INDEX CONCURRENTLY idx_products_embedding;`. For IVFFlat indexes, reindexing updates the cluster centroids to match current data distribution. For HNSW indexes, it rebuilds the graph structure.

Check index size and usage statistics to monitor index health. Query `pg_stat_user_indexes` to see index sizes with `SELECT indexrelname, pg_size_pretty(pg_relation_size(indexrelid)) AS size FROM pg_stat_user_indexes WHERE relname = 'products';`. Check if indexes are being used with `SELECT indexrelname, idx_scan, idx_tup_read FROM pg_stat_user_indexes WHERE relname = 'products';`. Low `idx_scan` counts suggest the index isn't being used. Verify that query operators match the index operator class.

### Additional resources

* [pgvector indexing documentation](https://github.com/pgvector/pgvector#indexing)
* [Indexing best practices for Azure Database for PostgreSQL](/en-us/azure/postgresql/monitor/concepts-autonomous-tuning)
* [HNSW algorithm paper](https://arxiv.org/abs/1603.09320)

---

## Optimize data layout

Data modeling decisions significantly affect vector search performance. How you structure tables, choose data types for metadata, and create supporting indexes determines whether queries execute efficiently as your dataset grows.

Note

Code examples in this unit demonstrate schema design patterns for vector data with metadata. Adapt these patterns to your specific data model and query requirements.

### Vector storage considerations

Vector columns consume substantial storage and processing resources. Understanding the storage characteristics helps you make informed decisions about schema design.

Each vector dimension adds 4 bytes of storage (for single\-precision float) plus fixed overhead. The relationship between dimensions and storage is linear:

| Dimensions | Bytes per vector | 1 million vectors |
| --- | --- | --- |
| 384 | \~1\.5 KB | \~1\.5 GB |
| 768 | \~3 KB | \~3 GB |
| 1536 | \~6 KB | \~6 GB |
| 3072 | \~12 KB | \~12 GB |

For a product catalog with two million items using 1536\-dimensional embeddings, the vector column alone requires approximately 12 GB of storage. Adding HNSW indexes increases this by roughly 50%.

Many embedding models offer multiple dimension options. Lower dimensions reduce storage and computation costs while maintaining reasonable quality for many use cases. Specifying dimensions in the column definition provides validation. Attempts to insert vectors with different dimensions fail with an error, preventing subtle bugs from mismatched embedding models. Define your table with an explicit dimension constraint using `embedding vector(768)` in the column definition.

Some applications need vectors from different models. For example, you might store product title embeddings, image embeddings, and user behavior embeddings separately. Each vector column needs its own index because you can't create a single index that covers multiple vector columns.

```
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    title_embedding vector(768),      -- Text embedding model
    image_embedding vector(512),       -- Image embedding model
    category_id INTEGER,
    price NUMERIC(10,2)
);

-- Create separate indexes for each embedding type
CREATE INDEX ON products USING hnsw (title_embedding vector_cosine_ops);
CREATE INDEX ON products USING hnsw (image_embedding vector_cosine_ops);

```

### Metadata data types: structured columns versus JSONB

Product recommendations rarely use vector similarity alone. Queries typically filter by category, price range, availability, or other attributes before or alongside vector search. How you store this metadata affects query performance.

Structured columns use PostgreSQL's native data types (INTEGER, TIMESTAMP, NUMERIC, TEXT) with explicit schema. These columns offer query performance benefits because native types enable efficient B\-tree indexes for equality and range queries, storage efficiency through optimized storage formats, type safety through insert\-time validation, and query optimization through accurate planner statistics. Use structured columns when attributes are known at design time, you frequently filter or sort by specific attributes, or query performance is critical.

```
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    embedding vector(1536),
    category_id INTEGER NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    in_stock BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    brand TEXT,
    rating NUMERIC(2,1)
);

```

JSONB stores semi\-structured data as binary JSON, offering flexibility for dynamic attributes. JSONB provides schema flexibility (different products can have different attributes), easy evolution (add new attributes without schema migrations), and nested structures (store complex hierarchical data). However, JSONB has query overhead (extracting values requires parsing), index limitations (GIN indexes work for containment queries but not range queries), and planner uncertainty (statistics are less precise for JSONB contents).

For filtered vector searches, the metadata filter performance directly affects total query time. Structured columns with B\-tree indexes enable PostgreSQL to quickly narrow candidates before vector distance calculations, while JSONB requires different query patterns and index types. A structured column filter like `WHERE category_id = 5 AND price BETWEEN 100 AND 500` can use a B\-tree index on `(category_id, price)` to quickly identify candidate rows. A JSONB filter like `WHERE attributes @> '{"category": "electronics"}' AND (attributes->>'price')::numeric BETWEEN 100 AND 500` requires either a GIN index (which doesn't help with range queries on price) or a sequential scan of the JSONB column.

Many applications benefit from combining structured columns and JSONB: use structured columns for frequently filtered attributes where query performance matters, and JSONB for dynamic or rarely filtered attributes where schema flexibility is more valuable. This pattern lets you optimize the common case without sacrificing flexibility for edge cases.

```
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    embedding vector(1536),
    -- Structured columns for common filters
    category_id INTEGER NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    in_stock BOOLEAN DEFAULT true,
    -- JSONB for dynamic attributes
    attributes JSONB DEFAULT '{}'
);

```

### Metadata indexes for filtered searches

Metadata indexes complement vector indexes by accelerating the filtering phase of queries. Without proper metadata indexes, PostgreSQL might need to scan all rows to apply filters before vector search.

Create B\-tree indexes on columns used in WHERE clauses. Single\-column indexes handle exact matches, while composite indexes handle filter combinations. Composite indexes are most effective when queries filter on the leftmost columns. An index on `(category_id, price)` efficiently handles `WHERE category_id = 5` and `WHERE category_id = 5 AND price < 100`, but it doesn't help with `WHERE price < 100` alone because price isn't the leftmost column.

```
-- Single-column index for exact matches
CREATE INDEX idx_products_category ON products (category_id);

-- Composite index for common filter combinations
CREATE INDEX idx_products_category_price ON products (category_id, price);

```

If most queries filter on the same condition (such as in\-stock products), a partial index reduces index size and improves performance. This index is smaller than a full index and is used only for queries that include `WHERE in_stock = true`. For an e\-commerce recommendation engine where nearly all queries target available products, this can significantly reduce index maintenance overhead. Create a partial index with `CREATE INDEX idx_products_instock_category ON products (category_id) WHERE in_stock = true;`.

If you use JSONB for attributes, GIN indexes support containment queries using the `@>` (contains), `<@` (contained by), `?` (key exists), and `?|`/`?&` (any/all keys exist) operators. They don't accelerate range queries or arbitrary JSON path expressions. Create a GIN index with `CREATE INDEX idx_products_attributes ON products USING gin (attributes);`. For frequently queried JSONB fields that need range queries, consider expression indexes. Create an expression index on a JSONB field extracted as numeric with `CREATE INDEX idx_products_json_price ON products (((attributes->>'price')::numeric));` to enable range queries on that field.

### Combine vector search with metadata filters

PostgreSQL executes queries by combining index scans with filtering. Understanding execution patterns helps you write efficient queries.

The most efficient pattern applies metadata filters first, reducing the set of vectors that need similarity calculations. PostgreSQL uses metadata indexes to identify products matching the filters, then applies vector similarity only to those candidates. If 5% of products match the filters, you're searching 100,000 vectors instead of 2 million.

```
-- Efficient: filter narrows candidates before vector search
SELECT id, name, embedding <=> $1 AS distance
FROM products
WHERE category_id = 5
  AND in_stock = true
  AND price BETWEEN 100 AND 500
ORDER BY embedding <=> $1
LIMIT 10;

```

Use `EXPLAIN ANALYZE` to verify that queries use expected indexes and to identify performance bottlenecks. The query plan shows whether PostgreSQL uses your metadata indexes to filter candidates before vector search, or whether it resorts to sequential scans that examine every row. Look for **Index Scan** or **Bitmap Index Scan** on metadata columns (efficient), **Index Scan** using the vector index (efficient), and **Seq Scan** on large tables (potentially inefficient). If you see unexpected sequential scans, check that appropriate indexes exist and that statistics are current using `ANALYZE products;`.

Some queries don't lend themselves to efficient filtering. When filters don't eliminate many rows (such as `WHERE price > 0` which nearly all products match), PostgreSQL might skip metadata indexes entirely and rely on the vector index alone. This is expected behavior because the optimizer makes cost\-based decisions.

Sometimes you need results from the vector index that also satisfy constraints not efficiently filterable beforehand. The post\-filtering pattern fetches more vector\-similar candidates than needed, then applies filters. Adjust the inner LIMIT based on expected filter selectivity.

```
-- Get more candidates than needed, then filter
WITH candidates AS (
    SELECT id, name, price, in_stock, embedding <=> $1 AS distance
    FROM products
    ORDER BY embedding <=> $1
    LIMIT 100
)
SELECT id, name, distance
FROM candidates
WHERE in_stock = true AND price BETWEEN 100 AND 500
ORDER BY distance
LIMIT 10;

```

### Table partitioning for large datasets

Partitioning divides a large table into smaller, more manageable pieces. For vector workloads, partitioning can improve query performance and simplify maintenance.

Consider partitioning when tables exceed tens of millions of rows, queries naturally filter by partition key (date, category, tenant), you need to efficiently drop old data (partition pruning), or index build times become prohibitive on the full table.

For applications that process time\-series embeddings (such as user activity vectors or content published over time), range partitioning by date is effective. Queries that filter by date scan only relevant partitions. Each partition has its own indexes, making maintenance more manageable.

```
-- Create partitioned table
CREATE TABLE user_interactions (
    id BIGSERIAL,
    user_id BIGINT NOT NULL,
    embedding vector(768),
    created_at TIMESTAMP NOT NULL,
    interaction_type TEXT
) PARTITION BY RANGE (created_at);

-- Create partitions for each month
CREATE TABLE user_interactions_2025_01
    PARTITION OF user_interactions
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

```

For multitenant applications or product catalogs with natural categories, list or hash partitioning can help. Queries filtered by category scan only the relevant partition, reducing both data scanned and index size.

Create indexes on the parent table to automatically create matching indexes on all partitions using `CREATE INDEX ON products USING hnsw (embedding vector_cosine_ops);`. Each partition has its own index, which can be built or rebuilt independently. This is valuable for large datasets where rebuilding a single global index would take hours.

Partitioning adds complexity. Queries that span many partitions might be slower than on a single table. Cross\-partition unique constraints require the partition key in the constraint. Application logic might need awareness of partition boundaries. Evaluate whether your query patterns align with potential partition keys before implementing partitioning.

### Additional resources

* [Table partitioning in PostgreSQL](https://www.postgresql.org/docs/current/ddl-partitioning.html)
* [JSONB indexing strategies](https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING)
* [Index types in PostgreSQL](https://www.postgresql.org/docs/current/indexes-types.html)

---

## Scale for high\-volume workloads

As vector workloads grow beyond what a single database server can handle efficiently, you need strategies to scale capacity while managing costs. Azure Database for PostgreSQL provides several scaling options that address different aspects of the performance challenge.

### Vertical scaling on Azure

Vertical scaling increases the compute and memory resources available to your database server. For vector workloads, this directly addresses the CPU\-intensive nature of similarity calculations and the memory requirements for keeping indexes cached.

Azure Database for PostgreSQL offers three compute tiers with different resource allocations. Each tier targets different workload profiles, balancing cost against performance capabilities. For vector search workloads, the memory\-per\-vCore ratio is important because it determines how much index data can remain cached in memory.

| Tier | vCores | Memory per vCore | Best for |
| --- | --- | --- | --- |
| Burstable | 1\-20 | 2 GB | Development, low\-traffic workloads |
| General Purpose | 2\-96 | 4 GB | Balanced production workloads |
| Memory Optimized | 2\-96 | 8 GB | Large working sets, vector workloads |

For the product recommendation scenario with two million vectors and high concurrency, Memory Optimized tiers provide the best fit. The extra memory per vCore helps keep HNSW indexes cached, reducing disk I/O during queries.

Vector query performance scales with both CPU cores (for parallel distance calculations) and memory (for index caching). For datasets under one million vectors, start with General Purpose 4\-8 vCores, monitor memory pressure and cache hit ratios, and scale up if CPU utilization consistently exceeds 70% during peak load. For datasets of one to ten million vectors, start with Memory Optimized 8\-16 vCores, ensure memory exceeds vector index size by at least 50%, and consider 32\+ vCores for high concurrency (hundreds of concurrent queries). For datasets over ten million vectors, Memory Optimized 32\+ vCores is typically required. Evaluate whether read replicas can distribute load, and consider architectural changes (partitioning, caching layer).

Vertical scaling has diminishing returns and hard limits. Scale up (larger server) when single\-query latency is too high, memory pressure causes excessive disk I/O, or you haven't reached the tier's maximum resources. Scale out (replicas or caching) when total query volume exceeds what one server can handle, you have a read\-heavy workload with acceptable staleness, or you hit vertical scaling limits. Vertical scaling is simpler to implement and manage. Start by scaling up until you hit limits or cost becomes prohibitive, then add horizontal scaling.

### Read replicas for query distribution

Read replicas maintain copies of your primary database that handle read queries independently. For vector search workloads that are predominantly reads, replicas can multiply your query capacity.

Azure Database for PostgreSQL uses physical streaming replication to keep replicas synchronized with the primary server. Changes written to the primary are streamed to replicas, which apply them asynchronously. The primary server handles both reads and writes, while each replica handles read queries only. You can create up to five read replicas per primary, and replicas can be located in different Azure regions. Each replica has its own connection endpoint, so your application must route queries to the appropriate server.

Because replication is asynchronous, replicas might be slightly behind the primary. This lag is typically milliseconds to seconds under normal conditions but can increase during heavy write activity on the primary, large transactions or bulk loads, network congestion between regions, or replica resource constraints. For product recommendations, replica lag is often acceptable. If a new product is added, its appearance in recommendations a few seconds later doesn't affect user experience. However, if your application requires immediate consistency (such as showing a user's just\-updated preferences), those queries should go to the primary. Monitor replica lag using Azure Monitor metrics or query the replica directly with `SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) AS lag_seconds;`.

Your application must direct queries to appropriate servers. Common patterns include application\-level routing (choosing connection based on query type), DNS\-based routing (using Azure Traffic Manager or custom DNS to distribute connections across replicas), and connection proxy (PgBouncer or similar proxies that route queries based on patterns). For the recommendation engine scenario, vector similarity searches are ideal candidates for replica routing since they're read\-only and tolerance for slight staleness is high.

Replicas can be sized independently from the primary. For read\-heavy vector workloads, you might use smaller replicas if query volume is the constraint (more replicas, smaller each), use equal or larger replicas if individual query performance matters, or place replicas in regions close to users for lower latency.

### Cache strategies for vector search

Caching reduces database load by serving repeated queries from faster storage. Vector search workloads have specific caching opportunities.

Not all vector search results benefit equally from caching. The best candidates have high request frequency, low change rates, and bounded key spaces. Random similarity queries against arbitrary vectors have an infinite query space and don't cache well, but lookups for specific items or precomputed recommendations cache effectively. Good caching candidates include popular product embeddings requested frequently, precomputed "similar items" for top products, user embedding lookups for personalization, and category\-level aggregate embeddings. Poor caching candidates include arbitrary vector similarity queries (infinite query space), rapidly changing data (high invalidation rate), and queries with many filter combinations.

Azure Cache for Redis provides sub\-millisecond response times for cached data. For vector workloads, consider caching embedding lookups and precomputed recommendations. The following example demonstrates caching product embeddings with a one\-hour TTL.

```
import redis
import json

redis_client = redis.Redis(host='your-cache.redis.cache.windows.net',
                          port=6380, ssl=True, password='your-key')

def get_product_embedding(product_id):
    cache_key = f"embedding:{product_id}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    # Fetch from database
    embedding = fetch_embedding_from_db(product_id)

    # Cache for 1 hour
    redis_client.setex(cache_key, 3600, json.dumps(embedding))
    return embedding

```

Stale recommendations are usually acceptable for short periods, but eventually caches need refreshing. The right invalidation strategy depends on how quickly your data changes and how sensitive users are to outdated results. Most vector search applications can tolerate minutes of staleness, making simple time\-based expiration effective. Set TTL (time to live) based on acceptable staleness. For product recommendations, 15\-60 minutes is often reasonable. For event\-driven invalidation, clear specific cache entries when underlying data changes. For background refresh, proactively refresh popular items before expiration to avoid cache misses.

### Monitor capacity and plan for growth

Proactive monitoring helps you scale before performance degrades noticeably.

Track database\-level metrics through Azure Monitor including CPU percentage (sustained \>70% indicates scaling need), memory percentage (approaching limits causes swapping), storage IO percentage (high values suggest insufficient caching), and active connections (approaching max\_connections indicates pooling issues). Also track query\-level metrics including P95/P99 query latency for vector searches, query throughput (queries per second), and cache hit ratio (if using PostgreSQL's buffer cache effectively).

Configure Azure Monitor alerts to notify you before problems affect users. Set a warning alert when CPU percentage exceeds 80% for 5 minutes to send email to the ops team. Set a critical alert when memory percentage exceeds 90% for 5 minutes to page the on\-call engineer.

Effective capacity planning requires understanding your current usage patterns and projecting future needs. Without this foundation, you risk either over\-provisioning (wasting budget) or under\-provisioning (degrading user experience during growth). Establish baselines by measuring current query volume, latency, and resource utilization during normal and peak periods. Identify growth drivers such as catalog size growth, user growth, or query complexity changes. Model future load by projecting resource needs based on growth rate. If your catalog doubles annually and you're at 60% CPU, plan to scale within six months. Test scaling options before you need them by validating vertical scaling and replica deployment in non\-production environments. Document thresholds that define when each scaling action should trigger.

### Cost optimization

Performance optimization must balance against budget constraints. Several strategies help control costs while maintaining acceptable performance.

Over\-provisioning wastes money while under\-provisioning hurts users. Review resource utilization regularly. If average CPU is below 30%, consider scaling down. If memory utilization is consistently low, General Purpose might suffice instead of Memory Optimized. If you have replicas with low utilization, consolidate.

Azure offers significant discounts (up to 65%) for one\-year or three\-year reserved capacity commitments. If your baseline workload is predictable, reservations reduce costs substantially. Calculate your baseline (minimum always\-on capacity) and reserve that amount. Use on\-demand pricing for burst capacity above the baseline.

Storage costs accumulate for large vector datasets. Remove unused indexes (each HNSW index adds \~50% to vector storage). Archive old vectors that are rarely queried. Use appropriate precision (float4 vs float8\) for your accuracy needs.

Non\-production environments don't need production\-scale resources. Use Burstable tier for development. Scale down staging when not in active testing. Use smaller datasets in non\-production (representative samples, not full copies).

### Additional resources

* [Compute and storage options in Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/concepts-compute-storage)
* [Read replicas in Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/concepts-read-replicas)
* [Azure Cache for Redis documentation](/en-us/azure/azure-cache-for-redis/)
* [Azure Monitor for Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/concepts-monitoring)

---

## Connection optimization

Database connections are expensive resources. Each connection consumes server memory, requires authentication overhead, and counts against server limits. For AI applications that make frequent vector queries, efficient connection management is essential for achieving high throughput without exhausting resources.

Note

Code examples in this unit demonstrate connection management patterns for Python (psycopg) and .NET (Npgsql). These libraries are updated frequently. Visit the [psycopg documentation](https://www.psycopg.org/psycopg3/docs/) and [Npgsql documentation](https://www.npgsql.org/doc/) for current API details.

### Connection overhead

Creating a new PostgreSQL connection involves multiple steps, each adding latency:

1. **TCP handshake:** Establishing the network connection (typically 1\-3 round trips)
2. **TLS negotiation:** Encrypting the connection (required for Azure Database for PostgreSQL)
3. **Authentication:** Verifying credentials (password or token exchange)
4. **Server process allocation:** PostgreSQL spawns a backend process for each connection
5. **Session initialization:** Setting session parameters and loading configurations

This sequence takes 50\-200 milliseconds depending on network latency and server load. For a recommendation engine handling thousands of requests per second, creating new connections per request would consume more time in connection setup than in actual query execution.

Azure Database for PostgreSQL limits concurrent connections based on compute tier. Burstable B1ms allows 50 connections, General Purpose 2 vCores allows 859 connections, General Purpose 4 vCores allows 1,718 connections, Memory Optimized 4 vCores allows 3,437 connections, and Memory Optimized 16 vCores allows 5,000 connections. Exceeding these limits causes connection failures. Applications that create connections per request can quickly hit these limits during traffic spikes.

### Connection pooling with PgBouncer

PgBouncer is a lightweight connection pooler that sits between your application and PostgreSQL. It maintains a pool of database connections and multiplexes client connections across them, dramatically reducing the number of actual database connections needed.

Azure Database for PostgreSQL includes built\-in PgBouncer support on General Purpose and Memory Optimized compute tiers. The Burstable tier doesn't support this feature. Enable PgBouncer through the Azure portal or CLI. Once enabled, connect through port 6432 (the PgBouncer port) instead of 5432 (the direct PostgreSQL port). The PgBouncer connection string uses `postgresql://user:password@myserver.postgres.database.azure.com:6432/mydb`.

```
az postgres flexible-server parameter set \
    --resource-group myResourceGroup \
    --server-name myserver \
    --name pgbouncer.enabled \
    --value true

```

PgBouncer supports three pooling modes, each with different trade\-offs. Session mode means a client holds a server connection for the entire session (until disconnect). This mode supports all PostgreSQL features but provides minimal connection reduction. Transaction mode means a client holds a server connection only during a transaction. Between transactions, the connection returns to the pool. This mode works well for most applications and significantly reduces connection requirements. Statement mode means a client gets a connection only for individual statements. This mode provides maximum connection reduction but doesn't support multi\-statement transactions. For vector search workloads, transaction mode is typically the best choice.

PgBouncer exposes several parameters that control pool behavior, connection limits, and timeout handling. For vector search workloads with bursty traffic patterns, tuning these parameters helps balance connection availability against resource consumption. Configure `pgbouncer.default_pool_size` (20\-50 depending on concurrency needs), `pgbouncer.max_client_conn` (5000\+ for high\-traffic applications), `pgbouncer.pool_mode` (transaction), and `pgbouncer.query_wait_timeout` (30\-120 seconds).

Transaction mode returns connections to the pool after each transaction commits or rolls back. This affects several PostgreSQL features. Session variables reset between transactions, so settings applied with `SET` don't persist across transactions. Use `SET LOCAL` within transactions or configure defaults server\-side. Prepared statements might not work because named prepared statements are tied to connections. In transaction mode, a prepared statement created in one transaction might not be available in the next if a different connection is assigned. LISTEN/NOTIFY doesn't work because these features require persistent connections and are incompatible with transaction pooling. For vector search applications, these limitations are rarely problematic since queries are typically simple selects without session\-specific state.

### Application\-level connection pooling

In addition to (or instead of) PgBouncer, your application can manage connection pools directly. This provides finer control over connection lifecycle and integrates with application frameworks.

The `psycopg_pool` package provides connection pooling for psycopg. Application\-level pools give you control over connection lifecycle, idle timeout behavior, and health checking. They also integrate naturally with your application's error handling and logging. When combined with PgBouncer, application pools handle local connection management while PgBouncer handles server\-side multiplexing. The `with pool.connection()` context manager automatically returns the connection to the pool when the block exits, even if an exception occurs.

```
from psycopg_pool import ConnectionPool

## Create a connection pool
pool = ConnectionPool(
    conninfo="postgresql://user:password@myserver.postgres.database.azure.com:6432/mydb",
    min_size=5,      # Minimum connections to maintain
    max_size=20,     # Maximum connections allowed
    max_idle=300,    # Close idle connections after 5 minutes
    max_lifetime=3600  # Recycle connections after 1 hour
)

## Use connections from the pool
def search_similar_products(query_embedding, limit=10):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, embedding <=> %s AS distance
                FROM products
                ORDER BY embedding <=> %s
                LIMIT %s
            """, (query_embedding, query_embedding, limit))
            return cur.fetchall()

```

Npgsql includes built\-in connection pooling enabled by default, so you don't need a separate package. The pool automatically manages connection creation, reuse, and disposal based on parameters you specify in the connection string. Each unique connection string maintains its own pool, so consistent connection strings across your application ensure efficient pool utilization. When you call `conn.Close()` or the connection is disposed, it returns to the pool rather than being destroyed. Configure pooling through connection string parameters like `Minimum Pool Size=5;Maximum Pool Size=20;Connection Idle Lifetime=300;Connection Lifetime=3600`.

Pool size affects both performance and resource consumption. Setting the pool too small causes requests to wait for available connections, increasing latency. Setting it too large wastes memory and can overwhelm the database server. The right size depends on your traffic patterns, query duration, and the number of application instances sharing the database. Keep minimum size large enough to handle baseline traffic without waiting. Cap maximum size at what the database can handle divided by the number of application instances. If you have 10 application instances and your database supports 1,000 connections, set maximum to 100 per instance (leaving headroom). Recycle connections periodically (every 30\-60 minutes) to maintain health because long\-lived connections might accumulate memory leaks or hold stale cached plans.

### Session management for AI workloads

Some vector queries benefit from session\-level settings that allocate more resources to the query than the server\-wide defaults allow.

Vector similarity queries that sort large result sets benefit from increased `work_mem`. Set it for specific sessions or transactions using `SET LOCAL work_mem = '256MB'`. `SET LOCAL` applies only within the current transaction. When the transaction ends, the setting reverts to the default, which is safe for pooled connections.

Adjust `hnsw.ef_search` or `ivfflat.probes` for queries with different accuracy requirements. Use `SET LOCAL hnsw.ef_search = 200` for higher recall in queries where accuracy is critical, or `SET LOCAL hnsw.ef_search = 20` for faster queries where approximate results are acceptable. This pattern lets you balance accuracy and speed based on the specific use case without affecting other queries.

### Efficient SDK usage patterns

Beyond connection management, how you structure database interactions affects performance.

Network round trips add latency to every database operation. When you need multiple pieces of data, fetching them in a single query eliminates the per\-query overhead of network transmission, query parsing, and result serialization. For AI applications that retrieve embeddings for multiple items, batching can reduce total latency from hundreds of milliseconds to single digits. Instead of making multiple round trips with individual queries, use a single query with `WHERE id = ANY(%s)` and pass a list of IDs.

For loading large numbers of vectors, the PostgreSQL `COPY` command is dramatically faster than individual `INSERT` statements. `COPY` streams data directly into the table in a binary or text format, bypassing the overhead of parsing individual SQL statements. When loading embedding data from batch processing pipelines or initial data migrations, `COPY` can reduce load times from hours to minutes. `COPY` can load hundreds of thousands of rows per second, while individual inserts are limited to thousands per second.

When your application can parallelize work, async database operations improve throughput by executing multiple queries concurrently without blocking threads. This pattern is valuable for AI workloads that need to search multiple vector collections simultaneously or combine vector search with other data retrieval. Async pools manage connections efficiently across concurrent operations while respecting pool size limits. Use `AsyncConnectionPool` from psycopg\_pool and `asyncio.gather` to execute multiple searches concurrently.

### Connection resilience

Network issues, server restarts, and failovers can interrupt database connections. Robust applications handle these gracefully.

Transient failures such as network blips, connection resets, and brief server unavailability during maintenance are inevitable in cloud environments. Implementing retry logic with exponential backoff helps your application recover gracefully from these temporary issues without overwhelming the server with immediate retry attempts. Add random jitter to prevent multiple application instances from retrying simultaneously. Catch `OperationalError` exceptions, calculate wait time as `(2 ** attempt) + random.uniform(0, 1)`, and retry up to a maximum number of attempts.

Timeouts prevent your application from waiting indefinitely when the database is slow or unreachable. Connection timeouts limit how long to wait when establishing new connections, while statement timeouts limit query execution time. For vector search applications, choose timeouts that accommodate your slowest legitimate queries while failing fast on queries that exceed acceptable latency. Configure timeouts in your connection string using parameters like `connect_timeout=10` and `options=-c statement_timeout=30000`. For vector queries, set statement timeouts that accommodate your slowest acceptable queries. A 30\-second timeout is reasonable for complex vector searches; interactive applications might use lower values.

When all pool connections are in use and new requests arrive, the pool must either queue requests (adding latency) or reject them immediately. Neither option is ideal, so monitoring pool utilization helps you scale before exhaustion becomes frequent. When exhaustion does occur, returning a clear error message helps clients implement their own retry logic rather than timing out unpredictably. Handle `PoolTimeout` exceptions by returning a graceful error like `{"error": "Service temporarily busy, please retry"}`. Monitor pool utilization and scale if exhaustion happens frequently.

### Additional resources

* [PgBouncer in Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/concepts-pgbouncer)
* [psycopg connection pool documentation](https://www.psycopg.org/psycopg3/docs/api/pool.html)
* [Npgsql connection pooling](https://www.npgsql.org/doc/connection-string-parameters.html#pooling)

---

## Exercise \- Optimize vector search performance in Azure Database for PostgreSQL

In this exercise, you deploy an Azure Database for PostgreSQL instance and optimize it for vector search workloads. You create test data with vector embeddings, analyze baseline performance, build and compare IVFFlat and HNSW indexes, and tune search parameters. These techniques are essential for production AI applications that require fast similarity search across large datasets.

Tasks performed in this exercise:

* Download project starter files and configure the deployment script
* Deploy an Azure Database for PostgreSQL Flexible Server with Microsoft Entra authentication
* Create a test dataset with vector embeddings
* Analyze baseline vector search performance without indexes
* Create and compare IVFFlat and HNSW vector indexes
* Tune index parameters to balance speed and recall

This exercise takes approximately **30** minutes to complete.

### Before you start

To complete the exercise, you need:

* An Azure subscription with the permissions to deploy the necessary Azure services. If you don't already have one, you can [sign up for one](https://azure.microsoft.com/).
* [Visual Studio Code](https://code.visualstudio.com/) on one of the [supported platforms](https://code.visualstudio.com/docs/supporting/requirements#_platforms).
* The latest version of the [Azure CLI](/en-us/cli/azure/install-azure-cli).
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

In this module, you learned how to optimize Azure Database for PostgreSQL and pgvector for AI workloads. You explored PostgreSQL configuration parameters that affect vector query performance, including memory settings like `shared_buffers` and `work_mem`, and query planner settings optimized for SSD storage. You learned the differences between IVFFlat and HNSW vector indexes, understanding when each is appropriate based on dataset size, accuracy requirements, memory constraints, and build time tolerance. You configured index parameters like `lists`, `probes`, `m`, `ef_construction`, and `ef_search` to balance query speed against recall accuracy.

You discovered how data layout decisions affect filtered vector search performance. Structured columns with B\-tree indexes provide efficient filtering for common predicates, while JSONB with GIN indexes offers flexibility for dynamic attributes. You learned to combine vector similarity with metadata filters effectively, using query patterns that let PostgreSQL optimize execution plans. For large datasets, you explored table partitioning strategies that improve both query performance and maintenance operations.

You also learned scaling strategies for high\-volume vector workloads on Azure. Vertical scaling with Memory Optimized compute tiers keeps indexes cached in memory. Read replicas distribute query load for read\-heavy workloads. Application\-level caching with Azure Cache for Redis reduces database load for frequently requested data. Finally, you implemented connection optimization techniques including PgBouncer configuration in transaction mode and application\-level connection pooling to maximize throughput while staying within connection limits.

### Additional resources

* [pgvector extension for Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/how-to-use-pgvector)
* [Server parameters in Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/concepts-server-parameters)
* [PgBouncer in Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/concepts-pgbouncer)
* [Read replicas in Azure Database for PostgreSQL](/en-us/azure/postgresql/flexible-server/concepts-read-replicas)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/_

## Fuentes
- [Optimize vector search in Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/?WT.mc_id=api_CatalogApi)
