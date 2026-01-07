# CLAUDE.md
Continuous Claude v2 for ATLASsemi

---

This file provides guidance to Claude Code when working with the ATLASsemi codebase.

## Project Overview

**ATLASsemi** is an internal, firewall-protected agentic problem-solving system for semiconductor manufacturing. It transforms messy fab problems into structured, auditable 8D analysis artifacts.

**Core Purpose:** Support human decision-making in yield excursion response, yield improvement, and factory operations troubleshooting through structured 8D methodology.

**Key Principles:**
- Security-first design (three-tier security model)
- Narrative-first intake (no premature structuring)
- 8D methodology integration (D0-D8)
- Fact vs hypothesis separation
- Mode-aware workflows (excursion / improvement / operations)

## Architecture

ATLASsemi uses a multi-agent architecture with tier-aware model routing:

```
User Narrative (free-form)
    ↓
Phase 0: Narrative Agent (extract observations, interpretations)
    ↓
Phase 1: Clarification Agent (mode-aware questions)
    ↓
Phase 2: Analysis Agent (8D mapping)
    ↓
Phase 3: Prevention Agent (lessons learned, prevention plans)
```

## Directory Structure

```
ATLASsemi/
├── src/atlassemi/
│   ├── agents/              # Phase 0-3 agents
│   │   ├── base.py          # Base agent class
│   │   ├── narrative_agent.py
│   │   ├── clarification_agent.py
│   │   ├── analysis_agent.py
│   │   └── prevention_agent.py  # TODO
│   │
│   ├── config/              # Model routing
│   │   └── model_router.py  # Dev vs runtime, tier-aware
│   │
│   ├── security/            # Tier enforcement
│   │   └── tier_enforcer.py
│   │
│   ├── orchestrator/        # Workflow coordination (TODO)
│   ├── knowledge/           # Knowledge graph (TODO)
│   └── tools/               # Specialized tools (TODO)
│
├── thoughts/                # Working memory (Continuous Claude)
│   ├── ledgers/             # Session state
│   └── shared/
│       ├── handoffs/        # Between-session transfers
│       └── plans/           # Implementation plans
│
├── .claude/                 # Continuous Claude configuration
│   ├── agents/              # Custom agents
│   ├── rules/               # Behavioral rules
│   ├── hooks/               # Session lifecycle hooks
│   └── cache/               # Artifact Index (gitignored)
│
├── config/                  # Runtime configuration
├── docs/                    # Documentation
├── tests/                   # Test suite
└── cli.py                   # Main CLI interface
```

## Security Tier System

ATLASsemi enforces three security tiers (HARD BLOCKING, not warnings):

### Tier 1: General LLM
- **When:** Public knowledge, industry best practices, learning
- **Tools:** External APIs (Anthropic, OpenAI)
- **Data:** No proprietary fab data

### Tier 2: Confidential Fab
- **When:** Factory API access, SPC/FDC summaries, approved SOPs
- **Tools:** Factory APIs, knowledge graph, local tools
- **Data:** Managed fab data protection
- **CRITICAL:** NO external APIs with raw fab data

### Tier 3: Top Secret
- **When:** Proprietary IP, tool recipes, trade secrets
- **Tools:** On-prem LLM ONLY, local tools, air-gapped
- **Data:** Maximum security, audit trail
- **CRITICAL:** NO external communication whatsoever

**At session start, always ask:**
1. "What problem mode?" (excursion / improvement / operations)
2. "What security tier?" (general / confidential / top secret)

Document both in ledger immediately.

## Model Router System

ATLASsemi uses tier-aware model routing:

**Dev Mode** (fast/cheap for testing):
- Tier 1: Claude Haiku
- Tier 2: Factory API
- Tier 3: On-prem API

**Runtime Mode** (best models for production):
- Tier 1: Claude Sonnet/Opus
- Tier 2: Factory API
- Tier 3: On-prem API

Set via: `export ATLASSEMI_RUNTIME_MODE="dev"` or `"runtime"`

## Common Tasks

### Running the CLI

```bash
# Set runtime mode (optional, defaults to dev)
export ATLASSEMI_RUNTIME_MODE="dev"

# Set API key if using real LLMs
export ANTHROPIC_API_KEY="your-key"

# Run CLI
python cli.py
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=atlassemi --cov-report=html

# Specific test
pytest tests/test_narrative_agent.py
```

### Code Quality

```bash
# Format and lint
black . && isort . && flake8 .

# Type checking
mypy src/atlassemi/
```

### Programmatic Usage

```python
from atlassemi.agents import NarrativeAgent
from atlassemi.agents.base import AgentInput, ProblemMode, SecurityTier
from atlassemi.config import ModelRouter, RuntimeMode

# Initialize router
router = ModelRouter(mode=RuntimeMode.DEV)

# Create agent
agent = NarrativeAgent(model_router=router)

# Execute
agent_input = AgentInput(
    mode=ProblemMode.EXCURSION,
    security_tier=SecurityTier.GENERAL_LLM,
    context={"narrative": "Problem description..."}
)

output = agent.execute(agent_input)
print(output.content)
```

## Continuous Claude Integration

### Session Management

ATLASsemi uses the **clear, don't compact** approach:

```
Session Start → Work → Save to ledger → /clear → Fresh context + ledger loaded
```

**Key Skills:**
- `/continuity_ledger` - Save session state before /clear
- `/create_handoff` - Create detailed handoff for next session
- `/resume_handoff` - Load handoff and continue work

### Ledger Format

Every ledger should include:

```yaml
---
problem_mode: excursion|improvement|operations
security_tier: general_llm|confidential_fab|top_secret
api_routing: which endpoints to use
---

## Goal
[What does "done" look like?]

## Constraints
[Technical requirements, security tier restrictions]

## State
- Done: [✓] Completed items
- Now: [→] Current task
- Next: Upcoming tasks

## Key Decisions
[Choices made with rationale]

## Working Set
[Files, commands, branch]
```

### Handoff Pattern

```
1. Work on task
2. Before context full: "Update ledger"
3. /clear (fresh context, ledger auto-loads)
4. Continue work
5. End of day: "Create handoff"
6. Next session: "Resume from handoff"
```

## Agent Development Guidelines

When working on agents:

1. **Inherit from BaseAgent**
   - Implement `generate_prompt()` and `process_response()`
   - Return structured `AgentOutput`

2. **Separate Facts from Hypotheses**
   - Facts: What we know for sure
   - Hypotheses: What we suspect (need validation)

3. **Map to 8D Phases**
   - Use `extract_eight_d_mapping()` or manual assignment
   - D0-D8 phases should be explicit

4. **Mode-Aware Prompts**
   - Excursion: Fast containment focus
   - Improvement: Chronic issues, variability
   - Operations: Blocking issues, urgency

5. **Security-Conscious**
   - Never log proprietary data in git
   - Respect tier boundaries
   - Use appropriate model routing

## Code Style

- **Python 3.10+** features allowed
- **Type hints** required for public APIs
- **Docstrings** required for classes and public methods
- **black** for formatting
- **isort** for import sorting
- **flake8** for linting

## Testing Guidelines

- **Unit tests** for each agent
- **Mock LLM responses** for deterministic testing
- **Test JSON parsing** edge cases
- **Integration tests** for full workflow
- **Security tests** for tier enforcement

Example:

```python
def test_narrative_agent_parsing():
    """Test narrative agent can parse problematic input."""
    agent = NarrativeAgent(model_router=None)  # No LLM calls

    # Mock response
    agent._call_llm = lambda *args: '{"observations": ["Test"]}'

    agent_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={"narrative": "Test problem"}
    )

    output = agent.execute(agent_input)
    assert len(output.facts) > 0
```

## Important Notes

### Security Reminders

**CRITICAL:** This system handles proprietary fab data.

1. **Never commit API keys or credentials**
2. **Always select correct security tier at session start**
3. **Audit trail is mandatory for Tier 2 and 3**
4. **Default to most restrictive tier when uncertain**
5. **Review `.gitignore` patterns for proprietary data**

### Cost Awareness

Track costs via ModelRouter:

```python
router.get_usage_summary()  # Shows session costs
```

**Typical costs (dev mode):**
- Narrative analysis: ~$0.01
- Clarification: ~$0.01
- 8D analysis: ~$0.03-$0.05
- Full workflow: ~$0.05-$0.08

### Performance Optimization

- Use **dev mode** for testing (10x cheaper)
- Use **runtime mode** for production problems
- Cache common analyses when possible
- Batch similar problems

## Next Steps for Development

See `DEVELOPMENT_STATUS.md` for current implementation status.

**Priority tasks:**
1. Implement Prevention Agent (Phase 3)
2. Create Orchestrator (chain agents automatically)
3. Add comprehensive test suite
4. Knowledge graph integration (future)

## Reference Materials

- **Development Status**: `DEVELOPMENT_STATUS.md`
- **Security Guidelines**: `SECURITY.md`
- **Architecture Overview**: `README.md`
- **Example Config**: `config/runtime_config.example.yaml`

## Questions or Issues?

- Agent prompts are in `src/atlassemi/agents/*.py` - easy to customize
- Security enforcement in `src/atlassemi/security/tier_enforcer.py`
- Model routing in `src/atlassemi/config/model_router.py`

**Status:** Core agents complete (Phases 0-2), ready for orchestration.

---

**Version:** 0.1.0
**Last Updated:** 2026-01-07
