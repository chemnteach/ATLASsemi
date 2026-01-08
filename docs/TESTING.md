# ATLASsemi Testing Guide

## Overview

This document covers automated and manual testing procedures for ATLASsemi v1.0.

**Last Updated:** 2026-01-07

---

## Automated Testing

### Running Tests

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=atlassemi --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Test Coverage (v1.0)

**Overall Coverage:** 77%

**By Module:**
- Narrative Agent: 99%
- Clarification Agent: 86%
- Analysis Agent: 93%
- Prevention Agent: 97%
- Orchestrator: Integration tested
- Model Router: 100%
- Tier Enforcer: 100%

**Test Breakdown:**
- 13 agent unit tests
- 4 orchestrator integration tests
- 4 model router tests
- 4 security tier enforcement tests
- **Total:** 25 tests

### Test Execution Time

Expected: < 5 seconds for full suite (all tests use mocks, no real API calls)

---

## Manual Testing Checklist

### Pre-Deployment Testing

Before deploying to production, verify the following end-to-end scenarios:

#### Test 1: Tier 1 Excursion Mode (Public Knowledge)

**Setup:**
```bash
export ATLASSEMI_RUNTIME_MODE="dev"
export ANTHROPIC_API_KEY="your_key_here"
python cli.py
```

**Test Steps:**
1. **Select Mode:** Choose "1" (Yield Excursion Response)
2. **Select Tier:** Choose "1" (General LLM)
3. **Provide Narrative:**
   ```
   We saw a 15% yield drop on Chamber B after PM yesterday.
   Process is 193nm litho. Wafers from lot ABC123.
   Defect density increased from 0.5 to 2.3 per wafer.
   SPC alert triggered at 10:30 AM.
   ```
4. **Answer Questions:** Answer at least 2-3 clarification questions (or skip)
5. **Review Output:** Verify all sections appear:
   - Phase 0: Narrative analysis with facts/hypotheses
   - Phase 1: Clarification questions presented
   - Phase 2: 8D analysis with D0-D8 phases
   - Phase 3: Prevention plan
   - Cost summary

**Expected Results:**
- ✅ All 4 phases complete
- ✅ Facts identified (e.g., "15% yield drop", "Chamber B", "after PM")
- ✅ Hypotheses generated (e.g., "PM incomplete", "chamber drift")
- ✅ 8D phases addressed (at least D0, D2, D4)
- ✅ Prevention plan generated
- ✅ Total cost displayed
- ✅ No errors or exceptions

---

#### Test 2: Tier 1 Improvement Mode

**Setup:** Same as Test 1

**Test Steps:**
1. **Select Mode:** Choose "2" (Yield Improvement)
2. **Select Tier:** Choose "1" (General LLM)
3. **Provide Narrative:**
   ```
   We have chronic yield variability on Product X.
   Yield ranges from 85-92% week to week.
   Multiple chambers, not localized.
   Want to reduce variability to ±2%.
   ```
4. **Answer Questions:** Complete clarification Q&A
5. **Review Output:** Verify improvement-specific focus

**Expected Results:**
- ✅ Questions focus on chronic patterns, not containment
- ✅ Analysis emphasizes variability reduction
- ✅ Prevention plan includes process control improvements
- ✅ 8D phases emphasize D4-D8 (root cause through prevention)

---

#### Test 3: Tier 1 Operations Mode

**Setup:** Same as Test 1

**Test Steps:**
1. **Select Mode:** Choose "3" (Factory Operations)
2. **Select Tier:** Choose "1" (General LLM)
3. **Provide Narrative:**
   ```
   Chamber 5 keeps going down for PM.
   Impacting WIP flow and cycle time.
   Need to understand root cause of frequent failures.
   ```
4. **Answer Questions:** Complete clarification Q&A
5. **Review Output:** Verify operations-specific focus

**Expected Results:**
- ✅ Questions focus on availability and sustainment
- ✅ Analysis emphasizes containment and prevention
- ✅ 8D phases emphasize D3, D7 (containment and prevention)

---

#### Test 4: Security Tier Enforcement

**Test 4a: Tier 1 Allows External APIs**

```bash
python cli.py
# Select mode 1, tier 1
# Should complete without security errors
```

**Expected:** ✅ Workflow completes successfully

**Test 4b: Tier 2 Blocks External APIs (if configured)**

*Note: Requires factory API setup*

```bash
export ATLASSEMI_RUNTIME_MODE="runtime"
python cli.py
# Select mode 1, tier 2
```

**Expected:**
- ✅ External API calls should be blocked
- ✅ Should use factory API instead (if configured)
- ✅ OR provide clear error if factory API not available

**Test 4c: Tier 3 Blocks All External (if configured)**

*Note: Requires on-prem LLM*

```bash
python cli.py
# Select mode 1, tier 3
```

**Expected:**
- ✅ All external calls blocked
- ✅ Uses on-prem LLM only
- ✅ OR provides clear error if on-prem not available

---

#### Test 5: Error Handling

**Test 5a: Empty Narrative**

```bash
python cli.py
# Select mode and tier
# Press Ctrl+D immediately (empty input)
```

**Expected:**
- ✅ Message: "No narrative provided. Exiting."
- ✅ Graceful exit, no exception

**Test 5b: Invalid Mode Selection**

```bash
python cli.py
# Enter "9" for mode
```

**Expected:**
- ✅ Message: "Invalid mode selection."
- ✅ Graceful exit

**Test 5c: Invalid Tier Selection**

```bash
python cli.py
# Enter valid mode
# Enter "9" for tier
```

**Expected:**
- ✅ Message: "Invalid tier selection."
- ✅ Graceful exit

---

#### Test 6: Cost Tracking

**Setup:**
```bash
export ATLASSEMI_RUNTIME_MODE="dev"
python cli.py
```

**Test Steps:**
1. Run complete workflow (any mode/tier)
2. Check final output for cost summary

**Expected Results:**
- ✅ Cost displayed: $0.05-$0.08 (dev mode)
- ✅ Individual phase costs shown (if verbose)
- ✅ Usage summary includes token counts

---

#### Test 7: Question Skipping

**Test Steps:**
1. Run workflow with any mode/tier
2. When clarification questions appear, type "skip" for each

**Expected Results:**
- ✅ Questions are skipped gracefully
- ✅ Workflow continues to Phase 2
- ✅ Analysis works with limited clarification

---

### Performance Testing

#### Test 8: Response Time

**Test Steps:**
1. Run workflow with typical narrative (100-200 words)
2. Measure total execution time

**Expected Results (Dev Mode):**
- Phase 0: < 5 seconds
- Phase 1: < 3 seconds
- Phase 2: < 8 seconds
- Phase 3: < 5 seconds
- **Total:** < 25 seconds

**Expected Results (Runtime Mode):**
- Total: < 40 seconds (larger models, more thorough analysis)

---

### Regression Testing

After any code changes, run:

```bash
# Full test suite
pytest -v

# Verify all 25 tests pass
# Expected: 25 passed in < 5s

# Check coverage hasn't decreased
pytest --cov=atlassemi --cov-report=term-missing

# Expected: >=77% coverage
```

---

## Test Data

### Sample Narratives

**Excursion:**
```
Yield excursion on Product ABC after recipe update.
Chamber 3, Layer 5 lithography.
Defect type: particles.
Started 2 days ago, impacting 200 wafers.
```

**Improvement:**
```
Want to reduce process variability on etch step.
Current Cpk is 1.2, target is 1.5.
Multiple chambers, random pattern.
Need systematic improvement approach.
```

**Operations:**
```
Chamber downtime events increasing.
5 PM events in last 2 weeks vs typical 1-2 per month.
Impacting fab throughput targets.
Need to identify and fix root cause.
```

---

## Known Limitations (v1.0)

### Current Scope
- Tier 1 (General LLM) fully functional
- Tier 2/3 require additional API configuration
- Mock LLM responses for testing (no real API calls)

### Not Yet Implemented
- Knowledge graph integration
- Historical 8D RAG lookup
- Web interface
- Factory API connectors

---

## Troubleshooting Tests

### Issue: Tests Fail with Import Error

**Cause:** Python path not set correctly

**Solution:**
```bash
# Verify conftest.py exists
ls tests/conftest.py

# Run from project root
cd ATLASsemi
pytest
```

### Issue: Coverage Report Missing

**Cause:** pytest-cov not installed

**Solution:**
```bash
pip install pytest-cov
pytest --cov=atlassemi
```

### Issue: CLI Hangs on Input

**Cause:** Waiting for narrative input

**Solution:**
- Type narrative, then press `Ctrl+D` (Unix) or `Ctrl+Z` (Windows)
- Or create test script with piped input

---

## Continuous Testing

### Pre-Commit Checks

Before committing code:

```bash
# 1. Linting
black . && isort . && flake8 .

# 2. Type checking
mypy src/atlassemi/

# 3. Tests
pytest -v

# 4. Coverage check
pytest --cov=atlassemi --cov-report=term-missing

# All should pass before commit
```

### CI/CD Integration (Future)

Recommended pipeline:

```yaml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=atlassemi
      - name: Check coverage
        run: pytest --cov=atlassemi --cov-fail-under=77
```

---

## Test Maintenance

### Adding New Tests

When adding new features:

1. **Write test first** (TDD approach)
2. **Mock LLM responses** (use `model_router=None`)
3. **Test edge cases** (empty input, malformed data)
4. **Verify coverage** stays >=77%

Example:

```python
def test_new_feature():
    """Test new feature with mock LLM."""
    agent = NewAgent(model_router=None)

    # Mock response
    agent._call_llm = lambda **kwargs: '{"result": "test"}'

    output = agent.execute(test_input)
    assert output.some_field == expected_value
```

### Updating Tests

When changing agent prompts or logic:

1. Update corresponding test
2. Verify mock responses match new format
3. Run full test suite
4. Check coverage report

---

## Appendix: Quick Reference

### Run Commands

```bash
# All tests
pytest

# Verbose
pytest -v

# Coverage
pytest --cov=atlassemi --cov-report=html

# Specific module
pytest tests/test_narrative_agent.py

# Specific test
pytest tests/test_narrative_agent.py::test_narrative_agent_execution

# Stop on first failure
pytest -x

# Show print statements
pytest -s
```

### Expected Test Counts

- Total: 25 tests
- Agent tests: 13
- Integration tests: 4
- Router tests: 4
- Security tests: 4

### Coverage Thresholds

- Overall: >=77%
- Agents: >=85%
- Critical modules: >=90%

---

**End of Testing Guide**
