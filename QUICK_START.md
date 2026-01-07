# ATLASsemi Quick Start

**Version:** 0.1.0 | **Status:** Ready for Development

---

## 🚀 First Time Setup

```bash
# 1. Clone or navigate to repo
cd /mnt/c/src/Synterra/ATLASsemi

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set API keys (optional - works with mock LLM without keys)
export ANTHROPIC_API_KEY="your-key-here"
export ATLASSEMI_RUNTIME_MODE="dev"  # or "runtime"

# 5. Test installation
python cli.py
```

---

## 📁 Key Documentation

| File | Purpose |
|------|---------|
| **`README.md`** | Project overview, architecture, features |
| **`CLAUDE.md`** | Instructions for Claude Code (auto-loaded) |
| **`DEVELOPMENT_STATUS.md`** | What's done, what's next, testing guide |
| **`CONTINUOUS_CLAUDE_SETUP.md`** | Session continuity setup and usage |
| **`SECURITY.md`** | Security tier guidelines |
| **This file** | Quick reference card |

---

## 🎯 Common Commands

### Running the CLI

```bash
# Basic usage (mock LLM, no API key needed)
python cli.py

# With real Claude models
export ANTHROPIC_API_KEY="your-key"
python cli.py

# Runtime mode (best models, higher cost)
export ATLASSEMI_RUNTIME_MODE="runtime"
python cli.py
```

### Testing

```bash
# All tests
pytest

# With coverage
pytest --cov=atlassemi

# Specific test
pytest tests/test_narrative_agent.py -v
```

### Code Quality

```bash
# Format and lint (run before commits)
black . && isort . && flake8 .

# Type checking
mypy src/atlassemi/
```

### Git Workflow

```bash
# Use /commit skill in Claude Code for clean commits
# or manually:
git add -A
git commit -m "Your message here"
git push
```

---

## 🔐 Security Tiers Quick Reference

| Tier | Use When | Tools Allowed | Data |
|------|----------|---------------|------|
| **Tier 1: General LLM** | Public knowledge, learning | External APIs (Anthropic, OpenAI) | No fab data |
| **Tier 2: Confidential Fab** | Factory data via API | Factory APIs, local tools | Managed protection |
| **Tier 3: Top Secret** | Proprietary IP, recipes | On-prem only, air-gapped | Maximum security |

**Always ask at session start:**
1. Problem mode? (excursion / improvement / operations)
2. Security tier? (general / confidential / top secret)

---

## 🤖 Agent Workflow

```
User Problem (free-form narrative)
    ↓
Phase 0: Narrative Agent
    → Extracts observations, interpretations, constraints
    ↓
Phase 1: Clarification Agent
    → Asks mode-appropriate questions
    ↓
Phase 2: Analysis Agent
    → Performs 8D mapping (D0-D8)
    ↓
Phase 3: Prevention Agent (TODO)
    → Documents lessons learned, prevention plans
```

---

## 💡 Quick Examples

### Example 1: Test with Mock LLM

```bash
python cli.py

# Select: 1 (Yield Excursion)
# Select: 1 (General LLM)
# Enter narrative:
"""
We're seeing yield drop on litho tool Chamber B since 6 AM.
SPC shows Cpk went from 1.8 to 0.9 on CD measurements.
Lot XYZ-12345 affected, ships Friday. Need to fix fast.
"""
# System shows mock analysis
```

### Example 2: Use Real Claude API

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
export ATLASSEMI_RUNTIME_MODE="dev"  # Uses Haiku (cheap)

python cli.py
# Enter same narrative
# Gets real Claude analysis with JSON-structured output
```

### Example 3: Programmatic Usage

```python
from atlassemi.agents import NarrativeAgent
from atlassemi.agents.base import AgentInput, ProblemMode, SecurityTier
from atlassemi.config import ModelRouter, RuntimeMode

# Setup
router = ModelRouter(mode=RuntimeMode.DEV)
agent = NarrativeAgent(model_router=router)

# Execute
agent_input = AgentInput(
    mode=ProblemMode.EXCURSION,
    security_tier=SecurityTier.GENERAL_LLM,
    context={"narrative": "Yield drop on Chamber B..."}
)

output = agent.execute(agent_input)
print(output.content)
print(f"Cost: ${output.cost_usd:.4f}")
```

---

## 📊 Cost Estimates (Dev Mode)

| Operation | Cost (Haiku) | Cost (Sonnet) |
|-----------|-------------|---------------|
| Narrative Analysis | ~$0.01 | ~$0.10 |
| Clarification Questions | ~$0.01 | ~$0.10 |
| 8D Analysis | ~$0.03 | ~$0.30 |
| **Full Workflow** | **~$0.05** | **~$0.50** |

**Tip:** Use dev mode (Haiku) for development, runtime mode (Sonnet/Opus) for actual problems.

---

## 🔧 Continuous Claude Usage

### Starting a Session

```bash
# In Claude Code, at session start:
"Create a continuity ledger for [task name]"
```

### During Work

```bash
# Before context full (>70%):
"Update ledger, I'm about to clear"
# Then: /clear

# Ledger auto-loads in fresh context
```

### Ending a Session

```bash
"Create handoff, I'm done for today"

# Next session:
"Resume from handoff"
```

### Available Skills

- `/commit` - Clean git commits (no attribution)
- `/continuity_ledger` - Save session state
- `/create_handoff` - Create transfer doc
- `/resume_handoff` - Resume work

---

## 🏗️ Development Status

### ✅ Complete
- Model router (dev vs runtime, tier-aware)
- Phase 0: Narrative Agent
- Phase 1: Clarification Agent
- Phase 2: Analysis Agent (8D mapping)
- Security tier enforcement
- CLI interface
- Continuous Claude infrastructure

### 🚧 Next Up
1. Prevention Agent (Phase 3)
2. Orchestrator (chain agents automatically)
3. Test suite (unit + integration)

### 📋 Future
- Knowledge graph integration
- RAG for historical 8Ds
- Web interface
- Factory API implementation

---

## 🆘 Troubleshooting

### "Import error: No module named 'atlassemi'"

```bash
# Make sure you're in the venv
source venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

### "ANTHROPIC_API_KEY not set"

```bash
# Either set it:
export ANTHROPIC_API_KEY="your-key"

# Or run with mock LLM (works without API key)
python cli.py  # Just uses mock responses
```

### "Security violation" error

```python
# Check which tier you're in
from atlassemi.security.tier_enforcer import TierEnforcer, SecurityTier

enforcer = TierEnforcer(SecurityTier.CONFIDENTIAL_FAB)
print(enforcer.get_allowed_tools())  # Shows what's permitted
```

### Agent returns unparseable JSON

- Check agent prompt in `src/atlassemi/agents/*.py`
- May need to adjust JSON format requirements
- Fallback logic should catch most parsing errors

---

## 📚 Learn More

- **Architecture:** See `README.md`
- **Agent Development:** See `CLAUDE.md` → "Agent Development Guidelines"
- **Security:** See `SECURITY.md`
- **Session Continuity:** See `CONTINUOUS_CLAUDE_SETUP.md`
- **Current Status:** See `DEVELOPMENT_STATUS.md`

---

## 🎓 Example Session Flow

```
1. User opens Claude Code in ATLASsemi directory
   → CLAUDE.md auto-loads

2. Claude asks: "Problem mode and security tier?"
   → User: "Excursion, General LLM"

3. User runs: python cli.py
   → Selects mode, tier, enters narrative

4. CLI executes Phase 0 (narrative analysis)
   → Shows extracted observations, hypotheses

5. Claude asks: "Create ledger for this work?"
   → User: "Yes, create ledger"

6. Work continues... context gets full
   → User: "Update ledger and clear"

7. Fresh context, ledger auto-loads
   → Work continues from checkpoint

8. End of day:
   → User: "Create handoff"

9. Next session:
   → User: "Resume from handoff"
   → Full context restored

10. Work complete:
    → Use /commit skill for clean git commit
```

---

## ✅ Verification Checklist

Before starting development:

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list | grep anthropic`)
- [ ] Can run `python cli.py` successfully
- [ ] Can run `pytest` (even if no tests yet)
- [ ] CLAUDE.md exists and is loaded in Claude Code
- [ ] Security tier system understood (3 tiers)
- [ ] Know how to create ledgers (`thoughts/ledgers/`)
- [ ] Know how to use `/commit` skill

---

**Ready to go! 🚀**

Start with: `python cli.py` or ask Claude to create a ledger for your next task.
