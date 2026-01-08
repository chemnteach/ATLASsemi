# ATLASsemi Technical Debt

This document tracks known technical debt, future improvements, and deferred work.

**Last Updated:** 2026-01-07

---

## High Priority (Before v2.0)

### 1. Increase Test Coverage from 77% to 90%+

**Current State:** 77% coverage (161 of 698 lines untested)

**What's Missing:**
1. **Real API Integration Tests** (53 lines in model_router.py, 53 lines in base.py)
   - Anthropic API actual calls
   - OpenAI API actual calls
   - Factory API calls (Tier 2)
   - On-prem API calls (Tier 3)

2. **Interactive CLI Input Tests** (33 lines in workflow.py)
   - `_default_answer_collector()` method
   - User input() mocking
   - Clarification Q&A flow

3. **Edge Case Coverage** (14 lines in tier_enforcer.py)
   - Additional tool validation scenarios
   - Error injection tests

**Why Deferred:**
- Real API tests require valid API keys (expensive, slow, non-deterministic)
- CLI input tests need complex mocking infrastructure
- Core business logic has excellent coverage (86-99%)
- Manual testing covers these paths (see docs/TESTING.md)

**When to Address:**
- **Trigger:** Before v2.0 release OR when Factory/On-prem APIs are implemented
- **Timeline:** 1-2 days of work
- **Dependencies:**
  - Factory API access (for Tier 2 tests)
  - On-prem API access (for Tier 3 tests)

**How to Implement:**
```bash
# Step 1: Add real API integration tests (separate test file)
# tests/test_api_integration.py
# - Requires ANTHROPIC_API_KEY
# - Runs only when env var set
# - Marked as @pytest.mark.integration

# Step 2: Mock CLI input for answer collector
# Use unittest.mock.patch('builtins.input')
# Test question display and answer collection

# Step 3: Add error injection tests
# Test security violations, malformed responses, network failures

# Expected result: 90%+ coverage
```

**Acceptance Criteria:**
- [ ] Overall coverage >=90%
- [ ] All API clients tested with real endpoints
- [ ] CLI input flow fully tested
- [ ] All error paths covered
- [ ] Tests run in <5 seconds (with mocks) or can be skipped for CI

---

## Medium Priority (v2.x Features)

### 2. Knowledge Graph Integration

**What:** Graph database connecting tools, processes, materials, failure modes

**Why Deferred:**
- v1.0 focuses on core workflow
- Requires significant data gathering effort
- RAG with reference docs provides 80% of value faster

**When to Address:** v1.4 or later

**Estimated Effort:** 2-3 weeks

---

### 3. Factory API Client (Tier 2)

**What:** Integration with internal factory GenAI API

**Why Deferred:** Awaiting API approval and endpoint details from factory team

**When to Address:** v1.2 (after approval)

**Dependencies:**
- Factory API endpoint URL
- Authentication credentials
- Rate limiting details
- Audit logging requirements

**Estimated Effort:** 3-5 days

---

### 4. On-Prem API Client (Tier 3)

**What:** Integration with air-gapped on-premises LLM

**Why Deferred:** Awaiting API approval from security team

**When to Address:** v1.3 (after approval)

**Dependencies:**
- On-prem API endpoint (air-gapped environment)
- Authentication mechanism
- Security clearance for team members
- Compliance review

**Estimated Effort:** 3-5 days

---

### 5. RAG Integration

**What:** Vector database with semiconductor reference documents

**Why Deferred:**
- v1.0 provides working system without RAG
- Need to gather and prepare documents
- Chromadb/similar tooling ready when needed

**When to Address:** v1.1

**Estimated Effort:** 1-2 weeks

---

## Low Priority (Nice to Have)

### 6. Web Interface

**What:** Flask/FastAPI backend + React frontend

**Why Deferred:** CLI is sufficient for initial users

**When to Address:** User demand drives priority

**Estimated Effort:** 4-6 weeks

---

### 7. Historical Troubleshooting Database

**What:** Queryable database of past excursions and resolutions

**Why Deferred:**
- Requires significant data gathering
- Manual ingestion of historical 8Ds
- Data cleaning and structuring effort

**When to Address:** v2.0 or later

**Estimated Effort:** 3-6 months (mostly data gathering)

---

## Technical Debt from v1.0 Development

### None Currently

All identified issues were resolved during v1.0 development:
- ✅ Safe metadata extraction (defensive programming added)
- ✅ Error handling in all agents
- ✅ Security tier enforcement
- ✅ Cost tracking

---

## How to Use This Document

### When Starting New Work

1. Check this document for related debt
2. Assess if debt should be addressed first
3. Update estimates based on new information

### When Adding Debt

1. Add entry with clear description
2. Explain why deferred (not forgotten!)
3. Set trigger conditions for addressing
4. Estimate effort
5. Update "Last Updated" date

### When Closing Debt

1. Mark item as ✅ complete
2. Move to "Resolved" section with date
3. Link to commit/PR that resolved it

---

## Resolved Technical Debt

### v1.0 Resolution

**Orchestrator Implementation** (Resolved 2026-01-07)
- Was: Individual agent calls in CLI
- Now: WorkflowOrchestrator chains all 4 phases
- Commit: 32d68da

**Test Suite** (Resolved 2026-01-07)
- Was: No automated tests
- Now: 25 tests with 77% coverage
- Commit: 095667d

---

## Contact

For questions about technical debt or to propose new debt items, contact the development team or update this document directly.
