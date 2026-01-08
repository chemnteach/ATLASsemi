# ATLASsemi Deployment Guide

## Overview

ATLASsemi is a production-ready agentic problem-solving system for semiconductor manufacturing. This guide covers installation, configuration, and operational deployment.

**Version:** 1.0.0
**Status:** Production Ready
**Last Updated:** 2026-01-07

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running ATLASsemi](#running-atlassemi)
5. [Security Tier Configuration](#security-tier-configuration)
6. [Model Routing](#model-routing)
7. [Testing](#testing)
8. [Monitoring and Costs](#monitoring-and-costs)
9. [Troubleshooting](#troubleshooting)
10. [Production Checklist](#production-checklist)

---

## Prerequisites

### System Requirements

- **Python:** 3.10 or higher
- **Operating System:** Linux, macOS, or Windows
- **Memory:** 2GB minimum (4GB recommended)
- **Network:** Internet access for Tier 1 (General LLM) operations

### Required Software

```bash
# Python 3.10+
python --version  # Should show 3.10 or higher

# pip (usually included with Python)
pip --version

# Git (for version control)
git --version
```

### API Keys

Depending on your deployment tier:

**Tier 1 (General LLM):**
- Anthropic API key (Claude Haiku/Sonnet/Opus)
- OR OpenAI API key

**Tier 2 (Confidential Fab):**
- Factory API credentials (provided by factory IT)

**Tier 3 (Top Secret):**
- On-premises LLM deployment required
- No external API keys needed

---

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/your-org/ATLASsemi.git
cd ATLASsemi
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (optional, for testing)
pip install -r requirements-dev.txt
```

### Step 4: Verify Installation

```bash
# Run test suite
pytest

# Check coverage
pytest --cov=atlassemi --cov-report=html

# Expected: All tests passing, 77%+ coverage
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Runtime Mode (dev = fast/cheap, runtime = best models)
ATLASSEMI_RUNTIME_MODE=dev  # or "runtime" for production

# Tier 1: External LLM API Key
ANTHROPIC_API_KEY=your_anthropic_key_here

# Tier 2: Factory API Credentials (if applicable)
FACTORY_API_URL=https://factory-api.internal
FACTORY_API_KEY=your_factory_key_here

# Tier 3: On-prem LLM Endpoint (if applicable)
ONPREM_LLM_URL=http://onprem-llm.internal:8000
```

### Runtime Configuration

**Dev Mode** (for testing and development):
- Uses Claude Haiku (fast, cheap)
- Tier 1 cost: ~$0.01 per narrative
- Full workflow cost: ~$0.05-$0.08

**Runtime Mode** (for production):
- Uses Claude Sonnet/Opus (best quality)
- Tier 1 cost: ~$0.03-$0.05 per narrative
- Full workflow cost: ~$0.15-$0.25

Set mode via environment:
```bash
export ATLASSEMI_RUNTIME_MODE="runtime"
```

Or in code:
```python
from atlassemi.config import ModelRouter, RuntimeMode

router = ModelRouter(mode=RuntimeMode.RUNTIME)
```

---

## Running ATLASsemi

### Command-Line Interface

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run CLI
python cli.py
```

### CLI Workflow

1. **Select Problem Mode:**
   - 1: Yield Excursion Response (fast containment)
   - 2: Yield Improvement (continuous improvement)
   - 3: Factory Operations (sustainment)

2. **Select Security Tier:**
   - 1: General LLM (public knowledge only)
   - 2: Confidential Fab (factory API access)
   - 3: Top Secret (on-prem only)

3. **Provide Narrative:**
   - Type free-form problem description
   - Press `Ctrl+D` (Unix) or `Ctrl+Z` (Windows) when done

4. **Answer Clarification Questions:**
   - System generates mode-aware questions
   - Answer each or type `skip` to skip

5. **Review Results:**
   - Narrative analysis (facts, hypotheses)
   - 8D analysis mapping
   - Prevention plan and lessons learned
   - Cost summary

### Programmatic Usage

```python
from atlassemi.orchestrator import WorkflowOrchestrator
from atlassemi.agents.base import ProblemMode, SecurityTier
from atlassemi.config import ModelRouter, RuntimeMode

# Initialize
router = ModelRouter(mode=RuntimeMode.DEV)
orchestrator = WorkflowOrchestrator(model_router=router)

# Run workflow
result = orchestrator.run_workflow(
    narrative="Yield dropped 15% on Chamber B after PM...",
    mode=ProblemMode.EXCURSION,
    tier=SecurityTier.GENERAL_LLM,
    answer_collector=None  # or custom function
)

# Access results
print(f"Facts: {result.facts_identified}")
print(f"Cost: ${result.total_cost_usd:.4f}")
print(f"8D Phases: {result.eight_d_phases_addressed}")
```

---

## Security Tier Configuration

### Tier 1: General LLM

**Use Cases:**
- Training and education
- Public knowledge queries
- Industry best practices

**Configuration:**
```python
SecurityTier.GENERAL_LLM
```

**Allowed Tools:**
- External APIs (Anthropic, OpenAI)
- Local tools (git, file system)
- Web search (if enabled)

**Restrictions:**
- NO proprietary fab data
- NO tool recipes
- NO trade secrets

### Tier 2: Confidential Fab

**Use Cases:**
- Factory API queries
- SPC/FDC data analysis
- Approved SOP retrieval

**Configuration:**
```python
SecurityTier.CONFIDENTIAL_FAB
```

**Allowed Tools:**
- Factory APIs (SPC, FDC, MES)
- Knowledge graph
- Local tools

**Restrictions:**
- NO external APIs with raw fab data
- Data must be sanitized before external calls
- Audit trail required

### Tier 3: Top Secret

**Use Cases:**
- Proprietary process development
- Tool recipe analysis
- Trade secret protection

**Configuration:**
```python
SecurityTier.TOP_SECRET
```

**Allowed Tools:**
- On-prem LLM ONLY
- Local tools (air-gapped)
- Knowledge graph (local)

**Restrictions:**
- NO external communication whatsoever
- Complete audit trail
- Requires security clearance

### Tier Enforcement

The system HARD BLOCKS violations:

```python
from atlassemi.security.tier_enforcer import (
    TierEnforcer,
    SecurityViolationError
)

enforcer = TierEnforcer(current_tier=SecurityTier.CONFIDENTIAL_FAB)

# This will raise SecurityViolationError
enforcer.validate_tool_use("anthropic")  # BLOCKED
```

---

## Model Routing

### Tier-Aware Routing

ATLASsemi automatically routes to appropriate models based on tier:

| Tier | Dev Mode | Runtime Mode |
|------|----------|--------------|
| Tier 1 | Claude Haiku | Claude Sonnet/Opus |
| Tier 2 | Factory API | Factory API |
| Tier 3 | On-prem API | On-prem API |

### Cost Tracking

```python
# Get usage summary
router = ModelRouter(mode=RuntimeMode.DEV)
# ... after workflow execution ...
print(router.get_usage_summary())
```

Output:
```
Total calls: 4
Total input tokens: 5234
Total output tokens: 1456
Total cost: $0.0734
```

### Custom Model Configuration

Edit `src/atlassemi/config/model_router.py` for custom models:

```python
def get_model_config(
    self,
    task_type: str,
    security_tier: SecurityTier
) -> ModelConfig:
    # Add your custom routing logic here
```

---

## Testing

### Unit Tests

```bash
# Run all tests
pytest

# Run specific agent tests
pytest tests/test_narrative_agent.py

# Run with verbose output
pytest -v
```

### Integration Tests

```bash
# Run orchestrator integration tests
pytest tests/test_orchestrator.py -v

# Run with coverage
pytest tests/ --cov=atlassemi --cov-report=html
```

### Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=atlassemi --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

**Expected Coverage:**
- Overall: 77%+
- Narrative Agent: 99%
- Clarification Agent: 86%
- Analysis Agent: 93%
- Prevention Agent: 97%

### Mock LLM Testing

Tests use mock responses (no API calls required):

```python
def test_narrative_agent():
    # Pass None for model_router to enable mocking
    agent = NarrativeAgent(model_router=None)

    agent_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={"narrative": "Test"}
    )

    output = agent.execute(agent_input)
    assert output.agent_type == "narrative"
```

---

## Monitoring and Costs

### Cost Estimation

**Dev Mode (Claude Haiku):**
- Narrative: $0.01
- Clarification: $0.01
- Analysis: $0.03-$0.05
- Prevention: $0.01-$0.02
- **Total per workflow:** ~$0.05-$0.08

**Runtime Mode (Claude Sonnet/Opus):**
- Narrative: $0.03-$0.05
- Clarification: $0.02-$0.03
- Analysis: $0.08-$0.12
- Prevention: $0.03-$0.05
- **Total per workflow:** ~$0.15-$0.25

### Usage Monitoring

Track costs via ModelRouter:

```python
router.usage_stats
# {
#   'total_calls': 4,
#   'total_input_tokens': 5234,
#   'total_output_tokens': 1456,
#   'total_cost_usd': 0.0734
# }
```

### Logging

Enable logging for debugging:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("atlassemi")
```

---

## Troubleshooting

### Issue: "Module not found: atlassemi"

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Verify Python path
python -c "import sys; print(sys.path)"

# Run from project root
cd ATLASsemi
python cli.py
```

### Issue: "anthropic package not installed"

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep anthropic
```

### Issue: "SecurityViolationError: External API access blocked"

**Cause:** Using external API at Tier 2 or Tier 3

**Solution:**
- Use Tier 1 for external API access
- Or configure Factory/On-prem API for Tier 2/3

### Issue: "JSON parsing failed in agent"

**Cause:** LLM returned malformed JSON

**Solution:**
- Check model configuration
- Verify prompt templates
- Enable debug logging to see raw responses

### Issue: High costs in production

**Solution:**
- Use `RuntimeMode.DEV` for testing
- Switch to `RuntimeMode.RUNTIME` only for critical cases
- Monitor usage via `router.get_usage_summary()`

---

## Production Checklist

### Pre-Deployment

- [ ] All tests passing (`pytest`)
- [ ] Coverage ≥77% (`pytest --cov`)
- [ ] Environment variables configured
- [ ] API keys secured (not in code)
- [ ] Security tier enforcement tested
- [ ] Cost monitoring enabled

### Deployment

- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Runtime mode set (`ATLASSEMI_RUNTIME_MODE`)
- [ ] Security tier policy documented
- [ ] User training completed
- [ ] Audit logging configured (Tier 2/3)

### Post-Deployment

- [ ] Monitor costs via usage stats
- [ ] Review security violations (should be zero)
- [ ] Collect user feedback
- [ ] Document common use cases
- [ ] Establish escalation process for issues

### Tier 2/3 Specific

- [ ] Factory API credentials secured
- [ ] On-prem LLM endpoint configured
- [ ] Network isolation verified (Tier 3)
- [ ] Audit trail system active
- [ ] Security clearance verified
- [ ] Compliance review completed

---

## Next Steps

1. **Training:** Schedule user training sessions
2. **Pilot:** Run pilot with 5-10 real problems
3. **Feedback:** Collect feedback and iterate
4. **Scale:** Expand to full production deployment
5. **Monitor:** Track costs, usage, and effectiveness

---

## Support

For issues or questions:

1. **Documentation:** Check `README.md` and `CLAUDE.md`
2. **Tests:** Review test cases for usage examples
3. **Code:** Agent prompts are in `src/atlassemi/agents/*.py`
4. **Security:** See `SECURITY.md` for tier guidelines

---

## Appendix: File Structure

```
ATLASsemi/
├── cli.py                      # Main CLI entry point
├── src/atlassemi/
│   ├── agents/                 # Phase 0-3 agents
│   ├── orchestrator/           # Workflow coordination
│   ├── config/                 # Model routing
│   └── security/               # Tier enforcement
├── tests/                      # Test suite (77% coverage)
├── docs/                       # Documentation
├── config/                     # Runtime configuration
└── requirements.txt            # Dependencies
```

---

**End of Deployment Guide**
