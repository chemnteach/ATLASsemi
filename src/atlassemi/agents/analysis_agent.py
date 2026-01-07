"""
Analysis Agent - Phase 2: Structured 8D Analysis

Maps problem to 8D methodology and performs structured analysis
with LLM + knowledge graph integration.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from .base import BaseAgent, AgentInput, AgentOutput, ProblemMode


@dataclass
class EightDPhaseAnalysis:
    """Analysis for a single 8D phase."""

    phase: str  # D0-D8
    title: str
    findings: List[str]
    recommendations: List[str]
    confidence: str  # "high", "medium", "low"
    data_sources: List[str]


@dataclass
class EightDReport:
    """Complete 8D analysis report."""

    phases: List[EightDPhaseAnalysis] = field(default_factory=list)
    facts: List[str] = field(default_factory=list)
    hypotheses: List[str] = field(default_factory=list)
    gaps: List[str] = field(default_factory=list)  # What's missing
    next_steps: List[str] = field(default_factory=list)


class AnalysisAgent(BaseAgent):
    """
    Phase 2: Structured 8D Analysis Agent

    Purpose:
    - Map problem to 8D methodology (D0-D8)
    - Separate facts from hypotheses
    - Query knowledge graph for similar cases
    - Generate structured analysis report

    8D Phases:
    - D0: Preparation (problem detection, team formation trigger)
    - D1: Team (who should be involved - recommend expertise)
    - D2: Problem Definition (scope, timeline, impact)
    - D3: Interim Containment (stop the bleeding now)
    - D4: Root Cause Analysis (why did this happen)
    - D5: Permanent Corrective Actions (fix the root cause)
    - D6: Validation (prove the fix works)
    - D7: Prevention (how to avoid this systemically)
    - D8: Lessons Learned (document and share)
    """

    def __init__(self, model_router=None):
        super().__init__(agent_type="analysis", model_router=model_router)

    def generate_prompt(self, agent_input: AgentInput) -> str:
        """
        Generate 8D analysis prompt.

        Args:
            agent_input: Contains narrative + clarifications

        Returns:
            Prompt for comprehensive 8D analysis
        """
        mode = agent_input.mode
        narrative = agent_input.context.get('narrative', '')
        narrative_analysis = agent_input.context.get('narrative_analysis', {})
        clarifications = agent_input.context.get('clarifications', {})

        # Extract context
        observations = narrative_analysis.get('observations', [])
        suspected_causes = narrative_analysis.get('suspected_causes', [])
        constraints = narrative_analysis.get('constraints', [])

        prompt = f"""You are a semiconductor fab problem-solving expert conducting an 8D analysis.

**Problem Mode:** {mode.value}

**User Narrative:**
{narrative}

**Observations (Facts):**
{self._format_list(observations)}

**Suspected Causes (Hypotheses to validate):**
{self._format_list(suspected_causes)}

**Constraints:**
{self._format_list(constraints)}

**Clarifications:**
{self._format_clarifications(clarifications)}

**Your Task:**

Conduct a structured 8D (Eight Disciplines) analysis of this problem.

For each applicable 8D phase, provide:
1. **Findings** - What we know
2. **Recommendations** - What to do
3. **Confidence** - High/Medium/Low based on data
4. **Data Sources** - What's needed to validate

**8D Phases to Address:**

**D0: Preparation**
- How was this detected? (SPC alert, defect inspection, customer complaint)
- What triggered the investigation?
- Urgency assessment

**D1: Team**
- Who should be involved? (process engineer, equipment engineer, yield, quality)
- What expertise is needed?
- Who owns which parts of the investigation?

**D2: Problem Definition**
- WHAT is the problem? (specific symptom)
- WHERE is it occurring? (tool, chamber, product, step)
- WHEN did it start? (timeline, first occurrence)
- HOW BIG is it? (magnitude, impact, scope)
- IS vs IS NOT analysis

**D3: Interim Containment Actions**
- What can we do NOW to stop the bleeding?
- Lot holds? Tool holds? Rework?
- How to prevent more defects before root cause is found?

**D4: Root Cause Analysis**
- Why did this happen? (5 Whys, fishbone)
- Potential root causes (ranked by likelihood)
- Data needed to validate each hypothesis
- What experiments or analyses to run?

**D5: Permanent Corrective Actions** (if root cause is clear)
- How to fix the root cause permanently?
- Recipe changes? Tool fixes? Process improvements?
- Implementation plan

**D6: Validation** (if corrective action is proposed)
- How to prove the fix works?
- Test plan, acceptance criteria
- Monitoring plan

**D7: Prevention**
- How to prevent this systemically?
- SOP updates? Preventive maintenance? Automated checks?
- Process control improvements

**D8: Lessons Learned**
- What should be documented?
- What should be shared with the team?
- Knowledge base updates

**Important Guidelines:**
- Separate FACTS (what we know for sure) from HYPOTHESES (what we suspect)
- Be explicit about confidence levels (high/medium/low)
- Identify gaps (what data is missing)
- Be practical - not all phases may apply yet

**Output Format:**

Return JSON:
{{
  "phases": [
    {{
      "phase": "D0",
      "title": "Preparation",
      "findings": [...],
      "recommendations": [...],
      "confidence": "high|medium|low",
      "data_sources": [...]
    }},
    ...
  ],
  "facts": [...],  // Confirmed facts only
  "hypotheses": [...],  // Unconfirmed theories
  "gaps": [...],  // Missing information
  "next_steps": [...]  // Immediate actions
}}
"""

        return prompt

    def _format_list(self, items: List[str]) -> str:
        """Format list for prompt."""
        if not items:
            return "- (None provided)"
        return "\n".join([f"- {item}" for item in items])

    def _format_clarifications(self, clarifications: Dict[str, Any]) -> str:
        """Format clarifications for prompt."""
        if not clarifications:
            return "(None provided)"

        lines = []
        for key, qa in clarifications.get('clarifications', {}).items():
            q = qa.get('question', '')
            a = qa.get('answer', '')
            lines.append(f"**Q:** {q}")
            lines.append(f"**A:** {a}")
            lines.append("")

        return "\n".join(lines) if lines else "(None provided)"

    def process_response(
        self,
        response: str,
        agent_input: AgentInput
    ) -> AgentOutput:
        """
        Process LLM response into 8D report.

        Args:
            response: JSON response from LLM
            agent_input: Original input

        Returns:
            AgentOutput with 8D analysis
        """
        import json

        try:
            report_dict = json.loads(response)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            report_dict = {
                "phases": [],
                "facts": ["Unable to parse 8D analysis"],
                "hypotheses": [],
                "gaps": ["JSON parsing failed"],
                "next_steps": ["Re-run analysis"]
            }

        # Create 8D report
        report = EightDReport()

        # Parse phases
        for phase_dict in report_dict.get("phases", []):
            phase_analysis = EightDPhaseAnalysis(
                phase=phase_dict.get("phase", ""),
                title=phase_dict.get("title", ""),
                findings=phase_dict.get("findings", []),
                recommendations=phase_dict.get("recommendations", []),
                confidence=phase_dict.get("confidence", "low"),
                data_sources=phase_dict.get("data_sources", [])
            )
            report.phases.append(phase_analysis)

        # Extract summary lists
        report.facts = report_dict.get("facts", [])
        report.hypotheses = report_dict.get("hypotheses", [])
        report.gaps = report_dict.get("gaps", [])
        report.next_steps = report_dict.get("next_steps", [])

        # Format for output
        content = self._format_report(report)

        # Get 8D phases addressed
        eight_d_phases = [p.phase for p in report.phases]

        return AgentOutput(
            agent_type=self.agent_type,
            content=content,
            metadata={
                "report": report,
                "mode": agent_input.mode.value
            },
            eight_d_phases_addressed=eight_d_phases,
            facts=report.facts,
            hypotheses=report.hypotheses,
            open_questions=report.gaps,
            cost_usd=0.0  # Will be updated by caller
        )

    def _format_report(self, report: EightDReport) -> str:
        """Format 8D report for display."""

        lines = [
            "# 8D Analysis Report (Phase 2)",
            "",
            "---",
            ""
        ]

        # Phases
        for phase in report.phases:
            lines.extend([
                f"## {phase.phase}: {phase.title}",
                "",
                f"**Confidence:** {phase.confidence}",
                ""
            ])

            if phase.findings:
                lines.append("**Findings:**")
                for finding in phase.findings:
                    lines.append(f"- {finding}")
                lines.append("")

            if phase.recommendations:
                lines.append("**Recommendations:**")
                for rec in phase.recommendations:
                    lines.append(f"- {rec}")
                lines.append("")

            if phase.data_sources:
                lines.append("**Data Sources:**")
                for ds in phase.data_sources:
                    lines.append(f"- {ds}")
                lines.append("")

            lines.append("---")
            lines.append("")

        # Summary sections
        if report.facts:
            lines.append("## Confirmed Facts")
            lines.append("")
            for fact in report.facts:
                lines.append(f"✓ {fact}")
            lines.append("")

        if report.hypotheses:
            lines.append("## Hypotheses to Validate")
            lines.append("")
            for hyp in report.hypotheses:
                lines.append(f"? {hyp}")
            lines.append("")

        if report.gaps:
            lines.append("## Information Gaps")
            lines.append("")
            for gap in report.gaps:
                lines.append(f"⚠ {gap}")
            lines.append("")

        if report.next_steps:
            lines.append("## Recommended Next Steps")
            lines.append("")
            for i, step in enumerate(report.next_steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

        return "\n".join(lines)

    def get_max_tokens(self) -> int:
        """8D analysis needs larger token budget."""
        return 8000
