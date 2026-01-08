"""
Workflow Orchestrator - Chains all 4 agent phases

Phases:
- Phase 0: Narrative (free-form intake)
- Phase 1: Clarification (mode-aware questions)
- Phase 2: Analysis (8D mapping)
- Phase 3: Prevention (lessons learned + corrective actions)
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field

from atlassemi.agents.base import (
    AgentInput,
    AgentOutput,
    ProblemMode,
    SecurityTier
)
from atlassemi.agents import (
    NarrativeAgent,
    ClarificationAgent,
    AnalysisAgent,
    PreventionAgent
)
from atlassemi.config import ModelRouter


@dataclass
class WorkflowResult:
    """Complete workflow execution result."""

    # Phase outputs
    narrative_output: AgentOutput
    # [{question, rationale}, ...]
    clarification_questions: List[Dict[str, str]]
    clarification_answers: Dict[str, str]  # {question: answer}
    analysis_output: AgentOutput
    prevention_output: AgentOutput

    # Summary metrics
    total_cost_usd: float
    phases_completed: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    # Quality metrics
    facts_identified: int = 0
    hypotheses_identified: int = 0
    eight_d_phases_addressed: List[str] = field(default_factory=list)


class WorkflowOrchestrator:
    """
    Orchestrates the full 4-phase 8D problem-solving workflow.

    Responsibilities:
    - Execute each phase in sequence
    - Collect user input for clarification
    - Pass context between phases
    - Accumulate costs and metrics
    - Handle errors gracefully
    """

    def __init__(self, model_router: ModelRouter):
        """
        Initialize orchestrator.

        Args:
            model_router: ModelRouter for tier-aware LLM calls
        """
        self.model_router = model_router

        # Initialize agents
        self.narrative_agent = NarrativeAgent(model_router=model_router)
        self.clarification_agent = ClarificationAgent(
            model_router=model_router
        )
        self.analysis_agent = AnalysisAgent(model_router=model_router)
        self.prevention_agent = PreventionAgent(model_router=model_router)

    def run_workflow(
        self,
        narrative: str,
        mode: ProblemMode,
        tier: SecurityTier,
        answer_collector: Optional[Callable] = None
    ) -> WorkflowResult:
        """
        Execute the full 4-phase workflow.

        Args:
            narrative: User's problem description
            mode: Problem-solving mode (excursion/improvement/operations)
            tier: Security tier (general/confidential/top_secret)
            answer_collector: Function to collect user answers
                (defaults to CLI input)

        Returns:
            WorkflowResult with all phase outputs and metrics
        """
        phases_completed: List[str] = []
        errors: List[str] = []

        # Phase 0: Narrative Analysis
        print("\n" + "=" * 80)
        print("PHASE 0: NARRATIVE ANALYSIS")
        print("=" * 80)

        narrative_output = self._execute_phase_0(narrative, mode, tier)
        phases_completed.append("Phase 0: Narrative")

        # Phase 1: Clarification Questions
        print("\n" + "=" * 80)
        print("PHASE 1: CLARIFICATION")
        print("=" * 80)

        clarification_questions, clarification_answers = self._execute_phase_1(
            narrative_output, mode, tier, answer_collector
        )
        phases_completed.append("Phase 1: Clarification")

        # Phase 2: 8D Analysis
        print("\n" + "=" * 80)
        print("PHASE 2: 8D ANALYSIS")
        print("=" * 80)

        analysis_output = self._execute_phase_2(
            narrative_output, clarification_answers, mode, tier
        )
        phases_completed.append("Phase 2: Analysis")

        # Phase 3: Prevention Planning
        print("\n" + "=" * 80)
        print("PHASE 3: PREVENTION AND LESSONS LEARNED")
        print("=" * 80)

        prevention_output = self._execute_phase_3(
            analysis_output, narrative_output, mode, tier
        )
        phases_completed.append("Phase 3: Prevention")

        # Accumulate metrics
        total_cost = (
            narrative_output.cost_usd +
            analysis_output.cost_usd +
            prevention_output.cost_usd
        )

        facts_count = (
            len(narrative_output.facts) +
            len(analysis_output.facts) +
            len(prevention_output.facts)
        )

        hypotheses_count = (
            len(narrative_output.hypotheses) +
            len(analysis_output.hypotheses) +
            len(prevention_output.hypotheses)
        )

        # Collect all 8D phases addressed
        all_phases = set()
        all_phases.update(narrative_output.eight_d_phases_addressed)
        all_phases.update(analysis_output.eight_d_phases_addressed)
        all_phases.update(prevention_output.eight_d_phases_addressed)

        return WorkflowResult(
            narrative_output=narrative_output,
            clarification_questions=clarification_questions,
            clarification_answers=clarification_answers,
            analysis_output=analysis_output,
            prevention_output=prevention_output,
            total_cost_usd=total_cost,
            phases_completed=phases_completed,
            errors=errors,
            facts_identified=facts_count,
            hypotheses_identified=hypotheses_count,
            eight_d_phases_addressed=sorted(list(all_phases))
        )

    def _execute_phase_0(
        self,
        narrative: str,
        mode: ProblemMode,
        tier: SecurityTier
    ) -> AgentOutput:
        """Execute Phase 0: Narrative Analysis"""
        agent_input = AgentInput(
            mode=mode,
            security_tier=tier,
            context={"narrative": narrative}
        )

        return self.narrative_agent.execute(agent_input)

    def _execute_phase_1(
        self,
        narrative_output: AgentOutput,
        mode: ProblemMode,
        tier: SecurityTier,
        answer_collector: Optional[Callable]
    ) -> tuple[List[Dict[str, str]], Dict[str, str]]:
        """
        Execute Phase 1: Clarification Questions

        Generates mode-aware questions and collects user answers.

        Args:
            narrative_output: Output from Phase 0
            mode: Problem-solving mode
            tier: Security tier
            answer_collector: Function to collect answers
                (None = use default CLI)

        Returns:
            (questions, answers) tuple where:
            - questions: [{question, rationale}, ...]
            - answers: {question: answer, ...}
        """
        # Generate clarification questions
        # Get urgency signals if available
        urgency_signals = []
        analysis_data = narrative_output.metadata.get("analysis", None)
        if analysis_data and hasattr(analysis_data, "urgency_signals"):
            urgency_signals = analysis_data.urgency_signals
        elif isinstance(analysis_data, dict):
            urgency_signals = analysis_data.get("urgency_signals", [])

        agent_input = AgentInput(
            mode=mode,
            security_tier=tier,
            context={
                "narrative": narrative_output.metadata.get("narrative", ""),
                "observations": narrative_output.facts,
                "interpretations": narrative_output.hypotheses,
                "urgency_signals": urgency_signals
            }
        )

        clarification_output = self.clarification_agent.execute(agent_input)

        # Parse questions from output
        import json
        try:
            questions_data = json.loads(clarification_output.content)
            questions = questions_data.get("questions", [])
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            print(
                "Warning: Could not parse clarification questions. "
                "Proceeding without them."
            )
            return [], {}

        # Display questions
        print(f"\n{len(questions)} clarification questions generated:\n")
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q['question']}")
            print(f"   Why this matters: {q['rationale']}\n")

        # Collect answers
        if answer_collector:
            answers = answer_collector(questions)
        else:
            answers = self._default_answer_collector(questions)

        return questions, answers

    def _default_answer_collector(
        self, questions: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """
        Default CLI-based answer collection.

        Args:
            questions: List of question dicts

        Returns:
            Dict mapping questions to answers
        """
        print("\n" + "=" * 80)
        print("Please answer the following questions:")
        print(
            "(Type your answer and press Enter. "
            "Type 'skip' to skip a question.)"
        )
        print("=" * 80 + "\n")

        answers = {}

        for i, q in enumerate(questions, 1):
            print(f"\nQuestion {i}/{len(questions)}:")
            print(f"{q['question']}")
            print(f"(Rationale: {q['rationale']})")
            print()

            answer = input("Your answer: ").strip()

            if answer.lower() != 'skip' and answer:
                answers[q['question']] = answer
            else:
                print("(Skipped)")

        print(f"\n{len(answers)}/{len(questions)} questions answered.\n")

        return answers

    def _execute_phase_2(
        self,
        narrative_output: AgentOutput,
        clarification_answers: Dict[str, str],
        mode: ProblemMode,
        tier: SecurityTier
    ) -> AgentOutput:
        """
        Execute Phase 2: 8D Analysis

        Passes rich context from Phases 0-1.
        """
        # Extract analysis data safely
        analysis_data = narrative_output.metadata.get("analysis", None)
        urgency_signals = []
        constraints = []
        data_sources = []

        if analysis_data:
            if hasattr(analysis_data, "urgency_signals"):
                urgency_signals = analysis_data.urgency_signals
            elif isinstance(analysis_data, dict):
                urgency_signals = analysis_data.get("urgency_signals", [])

            if hasattr(analysis_data, "constraints"):
                constraints = analysis_data.constraints
            elif isinstance(analysis_data, dict):
                constraints = analysis_data.get("constraints", [])

            if hasattr(analysis_data, "data_sources_mentioned"):
                data_sources = analysis_data.data_sources_mentioned
            elif isinstance(analysis_data, dict):
                data_sources = analysis_data.get("data_sources_mentioned", [])

        # Build comprehensive context
        context = {
            "narrative": narrative_output.metadata.get("narrative", ""),
            "observations": narrative_output.facts,
            "interpretations": narrative_output.hypotheses,
            "suspected_causes": narrative_output.hypotheses,
            "clarifications": clarification_answers,
            "urgency_signals": urgency_signals,
            "constraints": constraints,
            "data_sources": data_sources
        }

        agent_input = AgentInput(
            mode=mode,
            security_tier=tier,
            context=context
        )

        return self.analysis_agent.execute(agent_input)

    def _execute_phase_3(
        self,
        analysis_output: AgentOutput,
        narrative_output: AgentOutput,
        mode: ProblemMode,
        tier: SecurityTier
    ) -> AgentOutput:
        """
        Execute Phase 3: Prevention Planning

        Passes rich context from Phase 2 analysis.
        """
        # Extract 8D analysis from metadata
        eight_d_analysis = analysis_output.metadata.get("eight_d_mapping", {})

        # Build comprehensive context
        context = {
            "narrative": narrative_output.metadata.get("narrative", ""),
            "analysis": eight_d_analysis,
            "root_causes": eight_d_analysis.get("D4_root_cause_analysis", []),
            "containment_actions": eight_d_analysis.get("D3_containment", []),
            "problem_definition": eight_d_analysis.get(
                "D2_problem_definition", ""
            ),
            "facts": analysis_output.facts,
            "hypotheses": analysis_output.hypotheses,
            "gaps_identified": eight_d_analysis.get("gaps", [])
        }

        agent_input = AgentInput(
            mode=mode,
            security_tier=tier,
            context=context
        )

        return self.prevention_agent.execute(agent_input)
