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

# Or install in development mode
pip install -e .
```

### Configuration

```bash
# Copy example config
cp config/runtime_config.example.yaml config/runtime_config.yaml

# Edit config to add API keys / endpoints
# For Confidential tier: Add FACTORY_API_ENDPOINT
# For Top Secret tier: Add ONPREM_API_ENDPOINT
```

### Run

```bash
# Command-line interface
python cli.py

# Or if installed
atlassemi
```

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
System asks context-appropriate questions
    ↓
- Why did this surface now?
- What looks different from normal?
- Is this localized or widespread?
- What data is trusted vs uncertain?
    ↓
Scope and terms stabilize
```

### Phase 2: Structured Analysis (8D Mapping)
```
System analyzes with LLM + Knowledge Graph
    ↓
- Maps findings to 8D phases (D0-D8)
- Separates facts from hypotheses
- Queries similar historical excursions
- Identifies related systems/processes
    ↓
Generates structured 8D report
```

### Phase 3: Prevention & Documentation
```
System documents lessons learned
    ↓
- Permanent corrective actions (D5)
- Systemic prevention (D7)
- Knowledge base updates (D8)
    ↓
Closes loop
```

---

## Development Status

### ✅ Implemented
- Base agent architecture
- Security tier enforcement
- Narrative intake agent
- CLI interface
- Directory structure

### 🚧 In Progress
- Model router (dev vs runtime)
- Knowledge graph schema
- Clarification agent
- Analysis agent (8D mapping)

### 📋 Planned
- RAG integration
- Factory API clients
- Web interface
- Jupyter notebook interface
- Historical 8D ingestion

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=atlassemi --cov-report=html

# Run specific test
pytest tests/test_narrative_agent.py
```

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

**Version:** 0.1.0 (Initial Release)
**Last Updated:** 2026-01-07
