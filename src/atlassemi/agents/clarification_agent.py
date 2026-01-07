"""
Clarification Agent - Phase 1: Adaptive Clarification

Asks context-appropriate questions to stabilize scope and terminology.
Mode-aware: different questions for excursion vs improvement vs operations.
"""

from typing import Dict, Any, List
from dataclasses import dataclass

from .base import BaseAgent, AgentInput, AgentOutput, ProblemMode


@dataclass
class ClarificationSet:
    """Set of clarification questions and answers."""

    questions: List[str]
    answers: List[str]
    remaining_ambiguities: List[str]
    scope_summary: str


class ClarificationAgent(BaseAgent):
    """
    Phase 1: Adaptive Clarification Agent

    Purpose:
    - Ask mode-appropriate questions
    - Stabilize scope and terminology
    - Identify data sources and confidence
    - Prepare for 8D structured analysis

    Mode-Aware Questions:
    - Excursion: When? Where? What's normal? What changed?
    - Improvement: How long? How widespread? What's variability?
    - Operations: What's blocking? What's urgent? Impact?
    """

    def __init__(self, model_router=None):
        super().__init__(agent_type="clarification", model_router=model_router)

    def generate_prompt(self, agent_input: AgentInput) -> str:
        """
        Generate clarification questions prompt.

        Args:
            agent_input: Contains narrative analysis

        Returns:
            Prompt for LLM to generate questions
        """
        mode = agent_input.mode
        narrative_analysis = agent_input.context.get('narrative_analysis', {})

        # Get observations and hypotheses from narrative
        observations = narrative_analysis.get('observations', [])
        suspected_causes = narrative_analysis.get('suspected_causes', [])
        data_sources = narrative_analysis.get('data_sources_mentioned', [])

        # Mode-specific question templates
        mode_templates = self._get_mode_templates(mode)

        prompt = f"""You are helping clarify a semiconductor fab problem.

**Problem Mode:** {mode.value}

**What we know so far:**

Observations:
{self._format_list(observations)}

Suspected Causes:
{self._format_list(suspected_causes)}

Data Sources Mentioned:
{self._format_list(data_sources)}

**Your Task:**

Generate 5-10 clarification questions tailored to the **{mode.value}** problem mode.

{mode_templates}

**Key Questions to Ask:**

1. **Scope Questions:**
   - When did this surface? (timeline)
   - Where is this happening? (tools, lots, products)
   - How widespread? (isolated vs systemic)

2. **Baseline Questions:**
   - What does "normal" look like?
   - What looks different now?
   - Has this happened before?

3. **Data Questions:**
   - What data is trusted vs uncertain?
   - What measurements are available?
   - What's the confidence level?

4. **Context Questions:**
   - Recent changes? (recipe, tool PM, material lot)
   - Production impact? (WIP at risk, urgency)
   - Constraints? (time, access, resources)

**Output Format:**

Generate a JSON response with:
{{
  "questions": [
    "Question 1",
    "Question 2",
    ...
  ],
  "rationale": "Why these questions matter for {mode.value} mode"
}}

Make questions specific and actionable. Avoid generic questions.
"""

        return prompt

    def _get_mode_templates(self, mode: ProblemMode) -> str:
        """Get mode-specific question templates."""

        if mode == ProblemMode.EXCURSION:
            return """**Excursion Mode Focus:**
- WHEN did the excursion trigger? (exact timeline)
- WHERE is it localized? (tool, chamber, product, lot)
- WHAT was normal baseline? (SPC limits, Cpk)
- WHAT changed? (recipe, material, tool state)
- CONTAINMENT: What lots are at risk?
- URGENCY: Production impact?"""

        elif mode == ProblemMode.IMPROVEMENT:
            return """**Improvement Mode Focus:**
- HOW LONG has this been an issue? (chronic pattern)
- HOW WIDESPREAD? (across tools, products, time)
- WHAT'S THE VARIABILITY? (tool-to-tool, lot-to-lot)
- ROOT CAUSES: What's been tried? What didn't work?
- BASELINE: What's current capability? (Cp, Cpk)
- GOAL: What's target improvement?"""

        elif mode == ProblemMode.OPERATIONS:
            return """**Operations Mode Focus:**
- WHAT'S BLOCKING? (tool down, queue time, dispatch issue)
- WHAT'S URGENT? (customer commit, capacity constraint)
- IMPACT: How many lots affected? Revenue risk?
- WORKAROUNDS: What temporary solutions exist?
- ROOT CAUSE: Recurring issue or one-time?
- PREVENTION: How to avoid next time?"""

        return ""

    def _format_list(self, items: List[str]) -> str:
        """Format list for prompt."""
        if not items:
            return "- (None provided)"
        return "\n".join([f"- {item}" for item in items])

    def process_response(
        self,
        response: str,
        agent_input: AgentInput
    ) -> AgentOutput:
        """
        Process LLM response into clarification questions.

        Args:
            response: JSON response from LLM
            agent_input: Original input

        Returns:
            AgentOutput with questions
        """
        import json

        try:
            response_dict = json.loads(response)
            questions = response_dict.get("questions", [])
            rationale = response_dict.get("rationale", "")
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            questions = [
                "When did you first notice this issue?",
                "Which tools or processes are affected?",
                "What does normal operation look like for comparison?",
                "What data sources are available to investigate?"
            ]
            rationale = "Default questions (JSON parsing failed)"

        # Format output
        content = self._format_questions(questions, rationale)

        # 8D phase: D1 (team) and D2 (problem definition)
        eight_d_phases = ["D1", "D2"]

        return AgentOutput(
            agent_type=self.agent_type,
            content=content,
            metadata={
                "questions": questions,
                "rationale": rationale,
                "mode": agent_input.mode.value
            },
            eight_d_phases_addressed=eight_d_phases,
            facts=[],  # No new facts yet - waiting for answers
            hypotheses=[],
            open_questions=questions,
            cost_usd=0.0  # Will be updated by caller
        )

    def _format_questions(self, questions: List[str], rationale: str) -> str:
        """Format questions for display."""

        lines = [
            "# Clarification Questions (Phase 1)",
            "",
            f"**Rationale:** {rationale}",
            "",
            "## Questions",
            ""
        ]

        for i, question in enumerate(questions, 1):
            lines.append(f"{i}. {question}")

        lines.extend([
            "",
            "---",
            "",
            "Please answer these questions to help refine the problem scope."
        ])

        return "\n".join(lines)

    def get_max_tokens(self) -> int:
        """Clarification questions need moderate token budget."""
        return 2000


def process_clarification_answers(
    questions: List[str],
    answers: List[str]
) -> Dict[str, Any]:
    """
    Process user answers to clarification questions.

    Args:
        questions: List of questions asked
        answers: List of user answers

    Returns:
        Dictionary with processed Q&A pairs
    """
    clarifications = {}

    for i, (q, a) in enumerate(zip(questions, answers)):
        clarifications[f"Q{i+1}"] = {
            "question": q,
            "answer": a
        }

    return {
        "clarifications": clarifications,
        "count": len(questions)
    }
