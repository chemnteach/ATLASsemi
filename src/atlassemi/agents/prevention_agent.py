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

            # 8D phases addressed in prevention phase
            eight_d_phases_addressed = ["D5", "D7", "D8"]

            return AgentOutput(
                agent_type=self.agent_type,
                content=json.dumps(prevention_data, indent=2),
                metadata={
                    "permanent_actions": permanent_actions,
                    "systemic_prevention": systemic_prevention,
                    "lessons_learned": lessons_learned,
                    "knowledge_base_updates": kb_updates,
                    "follow_up_items": follow_up
                },
                eight_d_phases_addressed=eight_d_phases_addressed,
                facts=facts,
                hypotheses=hypotheses,
                cost_usd=0.0  # Will be updated by caller
            )

        except json.JSONDecodeError as e:
            # Fallback: treat as unstructured text
            return AgentOutput(
                agent_type=self.agent_type,
                content=response,
                metadata={"parse_error": str(e)},
                eight_d_phases_addressed=["D5", "D7", "D8"],
                facts=[f"Prevention plan generated (JSON parse failed: {str(e)})"],
                hypotheses=[],
                cost_usd=0.0
            )

    def get_max_tokens(self) -> int:
        """Return token budget for prevention planning"""
        return 4000  # Moderate budget for structured prevention plan
