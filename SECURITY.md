# ATLASsemi Security Guidelines

**CRITICAL:** This document outlines mandatory security practices for ATLASsemi.

---

## Security Tier System

ATLASsemi enforces a three-tier security model. Violations are **BLOCKED** (not just warned).

### Tier 1: General LLM
**Purpose:** Public knowledge, general reasoning

**Allowed:**
- ✅ External LLM APIs (Anthropic, OpenAI, Google, Perplexity)
- ✅ Local tools (git, file operations)
- ✅ Public documentation

**Prohibited:**
- ❌ Factory data (SPC, FDC, metrology)
- ❌ Internal SOPs or reports
- ❌ Proprietary tool information

**Use Case:** General industry research, learning, non-sensitive reasoning

---

### Tier 2: Confidential Fab
**Purpose:** Managed factory data with protection

**Allowed:**
- ✅ Factory API for LLM calls (internal endpoint)
- ✅ SPC summary data (via factory API)
- ✅ FDC summary metrics (via factory API)
- ✅ Metrology and defect summaries (via factory API)
- ✅ Approved internal SOPs
- ✅ Knowledge graph (internal)
- ✅ Local tools

**Prohibited:**
- ❌ External LLM APIs (no raw data to external services)
- ❌ Tool recipes or sensitive parameters
- ❌ Proprietary process IP

**Use Case:** Most fab problem-solving with managed data protection

**Configuration:**
```yaml
security_tier: confidential
factory_api_endpoint: https://factory-genai.internal.com/api
factory_api_key: ${FACTORY_API_KEY}  # From environment
```

---

### Tier 3: Top Secret
**Purpose:** Proprietary IP, trade secrets, on-prem only

**Allowed:**
- ✅ On-premises LLM only (air-gapped or strictly firewalled)
- ✅ Local tools only
- ✅ Proprietary tool recipes
- ✅ Novel process development data
- ✅ Pre-patent inventions

**Prohibited:**
- ❌ External LLM APIs (no external connectivity)
- ❌ Factory APIs (if they route externally)
- ❌ Any data transmission outside secure environment

**Use Case:** Trade secrets, competitive advantage processes, pre-patent work

**Configuration:**
```yaml
security_tier: top_secret
onprem_api_endpoint: http://internal-llm.local:8080
# No external connectivity allowed
```

---

## Enforcement

### Pre-Tool-Use Validation

Every tool use is validated before execution:

```python
from atlassemi.security.tier_enforcer import TierEnforcer, SecurityTier

enforcer = TierEnforcer(current_tier=SecurityTier.CONFIDENTIAL_FAB)

# This will BLOCK
try:
    enforcer.validate_tool_use("anthropic")  # External API
except SecurityViolationError as e:
    print(e)  # "Use factory_genai instead"
```

### Audit Trail

All operations are logged:
- Tool use attempts (allowed and blocked)
- Tier transitions
- Data access
- Query patterns

Logs stored in: `logs/audit_{session_id}.log`

---

## Data Handling Rules

### SPC/FDC/Metrology Data (Tier 2)

**Allowed:**
- ✅ Summary statistics (mean, std dev, Cpk)
- ✅ Trend information (increasing, decreasing, stable)
- ✅ Out-of-spec flags (yes/no)

**Prohibited:**
- ❌ Raw time-series data
- ❌ Wafer-level identifiers (unless anonymized)
- ❌ Logging raw data to disk

### Tool Recipes (Tier 3 Only)

**Allowed:**
- ✅ On-prem analysis only
- ✅ Never transmitted outside secure environment
- ✅ Access controlled by badge/role

**Prohibited:**
- ❌ Transmission to factory API
- ❌ External LLM processing
- ❌ Logging recipe details

### Historical 8D Reports (Tier 2+)

**Allowed:**
- ✅ Index and search via knowledge graph
- ✅ Cite document IDs
- ✅ Extract patterns and lessons learned

**Prohibited:**
- ❌ Transmitting full reports to external APIs
- ❌ Including proprietary tool names in external queries

---

## Session Management

### Starting a Session

**Always confirm tier selection:**
```
Select security tier [1-3]: 2
Security Tier: CONFIDENTIAL_FAB
Allowed tools: factory_genai, knowledge_graph, local_files, git
```

### Tier Transitions

**Downgrading** (e.g., Confidential → General):
- ✅ Allowed after sanitizing data
- ✅ Requires explicit user confirmation
- ✅ Audit log records transition

**Upgrading** (e.g., General → Confidential):
- ✅ Allowed with user confirmation
- ✅ Previous data tagged with lower tier
- ✅ Cannot retroactively upgrade data classification

---

## API Key Management

### Environment Variables (Preferred)

```bash
# ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export FACTORY_API_KEY="fac-..."
export ONPREM_API_ENDPOINT="http://internal-llm.local:8080"
```

### Configuration File (Alternative)

```yaml
# config/runtime_config.yaml (NEVER COMMIT)
api_keys:
  anthropic: ${ANTHROPIC_API_KEY}
  factory: ${FACTORY_API_KEY}
```

**CRITICAL:**
- ❌ Never commit API keys to git
- ❌ Never hardcode keys in source code
- ✅ Use environment variables or secure config files
- ✅ Add config files to `.gitignore`

---

## Knowledge Base Security

### Vector Store (Tier 2+)

**Allowed:**
- ✅ Local embeddings (sentence-transformers, no external API)
- ✅ Store on internal servers
- ✅ Index approved documents only

**Prohibited:**
- ❌ External embedding APIs (OpenAI, Cohere) for confidential data
- ❌ Uploading proprietary docs to external vector stores

### Knowledge Graph (Tier 2+)

**Allowed:**
- ✅ Internal Neo4j instance
- ✅ Relationships between tools, processes, materials
- ✅ Anonymized linkages

**Prohibited:**
- ❌ External graph databases (Neptune, etc.)
- ❌ Sensitive parameter values in node properties

---

## Incident Response

### Security Violation Detected

If a security violation occurs:

1. **Immediate:** Tool use is blocked
2. **Log:** Violation recorded in audit trail
3. **Alert:** User notified with suggestion
4. **Review:** Security team reviews violation log

### Data Leak Suspected

If proprietary data may have been transmitted externally:

1. **Stop:** Immediately terminate session
2. **Report:** Contact security team
3. **Audit:** Review session logs
4. **Remediate:** Rotate API keys if needed

---

## Compliance Checklist

Before each session:
- [ ] Confirmed correct security tier
- [ ] Reviewed allowed tools for this tier
- [ ] Verified no proprietary data in General tier
- [ ] API keys loaded from secure source
- [ ] Audit logging enabled

After each session:
- [ ] Reviewed audit log
- [ ] No tier violations occurred
- [ ] Output sanitized if sharing externally
- [ ] Session data archived securely

---

## Training Requirements

Users must complete:
- [ ] Security tier training
- [ ] Data classification training
- [ ] Proprietary information handling
- [ ] Incident reporting procedures

---

## Contact

**Security Questions:** Contact InfoSec team
**Data Classification:** Contact Legal/Compliance
**Tool Issues:** Contact Yield Engineering

---

**Document Version:** 1.0
**Last Updated:** 2026-01-07
**Review Frequency:** Quarterly
