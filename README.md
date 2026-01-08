# ATLASsemi

**Semiconductor Fab Problem-Solving Assistant**

ATLASsemi is an internal, firewall-protected agentic problem-solving system for semiconductor manufacturing. It transforms messy, ambiguous fab problems into structured, auditable 8D analysis artifacts.

---

## Purpose

Support human decision-making in:
- **Yield excursion response** (fast containment)
- **Yield improvement / continuous improvement** (process optimization)
- **Factory operations troubleshooting** (sustainment)

**What it does:** Augment human judgment with structured analysis
**What it doesn't do:** Implement changes or make autonomous decisions

---

## Key Features

### 🔒 **Security-First Design**
- Three-tier security model (General LLM / Confidential Fab / Top Secret)
- Hard enforcement of tier boundaries (blocks, not warns)
- Audit trail for all operations

### 📝 **8D Methodology Integration**
- Explicitly embeds 8D problem-solving process (D0-D8)
- Separates facts from hypotheses
- Produces auditable artifacts

### 🎯 **Narrative-First Intake**
- Starts with free-form problem description
- No premature structuring or precision demands
- Comfortable with incomplete information

### 🧠 **Hybrid Knowledge System**
- **Knowledge Graph:** Relationships between tools, processes, materials
- **Vector RAG:** Historical 8Ds, SOPs, lessons learned
- **Specialized Models:** Yield modeling, defect classification

---

## Quick Start

### Installation

```bash
# Clone repository
git clone <internal-repo-url> ATLASsemi
cd ATLASsemi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests to verify installation
pytest
```

### Configuration

Set environment variables in `.env`:

```bash
# Runtime mode (dev = fast/cheap, runtime = best models)
ATLASSEMI_RUNTIME_MODE=dev

# API key for Tier 1 (General LLM)
ANTHROPIC_API_KEY=your_key_here
```

For complete deployment guide, see **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)**

### Run

```bash
# Command-line interface
python cli.py
```

The CLI will guide you through:
1. Selecting problem mode (excursion/improvement/operations)
2. Selecting security tier (general/confidential/top_secret)
3. Providing narrative description
4. Answering clarification questions
5. Reviewing analysis and prevention plan

---

## Architecture

```
ATLASsemi/
├── src/atlassemi/
│   ├── agents/              # Problem-solving agents
│   │   ├── base.py          # Base agent class
│   │   ├── narrative_agent.py      # Phase 0: Intake
│   │   ├── clarification_agent.py  # Phase 1: Questions
│   │   ├── analysis_agent.py       # Phase 2: 8D Analysis
│   │   └── prevention_agent.py     # Phase 3: Prevention
│   │
│   ├── orchestrator/        # Workflow coordination
│   ├── security/            # Tier enforcement
│   ├── knowledge/           # Knowledge graph + RAG
│   ├── methodology/         # 8D mapping
│   └── tools/               # Specialized tools
│
├── docs/                    # Documentation
│   ├── domains/             # Mode configurations
│   └── methodology/         # 8D process guides
│
├── config/                  # Configuration files
└── tests/                   # Test suite
```

---

## Three Security Tiers

### Tier 1: General LLM
- **Allowed:** Public knowledge, industry best practices
- **Tools:** External APIs (Anthropic, OpenAI, etc.)
- **Use case:** General reasoning, no proprietary data

### Tier 2: Confidential Fab
- **Allowed:** Factory API access, SPC/FDC summaries, approved SOPs
- **Tools:** Factory APIs, knowledge graph, local tools
- **Use case:** Most fab problems with managed data protection

### Tier 3: Top Secret
- **Allowed:** On-prem only, proprietary IP, tool recipes
- **Tools:** On-prem LLM, local tools, air-gapped
- **Use case:** Trade secrets, novel processes, pre-patent work

---

## Three Problem-Solving Modes

### Mode A: Yield Excursion Response
- **Focus:** Rapid containment, scope definition, risk assessment
- **Timeline:** Hours to days
- **8D Emphasis:** D0-D6 (preparation through validation)

### Mode B: Yield Improvement
- **Focus:** Chronic issues, variability reduction, process optimization
- **Timeline:** Weeks to months
- **8D Emphasis:** D2, D4-D8 (characterization through prevention)

### Mode C: Factory Operations
- **Focus:** Tool availability, dispatch, queue time, sustainment
- **Timeline:** Ongoing
- **8D Emphasis:** D3, D7 (containment and prevention)

---

## Workflow

ATLASsemi uses a **WorkflowOrchestrator** to execute all 4 phases sequentially:

### Phase 0: Narrative Intake
```
User provides free-form problem description
    ↓
System extracts:
- Observations (facts)
- Interpretations (theories)
- Constraints (time, production impact)
- Urgency signals
- Data sources mentioned
    ↓
Reflects back for validation
```

### Phase 1: Adaptive Clarification
```
System generates mode-aware questions
    ↓
- Why did this surface now?
- What looks different from normal?
- Is this localized or widespread?
- What data is trusted vs uncertain?
    ↓
User answers (or skips) questions
    ↓
Scope and terms stabilize
```

### Phase 2: Structured Analysis (8D Mapping)
```
System analyzes with comprehensive context
    ↓
- Maps findings to 8D phases (D0-D8)
- Separates facts from hypotheses
- Incorporates clarification answers
- Identifies gaps in understanding
    ↓
Generates structured 8D report
```

### Phase 3: Prevention & Documentation
```
System documents lessons learned
    ↓
- Permanent corrective actions (D5)
- Systemic prevention (D7)
- Lessons learned (D8)
- Process improvements
    ↓
Closes loop
```

**Orchestrator Benefits:**
- Sequential execution with context passing
- Cost tracking across all phases
- Comprehensive workflow results
- Error handling and recovery

---

## Development Status

**Version 1.0.0 - Production Ready** 🎉

### ✅ v1.0 Complete (2026-01-07)
- ✅ Base agent architecture
- ✅ Security tier enforcement (hard blocking)
- ✅ Model router (dev vs runtime with tier-aware routing)
- ✅ Narrative intake agent (Phase 0)
- ✅ Clarification agent (Phase 1)
- ✅ Analysis agent (Phase 2: 8D mapping)
- ✅ Prevention agent (Phase 3: lessons learned)
- ✅ **WorkflowOrchestrator** (chains all 4 phases)
- ✅ CLI interface (fully integrated)
- ✅ Cost tracking and usage monitoring
- ✅ **Comprehensive test suite** (25 tests, 77% coverage)
- ✅ **Deployment documentation** (see docs/DEPLOYMENT.md)

### Test Coverage (v1.0)
```
Overall: 77%
- Narrative Agent: 99%
- Clarification Agent: 86%
- Analysis Agent: 93%
- Prevention Agent: 97%
- Orchestrator: Integration tested
```

### 📋 Future Enhancements
- Knowledge graph integration
- Factory API connectors (Tier 2)
- On-prem LLM integration (Tier 3)
- RAG for historical 8D lookup
- Web interface
- Jupyter notebook interface

---

## Testing

ATLASsemi includes a comprehensive test suite with 77% coverage:

```bash
# Run all tests (25 tests)
pytest

# Run with coverage report
pytest --cov=atlassemi --cov-report=html

# View coverage report
open htmlcov/index.html

# Run specific test module
pytest tests/test_narrative_agent.py -v

# Run integration tests
pytest tests/test_orchestrator.py -v
```

**Test Suite:**
- 13 agent unit tests (narrative, clarification, analysis, prevention)
- 4 orchestrator integration tests
- 4 model router tests
- 4 security tier enforcement tests

All tests use mock LLM responses (no API keys required)

---

## Security Notes

**CRITICAL:** This system handles proprietary fab data.

1. **Never commit API keys or credentials**
2. **Always select correct security tier**
3. **Audit trail is mandatory**
4. **Default to most restrictive tier when uncertain**
5. **Review `.gitignore` patterns for proprietary data**

See `SECURITY.md` for complete security guidelines.

---

## Contributing

This is an internal tool. For questions or contributions:

1. Create feature branch from `main`
2. Implement with tests
3. Run linters: `black .`, `isort .`, `flake8 .`
4. Submit PR with description

---

## License

Internal use only. Proprietary and confidential.

---

## Contact

For questions or support, contact the Yield Engineering team.

---

**Version:** 1.0.0 - Production Ready
**Release Date:** 2026-01-07

For deployment instructions, see **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)**
