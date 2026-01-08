---
date: 2026-01-08T14:30:00Z
type: validation
status: VALIDATED
plan_file: thoughts/shared/plans/2026-01-08-v1.2-database-pipeline-debugging.md
---

# Plan Validation: v1.2 Database Pipeline Debugging

## Overall Status: VALIDATED

All technical choices in the v1.2 Database Pipeline Debugging plan are current best practices for 2024-2025. The plan uses mature, well-supported technologies appropriate for a Tier 2 (Confidential Fab) production environment.

## Precedent Check (RAG-Judge)

**Note:** RAG-Judge not available (no Braintrust Artifact Index in this project yet).

**Relevant Past Work:**
- v1.0: Orchestrator Test Suite MVP completed (2026-01-07)
- v1.1: RAG Integration plan exists but not yet implemented
- This is the first major pipeline/lineage-focused feature in ATLASsemi

---

## Tech Choices Validated

### 1. SQL Server DMVs (sys.dm_sql_referenced_entities, sys.sql_modules)
**Purpose:** Extract database metadata and object dependencies
**Status:** VALID ✓
**Findings:**
- These are the current Microsoft-recommended approaches for dependency tracking
- `sys.sql_expression_dependencies` provides cross-database/cross-server dependencies (more comprehensive than older methods)
- `sp_depends` is deprecated; DMVs/DMFs are the modern replacement
- Permissions: Requires VIEW DATABASE STATE (SQL Server 2022+ requires VIEW DATABASE PERFORMANCE STATE)
- Limitation: Dynamic SQL dependencies won't be caught by `sys.sql_expression_dependencies`; need to search `sys.sql_modules` text for those
**Recommendation:** Keep as-is. Consider adding `sys.sql_expression_dependencies` alongside `sys.dm_sql_referenced_entities` for cross-database dependencies.
**Sources:**
- [Revisiting Object Dependencies – Andy Brownsword](https://andybrownsword.co.uk/2024/05/07/revisiting-object-dependencies/)
- [sys.dm_sql_referenced_entities - Microsoft Learn](https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-sql-referenced-entities-transact-sql?view=sql-server-ver17)
- [Using sys.sql_expression_dependencies - SQLRx](https://www.sqlrx.com/using-sys-sql_expression_dependencies-as-a-single-source-to-find-referenced-and-referencing-objects/)

---

### 2. Power BI Admin Scanner API
**Purpose:** Extract lineage metadata from Power BI reports to datasets to data sources
**Status:** VALID ✓
**Findings:**
- Scanner API is actively maintained and enhanced (not deprecated)
- Recent updates (2024): Now includes scheduled refresh settings, RLS configuration, RDL data source properties, and more
- Microsoft Fabric compatible: Existing APIs work with Fabric workspaces
- Requires Power BI admin rights (service principal with appropriate permissions)
- API coverage for new Fabric objects is still evolving but core functionality is stable
**Recommendation:** Keep as-is. This is the official Microsoft API for metadata scanning and continues to receive active development.
**Sources:**
- [Scanner API includes more metadata - Microsoft Power BI Blog](https://powerbi.microsoft.com/en-us/blog/new-scanner-api-scenarios/)
- [Metadata scanning overview - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/governance/metadata-scanning-overview)
- [Power BI Admin APIs & Fabric - Microsoft Fabric Community](https://community.fabric.microsoft.com/t5/Service/Power-BI-Admin-APIs-amp-Fabric/m-p/3770032)

---

### 3. SQL Server 2025 Native Vectors (AI_GENERATE_EMBEDDINGS)
**Purpose:** Generate embeddings for SQL code using SQL Server's native AI capabilities
**Status:** VALID ✓ (with deployment consideration)
**Findings:**
- SQL Server 2025 RTM (Generally Available as of late 2024/early 2025) includes native vector support
- `AI_GENERATE_EMBEDDINGS` function uses EXTERNAL MODEL object to connect to embedding services (OpenAI, Azure OpenAI, Ollama)
- Performance gains: 2-5x faster queries via in-database parallelism, 70% latency drops in RAG apps (early adopters)
- DiskANN-powered vector indexes for scalable similarity search (billions of vectors)
- Half-precision (16-bit) vectors support up to ~4,000 dimensions
- Best practice: Start with Developer Edition for prototyping; use exact search for <50K vectors, approximate search (VECTOR_SEARCH with DiskANN index) for larger datasets
**Recommendation:** Keep as planned fallback. However, verify SQL Server version in production environment. If production uses SQL Server 2022 or earlier, native vectors won't be available - sentence-transformers becomes primary path.
**Sources:**
- [SQL Server 2025 Embraces Vectors - Azure SQL Devs' Corner](https://devblogs.microsoft.com/azure-sql/sql-server-2025-embraces-vectors-setting-the-foundation-for-empowering-your-data-with-ai/)
- [AI in SQL Server 2025: Embeddings - Simple Talk](https://www.red-gate.com/simple-talk/databases/sql-server/t-sql-programming-sql-server/ai-in-sql-server-2025-embeddings/)
- [SQL Server 2025 AI with OLLAMA - Architecture et Performance](https://www.architecture-performance.fr/ap_blog/get-your-embeddings-on-sql-server-2025-with-ai_generate_embeddings-and-external-model-using-ollama-local-and-your-gpu/)

---

### 4. sentence-transformers (Local Embeddings Fallback)
**Purpose:** Generate embeddings locally for Tier 2 security (no cloud APIs)
**Status:** VALID ✓
**Findings:**
- sentence-transformers remains the de facto standard for local embedding generation in 2024-2025
- Mature, widely used, integrates seamlessly with Python ecosystem
- Model choice: `all-MiniLM-L6-v2` is a good default (fast, 384 dimensions)
- Alternatives exist (OpenAI API, Cohere API, Universal Sentence Encoder) but violate Tier 2 security (cloud APIs)
- For speed/scale: ONNX Runtime or Triton Inference Server can accelerate inference, but sentence-transformers is sufficient for this use case
**Recommendation:** Keep as-is. sentence-transformers is the best choice for local, Tier 2-compliant embeddings. Model choice (`all-MiniLM-L6-v2`) is appropriate for code search.
**Sources:**
- [Comparing Popular Embedding Models - DEV Community](https://dev.to/simplr_sh/comparing-popular-embedding-models-choosing-the-right-one-for-your-use-case-43p1)
- [How do I choose embedding frameworks? - Zilliz](https://zilliz.com/ai-faq/how-do-i-choose-between-sentencetransformers-and-other-embedding-frameworks)
- [Best Open Source Sentence Embedding Models - Codesphere](https://codesphere.com/articles/best-open-source-sentence-embedding-models)

---

### 5. ChromaDB (Vector Storage)
**Purpose:** Store and query SQL code embeddings for semantic search
**Status:** VALID (with scaling consideration)
**Findings:**
- ChromaDB 2025 Rust rewrite delivers 4x faster writes and queries vs original Python implementation
- Strengths: Developer-friendly API, zero-config embedded deployment, local persistence (Tier 2 compliant)
- Limitations: Single-node architecture (hard to scale beyond one server), limited auth/multi-tenant controls
- Best use case: Rapid prototyping, embedded deployments, smaller datasets (<100K vectors)
- Alternatives for production scale: Milvus (35K+ GitHub stars, cloud-native, distributed), Qdrant (9K+ stars, real-time updates), Weaviate (8K+ stars)
**Recommendation:** Keep as-is for v1.2 MVP. ChromaDB is appropriate for initial deployment (<1,000 stored procedures). If scale exceeds 10K+ procedures or multi-tenancy is needed, plan migration to Milvus or Qdrant in v2.0.
**Sources:**
- [Best Vector Databases in 2025 - Firecrawl](https://www.firecrawl.dev/blog/best-vector-databases-2025)
- [Chroma vs Faiss vs Pinecone - Designveloper](https://www.designveloper.com/blog/chroma-vs-faiss-vs-pinecone/)
- [Milvus vs. Chroma DB - Zilliz](https://zilliz.com/blog/milvus-vs-chroma)

---

### 6. pyodbc (SQL Server Connection)
**Purpose:** Connect Python to SQL Server for metadata extraction
**Status:** VALID (with awareness of new alternative)
**Findings:**
- pyodbc is mature, stable, and widely used (de facto standard for SQL Server connections)
- Cross-platform support: Windows, Mac, Linux without code changes
- New alternative: `mssql-python` (Microsoft's new driver, 2024+) offers faster performance, eliminates Driver Manager dependencies, includes Direct Database Connectivity (DDBC)
- pymssql is also an option (pure Python, no ODBC drivers needed, smaller Docker images), but lacks SSL bindings for Azure SQL by default
**Recommendation:** Keep pyodbc for v1.2 (proven, stable). Consider `mssql-python` for v2.0 if performance becomes a bottleneck. For this use case (periodic metadata extraction), pyodbc is sufficient.
**Sources:**
- [mssql-python vs pyodbc Benchmarking - Microsoft Python Blog](https://devblogs.microsoft.com/python/mssql-python-vs-pyodbc-benchmarking-sql-server-performance/)
- [pymssql vs pyodbc - Medium](https://medium.com/reverse-engineering-by-amitabh/pymssql-vs-pyodbc-choosing-the-right-python-library-for-sql-server-4f39c1acc900)
- [Python drivers for SQL Server - Microsoft Learn](https://learn.microsoft.com/en-us/sql//connect/python/python-driver-for-sql-server?view=sql-server-ver16)

---

### 7. requests Library (Power BI API)
**Purpose:** Make HTTP requests to Power BI Admin API
**Status:** VALID ✓
**Findings:**
- requests is NOT deprecated (active maintenance, 40M+ downloads/month, 1.8M+ GitHub repos depend on it)
- Latest release: 2.28.2 (January 2024) with bug fixes and improvements
- httpx is a modern alternative with async support and HTTP/2, but not a replacement for general synchronous HTTP needs
- For this use case (synchronous API calls to Power BI Scanner API), requests is perfectly appropriate
**Recommendation:** Keep as-is. requests is the right choice for synchronous Power BI API calls. No need to switch to httpx unless async becomes a requirement.
**Sources:**
- [Are Python Requests Deprecated? - Web Scraping Site](https://webscrapingsite.com/blog/are-python-requests-deprecated-not-even-close/)
- [Python HTTP Clients Comparison - Speakeasy](https://www.speakeasy.com/blog/python-http-clients-requests-vs-httpx-vs-aiohttp)
- [Best Python HTTP Clients 2025 - Proxyway](https://proxyway.com/guides/the-best-python-http-clients)

---

### 8. Dependency Graph Approach (Structured Metadata vs Neo4j/Memgraph)
**Purpose:** Store and query lineage relationships between reports, datasets, procedures, tables
**Status:** VALID ✓ (start simple, evaluate graph DB later)
**Findings:**
- Neo4j is well-suited for complex dependency graphs (used in production for object dependency analysis)
- ISO approved GQL (Graph Query Language) standard in April 2024 - all major vendors moving toward compliance
- Neo4j 2025 advancements: AI integration, scalability, cloud-native features
- Graph databases excel when: >10K nodes, complex multi-hop queries, frequent graph algorithm use (PageRank, community detection)
- Structured metadata (JSON/relational) is sufficient for: <1K nodes, simple traversals (upstream/downstream), MVP validation
**Recommendation:** Keep as-is (start with structured metadata in v1.2). This is the right pragmatic approach. Re-evaluate Neo4j/Memgraph in v2.0 if:
  - Node count exceeds 5-10K
  - Query performance degrades (<3 sec target not met)
  - Need for graph algorithms (impact analysis, critical path identification)
**Sources:**
- [Knowledge Graph Extraction - Neo4j Blog](https://neo4j.com/blog/developer/knowledge-graph-extraction-challenges/)
- [Neo4j backs new graph query standard - Blocks and Files](https://blocksandfiles.com/2025/09/22/neo4j-genai-graph-interview/)
- [Software dependency analysis with Neo4j - INNOQ](https://www.innoq.com/en/talks/2015/05/neo4j-graph-database-graphconnect-2015/)

---

### 9. ProblemMode.DATA_PIPELINE Integration Pattern
**Purpose:** Extend ATLASsemi's agent architecture to support data pipeline debugging
**Status:** VALID ✓
**Findings:**
- Pattern follows existing ATLASsemi enum extension (EXCURSION, IMPROVEMENT, OPERATIONS)
- Clean separation of concerns: Pipeline context built separately, injected into Analysis Agent
- Mode-aware prompts are a proven pattern in the codebase
- Integration approach (PipelineOrchestrator) mirrors existing agent orchestration patterns
**Recommendation:** Keep as-is. This integration pattern is consistent with ATLASsemi's architecture and will maintain code maintainability.
**Sources:** (Internal codebase analysis - no external validation needed)

---

## Summary

### Validated (Safe to Proceed): ✓

All 9 technical choices are validated:

1. **SQL Server DMVs** ✓ - Current Microsoft recommendation
2. **Power BI Scanner API** ✓ - Actively maintained, Fabric-compatible
3. **SQL Server 2025 Vectors** ✓ - Production-ready (verify SQL version)
4. **sentence-transformers** ✓ - Best local embedding option for Tier 2
5. **ChromaDB** ✓ - Appropriate for MVP scale
6. **pyodbc** ✓ - Mature and stable
7. **requests** ✓ - Not deprecated, appropriate for sync HTTP
8. **Structured metadata first** ✓ - Right pragmatic approach
9. **ProblemMode.DATA_PIPELINE** ✓ - Consistent with architecture

### Needs Review: (None)

No tech choices require immediate changes.

### Must Change: (None)

No tech choices are deprecated or unsuitable.

---

## Recommendations

### For v1.2 Implementation:

All tech choices are current best practices. Plan is ready for implementation with these considerations:

1. **SQL Server Version Check:** Verify production SQL Server version before choosing between native vectors (2025+) vs sentence-transformers (2022 or earlier). sentence-transformers is the safer default for v1.2.

2. **Add sys.sql_expression_dependencies:** Consider querying this alongside `sys.dm_sql_referenced_entities` to capture cross-database dependencies.

3. **ChromaDB Scale Planning:** Document expected procedure count. If >5K procedures anticipated, note this for v2.0 migration planning to Milvus/Qdrant.

4. **Performance Baseline:** Establish performance baselines early (Phase 1-2) to validate <3 sec lineage query target before building on top of it.

### For Future Versions (v2.0+):

1. **Graph Database Migration:** Re-evaluate Neo4j/Memgraph if node count exceeds 5-10K or query performance degrades. GQL standard (2024) makes migration easier.

2. **mssql-python Driver:** Consider Microsoft's new `mssql-python` driver for performance gains if metadata extraction becomes a bottleneck.

3. **Vector Database Scale:** Plan ChromaDB → Milvus migration if vector count exceeds 100K or multi-tenancy is required.

---

**Validation Completed:** 2026-01-08
**Validator:** Claude Code Validation Agent
**Confidence Level:** HIGH (all choices validated against 2024-2025 sources)
