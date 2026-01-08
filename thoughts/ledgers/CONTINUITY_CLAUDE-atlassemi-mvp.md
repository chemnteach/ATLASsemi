# Continuity Ledger: ATLASsemi MVP Completion

```yaml
---
session_name: atlassemi-mvp
problem_mode: operations
security_tier: general_llm
api_routing: anthropic
started: 2026-01-07
last_updated: 2026-01-08 02:00
status: v1.0 COMPLETE ✅ | v1.1 Plan Validated ✅ | v1.2 Planning
version: 1.0.0 (deployed) | 1.1.0 (design phase) | 1.2.0 (planning)
---
```

## Goal

✅ **ACHIEVED - ATLASsemi v1.0 Production-Ready**

Completed:
- ✅ All 4 agents (Phases 0-3) implemented and working
- ✅ Orchestrator to chain agents automatically
- ✅ Comprehensive test suite (25 tests, 77% coverage)
- ✅ Deployment documentation (DEPLOYMENT.md, TESTING.md)
- ✅ GitHub repository established at https://github.com/chemnteach/ATLASsemi.git

**Success Criteria Met:**
- ✅ Full 4-phase workflow runs end-to-end automatically
- ✅ Production-grade test coverage (77%, core logic 86-99%)
- ✅ Robust error handling and graceful degradation
- ✅ Ready to deploy and use with general LLM tier
- ✅ Foundation ready for incremental additions (RAG, Factory API, On-prem API)

## Constraints

- **Security Tier:** General LLM (awaiting API approval for Confidential/Top Secret tiers)
- **Runtime Mode:** Dev mode for testing, runtime mode available
- **Timeline:** Production v1.0 foundation before adding enhancements
- **Quality Bar:** Production-ready, not just MVP prototype

## State

✅ **v1.0 MVP COMPLETE (2026-01-07)**

- Done:
  - [x] Phase 0-3: All 4 agents implemented
  - [x] WorkflowOrchestrator implementation
  - [x] Comprehensive test suite (25 tests, 77% coverage)
  - [x] CLI integration with orchestrator
  - [x] Deployment documentation (DEPLOYMENT.md)
  - [x] Testing guide (TESTING.md)
  - [x] README updated to v1.0 status
  - [x] All commits pushed to GitHub
  - [x] Technical debt tracking system created
  - [x] Release Planning Workflow established
  - [x] claude-bootstrap evaluation completed

📋 **v1.1 RAG DESIGN & PLANNING COMPLETE (2026-01-08)**

- Done:
  - [x] RAG architecture designed (two scenarios: generic + confidential)
  - [x] Three-tier document taxonomy defined
  - [x] Security tier strategy (OpenAI for Tier 1, local for Tier 2/3)
  - [x] Multi-project support designed
  - [x] Document processing strategy (text + OCR for v1.1)
  - [x] Document organization strategy (folder-based + auto-tagging)
  - [x] Implementation plan created (thoughts/shared/plans/2026-01-08-v1.1-rag-integration.md)
  - [x] Tech choices validated against 2025-2026 best practices (all VALID ✓)
  - [x] Document download utility created (scripts/download_docs.py)
- Next:
  - [ ] User gathers reference documents using download utility
  - [ ] Implement Phase 1: Document Indexer
  - [ ] Implement Phase 2: Query Engine
  - [ ] Implement Phase 3: Analysis Agent Integration
  - [ ] Implement Phase 4: Testing & Documentation

**Current Focus:** Document collection phase (user gathering PDFs/HTML)

📋 **v1.2 DATABASE PIPELINE DEBUGGING PLAN COMPLETE (2026-01-08)**

- Done:
  - [x] Technical research completed (SQL Server DMVs, Power BI API, embeddings, graph DBs)
  - [x] Implementation plan created (thoughts/shared/plans/2026-01-08-v1.2-database-pipeline-debugging.md)
  - [x] Tech choices validated against 2024-2025 best practices (all VALID ✓)
  - [x] 6-phase implementation approach defined (25-35 hours total)
- Next (for new data scientist):
  - [ ] Phase 1: SQL Server Metadata Extraction
  - [ ] Phase 2: Power BI Lineage Extraction
  - [ ] Phase 3: Code Embedding & Semantic Search
  - [ ] Phase 4: Dependency Graph Construction
  - [ ] Phase 5: Analysis Agent Integration (ProblemMode.DATA_PIPELINE)
  - [ ] Phase 6: Testing with Production Tickets

**Current Focus:** Plan ready for new data scientist onboarding (parallel workstream with v1.1)

## Technical Debt Tracking

**Document:** `TECHNICAL_DEBT.md` (in repo root)

**High Priority (Before v2.0):**
- Increase test coverage from 77% to 90%+
  - Real API integration tests (requires API keys)
  - CLI input mocking tests
  - Edge case coverage
  - **When:** Before v2.0 OR when Factory/On-prem APIs implemented
  - **Tracked in:** `.github/ISSUE_TEMPLATE/increase-test-coverage.md`

**Future Work:**
- v1.1: RAG integration (semiconductor reference docs)
- v1.2: Factory API integration (Tier 2)
- v1.3: On-prem API integration (Tier 3)
- Later: Knowledge graph, historical database

## Planning Future Releases

**For v2.0 or any major release:**

1. **Copy the template ledger:**
   ```bash
   cp thoughts/ledgers/TEMPLATE-major-release.md \
      thoughts/ledgers/CONTINUITY_CLAUDE-v2.0-release.md
   ```

2. **The template enforces:**
   - Following Release Planning Workflow
   - MANDATORY technical debt review (Step 2)
   - Systematic scope definition
   - No skipping debt items

3. **Workflow document:** `thoughts/workflows/RELEASE_PLANNING.md`
   - 8-step process
   - Technical debt review is Step 2 (mandatory)
   - Creates release plan
   - Tracks debt resolution

This ensures every major release systematically reviews and addresses triggered technical debt before proceeding.

## Key Decisions

1. **Decision:** Production v1.0 foundation before enhancements
   - **Rationale:** Need solid, tested base to build on; incremental additions minimize risk
   - **Impact:** Can deploy and use now, then add RAG/APIs without breaking existing functionality

2. **Decision:** RAG with semiconductor reference docs (not historical troubleshooting)
   - **Rationale:** Reference docs (manuals, SOPs, standards) are available; gathering troubleshooting history takes too long
   - **Impact:** Practical near-term enhancement that adds real value

3. **Decision:** Factory + On-prem APIs next priority after MVP
   - **Rationale:** Awaiting approval from teams that own those APIs
   - **Impact:** Architecture already supports it (just need implementations)

4. **Decision:** Full workflow orchestration (no partial workflows for MVP)
   - **Rationale:** Keeps implementation simple and focused
   - **Impact:** Always runs Phases 0→1→2→3 in order

5. **Decision:** Batch clarification Q&A (all questions at once)
   - **Rationale:** Better UX than one-at-a-time; users can see full question set
   - **Impact:** Simpler orchestrator logic, faster workflow

6. **Decision:** No session persistence for MVP
   - **Rationale:** Full workflow runs in one session; complexity not justified
   - **Impact:** Keep it simple; can add later if needed

7. **Decision:** Production-grade testing (not just 80% coverage target)
   - **Rationale:** This is v1.0 that will be deployed and enhanced
   - **Impact:** Higher confidence, catches regressions, enables safe additions

8. **Decision:** Technical debt tracking with workflow enforcement
   - **Rationale:** Systematic review prevents forgotten work at major releases
   - **Impact:** Template ledger + Release Planning Workflow forces Step 2 debt review
   - **Files:** TECHNICAL_DEBT.md, thoughts/workflows/RELEASE_PLANNING.md, TEMPLATE-major-release.md

9. **Decision:** Skip claude-bootstrap integration for now
   - **Rationale:** Solo project, small codebase (698 lines), marginal benefit vs overhead
   - **Impact:** Reassess at v2.0 if team grows or codebase exceeds 2000 lines
   - **Analysis:** thoughts/analysis/claude-bootstrap-vs-continuous-claude.md

## v1.1 RAG Design Decisions

10. **Decision:** Two RAG scenarios with different security models
    - **Scenario 1 (Generic):** Always-on public docs (manuals, standards), Tier 1, OpenAI embeddings
    - **Scenario 2 (Confidential):** Temporary problem-specific docs, Tier 2/3, local embeddings, auto-delete
    - **Rationale:** Public docs safe for cloud, confidential must stay on-prem
    - **Impact:** Hybrid embedding strategy, separate collections by tier

11. **Decision:** Three-tier document taxonomy (not domain-based collections)
    - **Tier 1 - Domain-Specific:** WHAT (yield, operations, organizational) - `applicability="specific"`
    - **Tier 2 - Universal Methodologies:** HOW (8D, DMAIC, 5 Whys) - `applicability="universal"`, `applies_to_domains=["all"]`
    - **Tier 3 - Cross-Cutting Support:** Supporting skills (statistics, communication) - `applicability="cross_domain"`
    - **Rationale:** 8D/problem-solving are universal, not domain-specific; single collection enables cross-domain queries
    - **Impact:** Query strategy: Always include Tier 2+3, dynamically select Tier 1 by problem mode
    - **Key Insight:** User observation: "8D applies to yield, operations, organizational - it's a bigger process"

12. **Decision:** Text extraction + OCR only for v1.1 (defer vision processing)
    - **Rationale:** Academic docs describe figures well, OCR captures 90-95% value, vision adds 4-6 hours for ~5% gain
    - **Impact:** Faster v1.1 delivery, defer LLaVA/GPT-4V to v1.2 when building Tier 2/3 RAG
    - **Tools:** PyMuPDF (PDF), python-pptx (PowerPoint), Tesseract (OCR)

13. **Decision:** Folder-based organization with automated content tagging
    - **Structure:** `reference_docs/{methodologies,yield,operations,support}/`
    - **Indexing:** Folder provides initial hint, content analysis refines tags, user can override with .meta.yaml
    - **Rationale:** Low friction (natural org), automatic refinement, flexible overrides
    - **Impact:** Easy document addition (drop in folder + reindex), discoverable without manual tagging

14. **Decision:** Plan-driven approach for v1.1 (not TDD)
    - **Rationale:** RAG is exploratory (chunk size, relevance tuning), needs manual quality evaluation
    - **Impact:** Follow same pattern that worked for orchestrator v1.0, include subjective quality checklists

15. **Decision:** Swap v1.2 to Database Pipeline Debugging (move Vision+Confidential to v1.3)
    - **Rationale:** New data scientist joining, can work in parallel; user is in production org, boss wants faster ticket closure
    - **Business value:** Close data tickets 5-10x faster (hours instead of days)
    - **Workstream strategy:** User does v1.1 (document RAG), data scientist does v1.2 (database pipeline) - independent, no conflicts
    - **Strategic alignment:** Production organization priority
    - **Impact:** Parallel development, faster overall delivery, immediate business value

## Open Questions

- None currently - all v1.1 design questions resolved
- v1.2 will need separate implementation plan for new data scientist

## Working Set

**Files Implemented (Phase 3):**
- `src/atlassemi/agents/prevention_agent.py` - Complete D5/D7/D8 implementation (215 lines)
- `src/atlassemi/agents/__init__.py` - Updated with PreventionAgent export
- `cli.py` - Integrated Phase 3 into workflow
- `DEVELOPMENT_STATUS.md` - Marked Phase 3 complete
- `CLAUDE.md` - Updated agent list
- `.claude/settings.json` - Simplified permissions
- `thoughts/shared/plans/2026-01-07-prevention-agent-phase3.md` - Implementation plan (16KB)
- `thoughts/shared/handoffs/validation-prevention-agent-phase3.md` - Validation handoff

**Commits:**
- `7d5d07f` - Add Prevention Agent implementation plan and validation
- `9677e2d` - Implement Prevention Agent (Phase 3) with D5/D7/D8 support

**Branch:** `main`
**Remote:** https://github.com/chemnteach/ATLASsemi.git

**Next Files to Create:**
- `src/atlassemi/orchestrator/__init__.py` - Package init
- `src/atlassemi/orchestrator/workflow.py` - Workflow orchestrator
- `tests/test_narrative_agent.py` - Unit tests for Phase 0
- `tests/test_clarification_agent.py` - Unit tests for Phase 1
- `tests/test_analysis_agent.py` - Unit tests for Phase 2
- `tests/test_prevention_agent.py` - Unit tests for Phase 3
- `tests/test_orchestrator.py` - Integration tests
- `tests/test_model_router.py` - Model router tests
- `tests/test_tier_enforcer.py` - Security tier tests

**Key Commands:**
```bash
# Run CLI (current - Phase 0 + 3 only)
python cli.py

# Run tests (after implementation)
pytest tests/ -v --cov=atlassemi --cov-report=html

# Format
black . && isort . && flake8 .

# Type check
mypy src/atlassemi/
```

## Progress Notes

### 2026-01-07 Afternoon Session

**Started:** User asked to validate and implement Prevention Agent plan

**Plan Validation (14:30):**
- Validated all 7 tech choices against 2024-2025 best practices
- All choices confirmed VALID (JSON outputs, template pattern, error handling, etc.)
- Optional enhancement identified: Anthropic's native Structured Outputs (Nov 2024 feature)
- Created validation handoff: `thoughts/shared/handoffs/validation-prevention-agent-phase3.md`

**Implementation (15:00-17:00):**
- Created `prevention_agent.py` with full D5/D7/D8 support
- Mode-aware prompts (excursion/improvement/operations)
- JSON-structured output with fallback error handling
- 4000 token budget for comprehensive prevention planning
- Updated agent exports and CLI integration
- Updated documentation (DEVELOPMENT_STATUS.md, CLAUDE.md)

**Testing (17:00-18:00):**
- Test 1: Mock LLM execution - PASSED
- Test 2: JSON parsing (valid + malformed) - PASSED
- Test 3: Mode-specific behavior - PASSED
- Verified all 8 success indicators - 7/8 PASSED (skipped real API test)

**Git Workflow (18:30):**
- Created 2 commits (plan/validation + implementation)
- Set up GitHub remote: https://github.com/chemnteach/ATLASsemi.git
- Cleared cached credentials (craig-synterra → chemnteach)
- Successfully pushed to GitHub

**Planning Next Phase (19:00):**
- User defined realistic roadmap:
  - Near-term: Factory API + On-prem API (pending approval)
  - Near-term: RAG with semiconductor reference docs (NOT troubleshooting history)
  - Later: Historical troubleshooting database, knowledge graph
- Agreed on production v1.0 approach:
  - Orchestrator + comprehensive tests = deployable foundation
  - Then incrementally add RAG, APIs
- User confirmed design decisions for orchestrator

**Completed (19:30-22:30):**
- Created Orchestrator + Test Suite implementation plan (detailed 6-phase plan)
- Validated tech choices against best practices
- Implemented all 6 phases (orchestrator + comprehensive tests)
- Integrated with CLI, created deployment docs
- Made 3 commits for v1.0 completion
- v1.0 COMPLETE ✅

### 2026-01-08 Post-v1.0 Session

**Started:** Continued from context compaction at v1.0 completion

**Technical Debt System (00:00-01:00):**
- User asked: "How do we remember to address test coverage before v2.0?"
- Created TECHNICAL_DEBT.md with trigger conditions
- Created Release Planning Workflow (8-step systematic process)
- Created TEMPLATE-major-release.md with workflow enforcement
- Key mechanism: Template ledger YAML references workflow → forces Step 2 debt review
- Created GitHub issue template for coverage work
- Made 2 commits for debt tracking system

**claude-bootstrap Evaluation (01:30-02:30):**
- User asked about claude-bootstrap integration
- Fetched and analyzed README (TDD-first, team coordination, quality constraints)
- Created comparative analysis document
- Recommendation: Skip integration (marginal benefit for solo project, 698 lines)
- Triggers to reassess: Team >1, codebase >2000 lines, duplication issues
- Made 1 commit for analysis

**v1.1 RAG Design (02:30-00:45):**
- User wants RAG with semiconductor reference docs
- **Two scenarios defined:**
  1. Generic knowledge base (Tier 1, always-on, public docs)
  2. Problem-specific confidential (Tier 2/3, temporary, IP protected)

- **Key architectural decisions:**
  - Hybrid embeddings: OpenAI for Tier 1, local for Tier 2/3
  - Multi-project support with lifecycle management
  - Three-tier taxonomy (domain/methodology/support)
  - Single collection with metadata tags (not separate collections)
  - Folder-based organization with automated content tagging

- **User's critical insight:**
  - "8D is a bigger process - applies to yield, operations, organizational, etc."
  - Led to recognizing methodologies as universal (Tier 2), not domain-specific
  - Query strategy: Always include Tier 2+3, dynamically select Tier 1 by mode

- **Document processing decisions:**
  - Text + OCR only for v1.1 (PyMuPDF, python-pptx, Tesseract)
  - Defer vision (LLaVA/GPT-4V) to v1.2 (internal docs benefit more)
  - Academic docs describe figures well enough for 90-95% value

- **Implementation approach:**
  - Plan-driven (NOT TDD) - same pattern that worked for orchestrator
  - Manual quality evaluation needed (subjective relevance assessment)

**Current Status (00:45):**
- All v1.1 RAG design questions resolved
- Document organization strategy defined (folder-based + auto-tagging)
- Ready to create v1.1 implementation plan
- Ledger updated with all design decisions

## Cost Tracking

**Session Cost:** ~$0.15 (validation research via WebSearch)

**Phase 3 Testing:**
- All tests used mock LLM (no API costs)

**Future Cost Estimates:**
- Full workflow (Phases 0-3) in dev mode: ~$0.08-0.12 per problem
- Full workflow in runtime mode: ~$0.40-1.00 per problem

## Security Notes

**Current Tier:** General LLM (Tier 1)
- All external APIs allowed
- No proprietary fab data involved
- Public knowledge only

**API Integration Status:**
- ✅ Anthropic: Implemented and working
- ✅ OpenAI: Implemented (placeholder client)
- 🚧 Factory API: Awaiting approval and endpoint details
- 🚧 On-prem API: Awaiting approval and endpoint details

**Next Session Considerations:**
- Still using General LLM tier for MVP
- When Factory/On-prem APIs approved, will implement clients
- RAG will stay at General tier initially (reference docs are public)

## Technical Notes

### Prevention Agent Architecture
- **Prompt Structure:** Mode-specific guidance + 8D context + JSON schema
- **Output Handling:** Try/except JSON parse with graceful fallback
- **8D Mapping:** D5 (permanent actions), D7 (systemic prevention), D8 (lessons learned)
- **Token Budget:** 4000 tokens (moderate complexity)

### Current Workflow (Partial)
- CLI runs Phase 0 (Narrative) → Phase 3 (Prevention)
- Phases 1-2 implemented but not orchestrated yet
- Context passing incomplete (Prevention Agent gets minimal context)

### Orchestrator Requirements (Next)
- Chain all 4 phases: Narrative → Clarification → Analysis → Prevention
- Collect user answers for clarification questions
- Pass rich context between phases:
  - Phase 1 gets narrative analysis from Phase 0
  - Phase 2 gets narrative + clarification answers
  - Phase 3 gets full 8D analysis from Phase 2
- Accumulate costs across all phases
- Error handling and recovery at each phase

### Test Suite Requirements (Next)
- **Unit Tests:** Each agent independently (mock LLM responses)
- **Integration Tests:** Full workflow with all agents
- **Edge Cases:** Empty inputs, malformed JSON, missing data
- **Error Handling:** Network failures, API errors, invalid tier
- **Cost Tracking:** Verify cost accumulation
- **Security:** Tier enforcement blocking

## Next Session Priorities

### v1.1 RAG Implementation (Immediate)

1. **Create v1.1 RAG Implementation Plan** (next task)
   - Detailed plan using plan-driven approach (not TDD)
   - 4-5 phases: Indexer, Query Engine, Integration, Testing, Documentation
   - Include manual quality evaluation checklists
   - Validate tech choices (ChromaDB, sentence-transformers, Tesseract, etc.)

2. **Implement Phase 1: Document Indexer** (~4-6 hours)
   - `src/atlassemi/knowledge/indexer.py`
   - Text extraction (PyMuPDF, python-pptx, python-docx)
   - OCR for images (Tesseract)
   - Folder-based + content-based tagging
   - ChromaDB storage with metadata

3. **Implement Phase 2: Query Interface** (~3-4 hours)
   - `src/atlassemi/knowledge/query_engine.py`
   - Semantic search with ChromaDB
   - Three-tier filtering strategy
   - Mode-aware boosting
   - Top-k retrieval

4. **Implement Phase 3: Integration** (~2-3 hours)
   - Modify Analysis Agent to accept RAG context
   - Query RAG before analysis
   - Inject relevant chunks into prompt
   - Test enriched analysis quality

5. **Phase 4: Testing and Documentation** (~3-4 hours)
   - Unit tests for indexer and query engine
   - Integration tests with Analysis Agent
   - Manual quality evaluation (is retrieval relevant?)
   - Document indexing workflow and usage

### Parallel Workstream (New Data Scientist - v1.2)

When new data scientist is ready:

1. **Create v1.2 Database Pipeline Implementation Plan** (for her)
   - SQL Server metadata extraction architecture
   - Power BI REST API integration
   - Graph structure design (dependencies)
   - Code embedding strategy (SQL chunking)
   - Integration with Analysis Agent (new mode)
   - Testing with real production tickets

2. **Separate ledger for v1.2 work:**
   - `thoughts/ledgers/CONTINUITY_CLAUDE-atlassemi-v1.2-pipeline.md`
   - Independent state tracking
   - No conflicts with v1.1 work

### Future (After v1.1 + v1.2)

- v1.3: Vision processing (LLaVA local, GPT-4V cloud)
- v1.3: Confidential RAG (Tier 2/3 with project lifecycle)
- v2.0: Increase test coverage to 90%+ (triggered by Release Planning Workflow)
- v2.0+: Factory API, On-prem API integration

## Repository Health

**Status:** ✅ v1.0 Production-Ready, v1.1 Design Complete

**Code Quality:**
- All code formatted (black, isort)
- Type hints present
- Docstrings complete
- No linting errors
- Comprehensive inline documentation

**Documentation:**
- ✅ DEPLOYMENT.md (installation, configuration, testing)
- ✅ TESTING.md (automated + manual test procedures)
- ✅ TECHNICAL_DEBT.md (tracking deferred work)
- ✅ Release Planning Workflow (systematic debt review)
- ✅ v1.1 RAG design documented in ledger
- ✅ claude-bootstrap evaluation completed

**Git History:**
- 15 commits total (clean progression from Phase 0 → v1.0 complete)
- Commits cover: agents, orchestrator, tests, docs, debt tracking, analysis
- Detailed commit messages with reasoning
- No sensitive data committed
- Pushed to GitHub successfully

**Test Coverage:**
- 25 automated tests, all passing
- 77% overall coverage (86-99% for core logic)
- Manual testing procedures documented
- Debt tracked for 90%+ coverage (triggered before v2.0)

## v1.1 RAG System Design

### Architecture Overview

**Two Scenarios:**

1. **Generic Knowledge Base (Tier 1 - Always-on)**
   - Public semiconductor reference documents
   - Equipment manuals, SOPs, industry standards, failure mode catalogs
   - Security: OpenAI embeddings (cloud safe for public docs)
   - Lifecycle: Permanent, single collection
   - Use: Enriches all analyses automatically

2. **Problem-Specific Confidential (Tier 2/3 - Temporary)**
   - Uploaded for specific task force investigations
   - Contains proprietary fab data, tool recipes, internal docs
   - Security: Local embeddings (sentence-transformers), no cloud
   - Lifecycle: active → archived → auto-deleted after investigation
   - Use: Manual query during confidential problem analysis

### Three-Tier Document Taxonomy

**Tier 1: Domain-Specific Knowledge (WHAT you're solving)**
- Examples: Defect atlas (yield), Factory Physics (operations), HR retention guide (organizational)
- Tags: `type="domain_knowledge"`, `domain="yield/operations/organizational"`, `applicability="specific"`

**Tier 2: Universal Methodologies (HOW to solve)**
- Examples: 8D handbook, DMAIC guide, 5 Whys toolkit, Root Cause Analysis methods
- Tags: `type="methodology"`, `methodology_name="8d/dmaic/5whys"`, `applies_to_domains=["all"]`, `applicability="universal"`
- **Key:** Always included in queries regardless of problem domain

**Tier 3: Cross-Cutting Support (Supporting skills)**
- Examples: Statistics textbook, data visualization, communication, project management
- Tags: `type="supporting_knowledge"`, `knowledge_area="statistics/communication"`, `applicability="cross_domain"`
- **Key:** Included for relevant problems, applies broadly but not universally

### Metadata Schema

```python
{
    # Primary classification
    "type": "domain_knowledge" | "methodology" | "supporting_knowledge",
    "applicability": "specific" | "universal" | "cross_domain",

    # For domain knowledge (Tier 1)
    "domain": "yield" | "operations" | "organizational" | "equipment",
    "subdomain": str,
    "topics": List[str],

    # For methodologies (Tier 2)
    "methodology_name": "8d" | "dmaic" | "5_whys" | "fishbone",
    "applies_to_domains": ["all"],
    "applies_to_modes": ["excursion", "improvement", "operations"],

    # For supporting knowledge (Tier 3)
    "knowledge_area": "statistics" | "communication" | "project_management",

    # Project management (Tier 2/3 confidential only)
    "project_id": str,
    "project": str,
    "status": "active" | "archived",
    "auto_delete_date": str,  # ISO format

    # Source tracking
    "source": str,
    "page": int,
    "chapter": str
}
```

### Query Strategy

**Query behavior:**
1. **Always include:** Tier 2 (methodologies) - universal applicability
2. **Always include:** Tier 3 (supporting knowledge) - broad applicability
3. **Dynamically select:** Tier 1 based on problem mode
   - EXCURSION mode → prioritize `domain="yield"`
   - OPERATIONS mode → prioritize `domain="operations"`
   - IMPROVEMENT mode → balanced, include both

**Example query for yield problem:**
```python
results = rag_query(
    query="Cpk degradation on Chamber B",
    filters={
        # Tier 1: Domain-specific (yield focus)
        "OR": [
            {"type": "domain_knowledge", "domain": "yield"},
            {"type": "domain_knowledge", "domain": "equipment"}
        ],
        # Tier 2: Always included (methodologies)
        {"type": "methodology"},
        # Tier 3: Always included (support)
        {"type": "supporting_knowledge"}
    },
    top_k=10
)
```

### Document Organization

**Source folder structure:**
```
reference_docs/
├── methodologies/           # Tier 2: Universal
│   ├── 8d_handbook.pdf
│   ├── dmaic_guide.pdf
│   └── root_cause_analysis.pdf
├── yield/                   # Tier 1: Domain-specific
│   ├── defect_atlas.pdf
│   ├── spc_handbook.pdf
│   └── excursion_response.pdf
├── operations/              # Tier 1: Domain-specific
│   ├── factory_physics.pdf
│   └── cycle_time_optimization.pdf
├── organizational/          # Tier 1: Domain-specific
│   └── retention_strategies.pdf
└── support/                 # Tier 3: Cross-cutting
    ├── statistics_textbook.pdf
    └── data_visualization_guide.pdf
```

**Indexing workflow:**
1. User organizes documents in folders (one-time)
2. Run indexer: `python -m atlassemi.knowledge.indexer --source-dir reference_docs/ --collection tier1_generic`
3. Indexer uses folder as hint, analyzes content, assigns tags
4. User can override with `.meta.yaml` files if needed

**Automatic tagging:**
- Folder location provides initial type hint
- Content analysis detects keywords (8D, Cpk, cycle time, etc.)
- Assigns appropriate tier, domain, topics
- Stores in ChromaDB with metadata

### Document Processing (v1.1)

**Supported formats:**
- PDF: PyMuPDF (text extraction)
- PowerPoint: python-pptx (text + OCR on embedded images)
- Word: python-docx (text extraction)
- Images in documents: Tesseract OCR (local, no cloud)

**Deferred to v1.2:**
- Vision processing (LLaVA local, GPT-4V cloud)
- Image understanding for internal diagrams
- Confidential RAG (Tier 2/3 with project lifecycle)

### Integration with Analysis Agent

**Enrichment flow:**
1. Analysis Agent receives 8D-mapped problem
2. Query RAG with problem keywords + mode-aware filters
3. Retrieve top 10 relevant chunks
4. Inject into Analysis Agent prompt context
5. Agent synthesizes LLM knowledge + RAG context
6. Returns enriched 8D analysis

## Realistic Product Roadmap

### v1.0 - MVP Foundation ✅ COMPLETE (2026-01-07)
**Goal:** Production-ready CLI tool with all 4 phases working
- ✅ All 4 agents implemented (Phases 0-3)
- ✅ WorkflowOrchestrator to chain agents
- ✅ Comprehensive test suite (25 tests, 77% coverage)
- ✅ Deployment documentation (DEPLOYMENT.md, TESTING.md)
- ✅ Technical debt tracking system
- ✅ Release Planning Workflow
- **Status:** Deployed and ready to use
- **Use Case:** Engineers can use it for 8D analysis with general LLM

### v1.1 - RAG Integration ✅ PLAN VALIDATED (2026-01-08)
**Goal:** Augment analysis with semiconductor reference documents
- ✅ Architecture designed (two scenarios: generic + confidential)
- ✅ Three-tier taxonomy defined
- ✅ Document organization strategy (folder-based + auto-tagging)
- ✅ Implementation plan created (4 phases, 12-17 hours)
- ✅ Tech choices validated against 2025-2026 best practices
- 📋 Phase 1: Document Indexer (PDF, PowerPoint, Word + OCR)
- 📋 Phase 2: Query Engine (semantic search, mode-aware filtering)
- 📋 Phase 3: Analysis Agent Integration
- 📋 Phase 4: Testing & Documentation
- **Timeline:** Ready for implementation
- **Use Case:** Analysis enriched with reference material, not just LLM knowledge
- **Tech Stack:** pymupdf4llm, python-pptx, python-docx, ChromaDB, OpenAI embeddings

### v1.2 - Database Pipeline Debugging 📋 PARALLEL WORKSTREAM
**Goal:** Trace Power BI reports to SQL source, debug data issues
- **Owner:** New data scientist (parallel with v1.1)
- **Business Value:** Close production data tickets 5-10x faster
- 📋 SQL Server metadata extraction (schemas, stored procs, dependencies)
- 📋 Power BI lineage tracing (reports → datasets → queries)
- 📋 Stored procedure code embedding and semantic search
- 📋 Graph-based dependency tracing (Neo4j or structured metadata)
- 📋 Integration with Analysis Agent (new `ProblemMode.DATA_PIPELINE`)
- 📋 Testing with real production tickets
- **Tech Stack:** SQL Server system tables, Power BI REST API, ChromaDB (vectors), graph structure
- **Timeline:** Parallel development while v1.1 in progress
- **Use Case:** "Yield Dashboard shows wrong Chamber B data" → trace pipeline → find JOIN mismatch
- **Strategic:** Makes boss happy (production org ticket velocity)

### v1.3 - Vision + Confidential RAG
**Goal:** Vision processing + Tier 2/3 document handling
- 📋 Vision processing (LLaVA local, GPT-4V cloud)
- 📋 Image understanding for internal diagrams
- 📋 Confidential RAG (Tier 2/3 with project lifecycle)
- 📋 Factory API integration (Tier 2)
- 📋 On-prem API integration (Tier 3)
- **Timeline:** After v1.1 and v1.2 stable
- **Use Case:** Analyze proprietary fab documents with complex diagrams

### Future (when feasible)
- 📋 Historical troubleshooting database (requires gathering effort)
- 📋 Knowledge graph (tools, processes, materials, failure modes)
- 📋 Web interface (Flask/FastAPI + React)

---

**Session Status:** v1.0 COMPLETE ✅ | v1.1 Plan Validated ✅ | Ready for Phase 1 Implementation
**Last Updated:** 2026-01-08 01:30
**Next Action:** Implement Phase 1 (Document Indexer) or take break and resume later

**Files Created This Session:**
- thoughts/shared/plans/2026-01-08-v1.1-rag-integration.md (Comprehensive 4-phase plan)
- thoughts/handoffs/validation-v1.1-rag-integration.md (Tech validation - all VALID ✓)
