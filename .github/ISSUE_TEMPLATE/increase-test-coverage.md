---
name: Increase Test Coverage to 90%
about: Track progress on increasing test coverage from 77% to 90%+
title: '[TECHNICAL DEBT] Increase test coverage to 90%+'
labels: testing, technical-debt, v2.0
assignees: ''
---

## Overview

Increase test coverage from current 77% to 90%+ before v2.0 release.

## Current Coverage (v1.0)

- **Overall:** 77% (161 of 698 lines untested)
- **Narrative Agent:** 99% ✅
- **Clarification Agent:** 89% ✅
- **Analysis Agent:** 95% ✅
- **Prevention Agent:** 98% ✅
- **Model Router:** 53% ⚠️
- **Base Agent:** 53% ⚠️
- **Orchestrator:** 74% ⚠️
- **Tier Enforcer:** 79% ⚠️

## What's Missing

### 1. Real API Integration Tests (~106 lines)

**Location:** `src/atlassemi/config/model_router.py` (53 lines) + `src/atlassemi/agents/base.py` (53 lines)

**What:** Tests that make actual API calls to:
- Anthropic API
- OpenAI API
- Factory API (Tier 2)
- On-prem API (Tier 3)

**Why Not Tested:**
- Requires valid API keys
- Makes expensive API calls
- Slow and non-deterministic
- v1.0 uses mocks for fast, reliable testing

**How to Add:**
```python
# tests/test_api_integration.py

import pytest
import os

@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="Requires real API key"
)
@pytest.mark.integration
def test_anthropic_real_api():
    """Test actual Anthropic API call."""
    router = ModelRouter(mode=RuntimeMode.DEV)
    # Make real API call
    # Verify response
```

### 2. Interactive CLI Input Tests (~33 lines)

**Location:** `src/atlassemi/orchestrator/workflow.py` lines 256-306

**What:** The `_default_answer_collector()` method that uses `input()` for CLI

**Why Not Tested:**
- Requires mocking user input
- Complex test setup
- Better tested manually

**How to Add:**
```python
# tests/test_orchestrator.py

from unittest.mock import patch

def test_answer_collector_with_mocked_input():
    """Test CLI answer collection."""
    questions = [{"question": "Q1?", "rationale": "R1"}]

    with patch('builtins.input', side_effect=["Answer 1"]):
        orchestrator = WorkflowOrchestrator(None)
        answers = orchestrator._default_answer_collector(questions)

    assert answers == {"Q1?": "Answer 1"}
```

### 3. Edge Case & Error Injection Tests (~14 lines)

**Location:** `src/atlassemi/security/tier_enforcer.py`

**What:** Additional tool validation scenarios, error paths

**How to Add:**
- Test unknown tool names
- Test malformed tool patterns
- Test tier boundary edge cases

## Implementation Plan

### Phase 1: Mock-Based Tests (No API Keys Required)
- [ ] Add CLI input mocking tests
- [ ] Add edge case tests for tier enforcer
- [ ] Add error injection tests
- **Expected Coverage:** 82-85%

### Phase 2: Real API Integration Tests (Requires API Keys)
- [ ] Add Anthropic API integration test
- [ ] Add OpenAI API integration test
- [ ] Mark as `@pytest.mark.integration`
- [ ] Document in README how to run integration tests
- **Expected Coverage:** 88-90%

### Phase 3: Factory & On-Prem Tests (Requires Access)
- [ ] Add Factory API integration test (when available)
- [ ] Add On-prem API integration test (when available)
- **Expected Coverage:** 92-95%

## Acceptance Criteria

- [ ] Overall coverage >=90%
- [ ] All public API methods tested
- [ ] All error paths covered
- [ ] Integration tests documented
- [ ] CI runs unit tests (<5 seconds)
- [ ] Integration tests are optional (require env vars)

## Timeline

**Trigger:** Before v2.0 release OR when Factory/On-prem APIs implemented

**Estimated Effort:** 1-2 days

**Dependencies:**
- Factory API access (optional, for Tier 2 tests)
- On-prem API access (optional, for Tier 3 tests)

## References

- **Technical Debt Doc:** `TECHNICAL_DEBT.md`
- **Testing Guide:** `docs/TESTING.md`
- **Coverage Report:** Run `pytest --cov=atlassemi --cov-report=html`

## Notes

The 77% coverage in v1.0 is intentional and acceptable because:
- Core business logic has excellent coverage (86-99%)
- Untested code is primarily API clients (intentionally mocked)
- Manual testing covers CLI input paths
- Increasing to 90%+ requires real API access
