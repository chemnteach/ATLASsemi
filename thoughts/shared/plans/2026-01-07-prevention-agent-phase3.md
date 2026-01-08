# Prevention Agent (Phase 3) Implementation Plan

## Overview

Implement the Prevention Agent to complete the ATLASsemi 8D workflow. This agent generates permanent corrective actions (D5), systemic prevention recommendations (D7), and documents lessons learned (D8) based on the analysis from Phase 2.

## Current State Analysis

**What exists:**
- ✅ Phases 0-2 agents complete (Narrative, Clarification, Analysis)
- ✅ BaseAgent architecture with template method pattern
- ✅ Model router with tier-aware routing
- ✅ AgentInput/AgentOutput structures
- ✅ 8D phase detection and mapping utilities

**What's missing:**
- ❌ Prevention Agent (Phase 3)
- ❌ Integration into agent exports
- ❌ CLI integration for Prevention Agent

**Key patterns to follow:**
- Inherit from `BaseAgent` (see `src/atlassemi/agents/base.py`)
- Implement `generate_prompt()` and `process_response()`
- Return JSON-structured output for reliable parsing
- Mode-aware prompts (excursion/improvement/operations)
- Separate facts from hypotheses
- Use model router for LLM calls

## Desired End State

A fully functional Prevention Agent that:
- Takes 8D analysis from Phase 2 as input
- Generates permanent corrective actions (D5)
- Recommends systemic prevention measures (D7)
- Documents lessons learned for knowledge base (D8)
- Returns structured JSON output
- Integrates into the CLI workflow

**Verification:**
- Agent can execute successfully with mock LLM
- Agent can execute successfully with real LLM (Claude)
- Output structure matches expected JSON schema
- Cost tracking works correctly
- Agent exports from `__init__.py`

## What We're NOT Doing

- Orchestrator implementation (separate task)
- Test suite (separate task)
- Knowledge graph integration (future enhancement)
- Automatic knowledge base updates (future enhancement)

## Implementation Approach

Single-phase implementation following the established agent pattern:
1. Create `prevention_agent.py` following BaseAgent structure
2. Generate prompts that focus on D5, D7, D8
3. Parse JSON response into structured output
4. Update agent exports
5. Manual testing via CLI

## Phase 1: Prevention Agent Core Implementation

### Overview
Create the Prevention Agent class with all required methods and prompt generation logic.

### Changes Required:

#### 1. Prevention Agent File
**File**: `src/atlassemi/agents/prevention_agent.py`
**Changes**: Create new file with complete Prevention Agent implementation

```python
"""Phase 3: Prevention and Lessons Learned Agent"""

import json
from typing import Dict, Any
from .base import BaseAgent, AgentInput, AgentOutput, ProblemMode


class PreventionAgent(BaseAgent):
    """
    Phase 3 Agent: Prevention and Documentation

    Generates:
    - Permanent corrective actions (D5)
    - Systemic prevention recommendations (D7)
    - Lessons learned documentation (D8)
    """

    def __init__(self, model_router=None):
        super().__init__(agent_type="prevention", model_router=model_router)

    def generate_prompt(self, agent_input: AgentInput) -> str:
        """Generate prevention planning prompt"""

        # Extract analysis from Phase 2
        analysis = agent_input.context.get("analysis", {})
        root_causes = agent_input.context.get("root_causes", [])

        # Mode-specific guidance
        mode_guidance = self._get_mode_guidance(agent_input.mode)

        prompt = f"""You are a prevention and documentation specialist for semiconductor manufacturing 8D analysis.

{mode_guidance}

## Context from Previous Analysis

**Root Causes Identified:**
{json.dumps(root_causes, indent=2)}

**8D Analysis:**
{json.dumps(analysis, indent=2)}

## Your Task

Generate a comprehensive prevention plan with three components:

### 1. Permanent Corrective Actions (D5)
Actions to fix the root cause permanently. For each action:
- Specific action to take (recipe change, tool fix, process improvement)
- Rationale for why this prevents recurrence
- Owner/team responsible
- Implementation timeline
- Success metrics

### 2. Systemic Prevention (D7)
Changes to prevent similar issues systemically. Consider:
- SOP updates
- Preventive maintenance changes
- Automated checks/controls
- SPC limit adjustments
- Training updates
- Process control improvements
- Scope (single tool vs all tools vs entire fab)

### 3. Lessons Learned (D8)
Document knowledge for future reference:
- Key lessons from this problem
- What worked well in the investigation
- What could be improved in our response
- Knowledge base updates needed
- Documentation updates (handbooks, SOPs, etc.)
- Case studies for training

## Output Format

Return ONLY valid JSON with this structure:

{{
  "permanent_actions": [
    {{
      "action": "Specific action description",
      "rationale": "Why this prevents recurrence",
      "owner": "Process Engineering / Maintenance / etc.",
      "timeline": "Within X weeks/days",
      "success_metrics": "How to measure effectiveness",
      "implementation_steps": ["Step 1", "Step 2", "..."]
    }}
  ],
  "systemic_prevention": [
    {{
      "change": "Description of systemic change",
      "scope": "Single tool / Tool type / Entire fab",
      "implementation": "How to implement",
      "benefits": "Expected benefits",
      "risks": "Potential risks or downsides"
    }}
  ],
  "lessons_learned": [
    "Lesson 1",
    "Lesson 2",
    "..."
  ],
  "knowledge_base_updates": [
    {{
      "document": "Tool Handbook Section X / SOP-XXX / etc.",
      "update_needed": "What to add/change",
      "priority": "high / medium / low"
    }}
  ],
  "follow_up_items": [
    {{
      "item": "Action item description",
      "owner": "Who is responsible",
      "deadline": "When it should be done"
    }}
  ]
}}

Be specific and actionable. Focus on prevention, not just detection.
"""
        return prompt

    def _get_mode_guidance(self, mode: ProblemMode) -> str:
        """Get mode-specific prevention guidance"""

        if mode == ProblemMode.EXCURSION:
            return """**Mode: Excursion Response**
Focus on:
- Immediate containment actions made permanent
- Preventing similar excursions on similar tools/processes
- Early warning systems for detection
- Maintenance and recipe control improvements"""

        elif mode == ProblemMode.IMPROVEMENT:
            return """**Mode: Yield Improvement**
Focus on:
- Sustainable process improvements
- Variability reduction strategies
- Long-term capability improvements
- Best practice documentation"""

        elif mode == ProblemMode.OPERATIONS:
            return """**Mode: Operations Troubleshooting**
Focus on:
- Workflow improvements to prevent delays
- Communication and escalation improvements
- Tools and automation to speed resolution
- Process clarification to prevent confusion"""

        return ""

    def process_response(self, response: str, agent_input: AgentInput) -> AgentOutput:
        """Parse prevention plan response"""

        try:
            # Try to parse as JSON
            prevention_data = json.loads(response)

            # Extract structured fields
            permanent_actions = prevention_data.get("permanent_actions", [])
            systemic_prevention = prevention_data.get("systemic_prevention", [])
            lessons_learned = prevention_data.get("lessons_learned", [])
            kb_updates = prevention_data.get("knowledge_base_updates", [])
            follow_up = prevention_data.get("follow_up_items", [])

            # Build facts (concrete actions)
            facts = []
            for action in permanent_actions:
                facts.append(f"D5: {action.get('action', 'N/A')} - {action.get('rationale', 'N/A')}")

            for prevention in systemic_prevention:
                facts.append(f"D7: {prevention.get('change', 'N/A')} (scope: {prevention.get('scope', 'N/A')})")

            # Build hypotheses (expected benefits, risks)
            hypotheses = []
            for prevention in systemic_prevention:
                if prevention.get('benefits'):
                    hypotheses.append(f"Expected benefit: {prevention['benefits']}")
                if prevention.get('risks'):
                    hypotheses.append(f"Potential risk: {prevention['risks']}")

            # Map to 8D phases
            eight_d_phases = {
                "D5_permanent_corrective_action": permanent_actions,
                "D7_prevent_recurrence": systemic_prevention,
                "D8_recognize_team": {
                    "lessons_learned": lessons_learned,
                    "knowledge_base_updates": kb_updates,
                    "follow_up_items": follow_up
                }
            }

            return AgentOutput(
                agent_type=self.agent_type,
                content=json.dumps(prevention_data, indent=2),
                facts=facts,
                hypotheses=hypotheses,
                eight_d_phases=eight_d_phases,
                cost_usd=0.0  # Will be updated by caller
            )

        except json.JSONDecodeError as e:
            # Fallback: treat as unstructured text
            return AgentOutput(
                agent_type=self.agent_type,
                content=response,
                facts=[f"Prevention plan generated (JSON parse failed: {str(e)})"],
                hypotheses=[],
                eight_d_phases={},
                cost_usd=0.0
            )

    def get_max_tokens(self) -> int:
        """Return token budget for prevention planning"""
        return 4000  # Moderate budget for structured prevention plan
```

#### 2. Agent Exports
**File**: `src/atlassemi/agents/__init__.py`
**Changes**: Add PreventionAgent to exports

```python
"""ATLASsemi Agents"""

from .base import (
    BaseAgent,
    AgentInput,
    AgentOutput,
    ProblemMode,
    SecurityTier,
    TaskType,
)
from .narrative_agent import NarrativeAgent
from .clarification_agent import ClarificationAgent
from .analysis_agent import AnalysisAgent
from .prevention_agent import PreventionAgent  # ADD THIS

__all__ = [
    "BaseAgent",
    "AgentInput",
    "AgentOutput",
    "ProblemMode",
    "SecurityTier",
    "TaskType",
    "NarrativeAgent",
    "ClarificationAgent",
    "AnalysisAgent",
    "PreventionAgent",  # ADD THIS
]
```

### Success Criteria:

#### Automated Verification:
- [ ] File `src/atlassemi/agents/prevention_agent.py` exists
- [ ] PreventionAgent exports from `__init__.py`
- [ ] Python syntax is valid: `python -m py_compile src/atlassemi/agents/prevention_agent.py`
- [ ] No import errors: `python -c "from atlassemi.agents import PreventionAgent; print('OK')"`
- [ ] Type hints are present (manual check)

#### Manual Verification:
- [ ] Review prompt generation logic for completeness
- [ ] Verify JSON output structure matches expected schema
- [ ] Check mode-specific guidance is appropriate
- [ ] Ensure 8D phase mapping is correct (D5, D7, D8)

## Phase 2: CLI Integration

### Overview
Add Prevention Agent to CLI workflow for manual testing.

### Changes Required:

#### 1. CLI Updates
**File**: `cli.py`
**Changes**: Add Prevention Agent execution option

```python
# Around line 7, add import
from atlassemi.agents import (
    NarrativeAgent,
    ClarificationAgent,
    AnalysisAgent,
    PreventionAgent,  # ADD THIS
)

# After analysis_agent execution (around line 130), add:

print("\n" + "="*80)
print("PHASE 3: PREVENTION AND LESSONS LEARNED")
print("="*80)

# Execute Prevention Agent
prevention_agent = PreventionAgent(model_router=model_router)

prevention_input = AgentInput(
    mode=mode,
    security_tier=security_tier,
    context={
        "analysis": analysis_output.eight_d_phases,
        "root_causes": analysis_output.eight_d_phases.get("D4_root_cause_analysis", []),
        "narrative": narrative_output.content,
    }
)

print("\nExecuting Prevention Agent...")
prevention_output = prevention_agent.execute(prevention_input)

print("\n--- Prevention Plan ---")
print(prevention_output.content)
print(f"\nPhase 3 Cost: ${prevention_output.cost_usd:.4f}")
```

### Success Criteria:

#### Automated Verification:
- [ ] CLI runs without errors: `python cli.py` (with test input)
- [ ] Prevention Agent executes in workflow
- [ ] Cost tracking includes Phase 3

#### Manual Verification:
- [ ] CLI displays prevention plan output
- [ ] JSON output is formatted correctly
- [ ] Cost is displayed properly
- [ ] Full workflow (Phases 0-3) completes successfully

## Phase 3: Documentation Updates

### Overview
Update project documentation to reflect Prevention Agent completion.

### Changes Required:

#### 1. Development Status
**File**: `DEVELOPMENT_STATUS.md`
**Changes**: Update status to show Phase 3 complete

```markdown
# Line 80 - Update status
#### Phase 3: Prevention Agent ✅  # Change from 🚧
- **Purpose:** Document lessons learned and prevention plans
- **Features:**
  - Permanent corrective actions (D5)
  - Systemic prevention recommendations (D7)
  - Lessons learned documentation (D8)
  - JSON-structured prevention plan
- **Output:** Complete prevention and documentation plan
```

#### 2. CLAUDE.md
**File**: `CLAUDE.md`
**Changes**: Update agent list

```markdown
# Around line 70 - Update agent list
   ├── agents/              # Phase 0-3 agents
   │   ├── base.py          # Base agent class
   │   ├── narrative_agent.py
   │   ├── clarification_agent.py
   │   ├── analysis_agent.py
   │   └── prevention_agent.py  # ADD THIS
```

### Success Criteria:

#### Automated Verification:
- [ ] Documentation files exist and are valid markdown
- [ ] No broken links in documentation

#### Manual Verification:
- [ ] Documentation accurately reflects implementation
- [ ] Examples are clear and correct
- [ ] Status updates are complete

## Testing Strategy

### Manual Testing (Phase 1-2):

1. **Test with Mock LLM:**
   ```bash
   cd C:\src\Synterra\ATLASsemi
   python cli.py
   # Select mode 1 (Excursion)
   # Select tier 1 (General LLM)
   # Enter test narrative
   # Verify Phases 0-3 complete
   ```

2. **Test with Real Claude API:**
   ```bash
   set ANTHROPIC_API_KEY=your-key
   set ATLASSEMI_RUNTIME_MODE=dev
   python cli.py
   # Enter real problem narrative
   # Verify prevention plan is sensible
   # Check cost tracking
   ```

3. **Test JSON Parsing:**
   - Verify prevention plan has all expected fields
   - Check that malformed JSON falls back gracefully
   - Verify 8D phase mapping is correct

4. **Test Mode-Specific Behavior:**
   - Run with excursion mode - verify focus on containment
   - Run with improvement mode - verify focus on sustainability
   - Run with operations mode - verify focus on workflow

### Edge Cases:
- Empty analysis input
- Missing root causes
- Very long analysis (token limits)
- Non-JSON LLM response

## Performance Considerations

- Token budget: 4000 tokens (moderate, similar to Clarification Agent)
- Expected cost: ~$0.02-0.03 per prevention plan (dev mode)
- No performance bottlenecks expected

## Migration Notes

N/A - This is a new agent, no migration needed.

## References

- Handoff document: `thoughts/shared/handoffs/atlassemi-initial-setup-handoff.md`
- Development status: `DEVELOPMENT_STATUS.md`
- Existing agents:
  - `src/atlassemi/agents/narrative_agent.py` (Phase 0 example)
  - `src/atlassemi/agents/clarification_agent.py` (Phase 1 example)
  - `src/atlassemi/agents/analysis_agent.py` (Phase 2 example)
- Base agent: `src/atlassemi/agents/base.py`
- 8D Methodology: Standard problem-solving framework (D0-D8)

## Implementation Notes

- Follow established patterns from existing agents
- Use same error handling approach
- Maintain mode-aware prompting style
- Keep JSON output structure consistent
- Document all public methods with docstrings

## Success Indicators

**Phase 3 agent is complete when:**
1. ✅ File created and exports correctly
2. ✅ Executes successfully with mock LLM
3. ✅ Executes successfully with real Claude API
4. ✅ JSON output structure is correct
5. ✅ Mode-specific behavior works
6. ✅ Cost tracking is accurate
7. ✅ CLI integration works
8. ✅ Documentation is updated

**Ready for next step (Orchestrator) when:**
- All 4 agents (Phases 0-3) work independently
- Each agent can be called programmatically
- Cost tracking works across all agents
- JSON parsing is reliable
