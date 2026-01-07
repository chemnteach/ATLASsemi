"""
Narrative Agent - Phase 0: Narrative-First Intake

Handles the initial free-form problem description from engineers.
Does not interrupt, reframe, or demand precision - just listens and extracts.
"""

from typing import Dict, Any, List
from dataclasses import dataclass

from .base import BaseAgent, AgentInput, AgentOutput


@dataclass
class NarrativeAnalysis:
    """Analysis of user's narrative."""

    # Core extraction
    observations: List[str]  # What they saw (facts)
    interpretations: List[str]  # What they think it means (theories)

    # Context
    constraints: List[str]  # Time pressure, production impact, etc.
    urgency_signals: List[str]  # Why this matters now
    data_sources_mentioned: List[str]  # SPC, FDC, metrology, etc.

    # Initial hypotheses (even if wrong)
    suspected_causes: List[str]

    # Reflection for user validation
    reflection: str


class NarrativeAgent(BaseAgent):
    """
    Phase 0: Narrative-First Intake Agent

    Purpose:
    - Receive free-form problem description
    - Extract observations vs interpretations
    - Identify constraints and urgency
    - Reflect back for validation

    Rules:
    - Do NOT interrupt
    - Do NOT demand precision
    - Do NOT introduce 8D terminology yet
    - Accept ambiguity and incompleteness
    """

    def __init__(self, model_router=None):
        super().__init__(agent_type="narrative", model_router=model_router)

    def generate_intake_prompt(self) -> str:
        """
        Generate the initial intake prompt.

        This is what the user sees first.

        Returns:
            Intake prompt string
        """
        return """Before we get structured, please describe the situation in your own words.

Just tell me what's going on — what you're seeing, what's worrying you,
any constraints you're under, and what prompted you to look into this now.

Bullet points or stream-of-consciousness are both fine."""

    def generate_prompt(self, agent_input: AgentInput) -> str:
        """
        Generate prompt for extracting narrative analysis.

        Args:
            agent_input: Contains the user's narrative

        Returns:
            Prompt for LLM to analyze narrative
        """
        narrative = agent_input.context.get('narrative', '')

        prompt = f"""You are analyzing a semiconductor fab engineer's problem description.

Your job is to extract structured information WITHOUT demanding precision or interrupting their flow.

**User's Narrative:**
{narrative}

**Extract the following:**

1. **Observations** (facts they saw):
   - What did they observe? (SPC alerts, defects, tool behavior, etc.)
   - Separate what they SAW from what they THINK

2. **Interpretations** (their theories):
   - What do they think is happening?
   - What are they suspecting? (even if it might be wrong)

3. **Constraints** (what's limiting them):
   - Time pressure?
   - Production impact?
   - Tool availability?
   - Data access limitations?

4. **Urgency Signals** (why this matters now):
   - What prompted them to escalate?
   - What's at risk?

5. **Data Sources Mentioned**:
   - SPC charts, FDC data, metrology, defect inspection, etc.

6. **Suspected Causes** (their current hypotheses):
   - What do they think might be the root cause?

Then generate a brief **reflection** that summarizes what you heard.
This reflection should be neutral and confirming, like:
"Here's what I heard — tell me if this is accurate."

Format your response as JSON:
{{
  "observations": [...],
  "interpretations": [...],
  "constraints": [...],
  "urgency_signals": [...],
  "data_sources_mentioned": [...],
  "suspected_causes": [...],
  "reflection": "..."
}}

Remember: Accept ambiguity. Don't demand precision. Capture their mental model as-is."""

        return prompt

    def process_response(
        self,
        response: str,
        agent_input: AgentInput
    ) -> AgentOutput:
        """
        Process LLM response into NarrativeAnalysis.

        Args:
            response: JSON response from LLM
            agent_input: Original input

        Returns:
            AgentOutput with narrative analysis
        """
        import json

        try:
            analysis_dict = json.loads(response)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            analysis_dict = {
                "observations": ["Unable to parse narrative"],
                "interpretations": [],
                "constraints": [],
                "urgency_signals": [],
                "data_sources_mentioned": [],
                "suspected_causes": [],
                "reflection": response
            }

        # Create NarrativeAnalysis
        analysis = NarrativeAnalysis(
            observations=analysis_dict.get("observations", []),
            interpretations=analysis_dict.get("interpretations", []),
            constraints=analysis_dict.get("constraints", []),
            urgency_signals=analysis_dict.get("urgency_signals", []),
            data_sources_mentioned=analysis_dict.get("data_sources_mentioned", []),
            suspected_causes=analysis_dict.get("suspected_causes", []),
            reflection=analysis_dict.get("reflection", "")
        )

        # Format for output
        content = self._format_analysis(analysis)

        # Extract 8D phases (narrative intake is D0-D1)
        eight_d_phases = ["D0"]  # Preparation phase

        return AgentOutput(
            agent_type=self.agent_type,
            content=content,
            metadata={
                "analysis": analysis,
                "narrative": agent_input.context.get('narrative', '')
            },
            eight_d_phases_addressed=eight_d_phases,
            facts=analysis.observations,
            hypotheses=analysis.suspected_causes,
            open_questions=[],  # Will be determined in clarification phase
            cost_usd=0.0,  # TODO: Track actual cost
            quality_metrics={}
        )

    def _format_analysis(self, analysis: NarrativeAnalysis) -> str:
        """
        Format narrative analysis for display.

        Args:
            analysis: NarrativeAnalysis object

        Returns:
            Formatted markdown string
        """
        lines = ["# Narrative Analysis (Phase 0)", ""]

        if analysis.observations:
            lines.append("## Observations (Facts)")
            for obs in analysis.observations:
                lines.append(f"- {obs}")
            lines.append("")

        if analysis.interpretations:
            lines.append("## Interpretations (Their Theory)")
            for interp in analysis.interpretations:
                lines.append(f"- {interp}")
            lines.append("")

        if analysis.constraints:
            lines.append("## Constraints")
            for constraint in analysis.constraints:
                lines.append(f"- {constraint}")
            lines.append("")

        if analysis.urgency_signals:
            lines.append("## Urgency Signals")
            for signal in analysis.urgency_signals:
                lines.append(f"- {signal}")
            lines.append("")

        if analysis.data_sources_mentioned:
            lines.append("## Data Sources Mentioned")
            for source in analysis.data_sources_mentioned:
                lines.append(f"- {source}")
            lines.append("")

        if analysis.suspected_causes:
            lines.append("## Suspected Causes (To Validate)")
            for cause in analysis.suspected_causes:
                lines.append(f"- {cause}")
            lines.append("")

        lines.append("## Reflection")
        lines.append("")
        lines.append(analysis.reflection)

        return "\n".join(lines)

    def get_max_tokens(self) -> int:
        """Narrative analysis needs moderate token budget."""
        return 2000
