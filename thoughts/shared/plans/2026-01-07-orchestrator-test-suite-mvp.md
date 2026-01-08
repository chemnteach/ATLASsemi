# Orchestrator and Test Suite Implementation Plan (MVP v1.0)

## Overview

Implement the Workflow Orchestrator and comprehensive test suite to complete ATLASsemi MVP v1.0 - a production-ready foundation for 8D semiconductor problem-solving. This creates a deployable CLI tool that chains all 4 agent phases automatically with full test coverage, robust error handling, and clear documentation.

## Current State Analysis

**What exists now:**
- ✅ All 4 agents implemented (Narrative, Clarification, Analysis, Prevention)
- ✅ Model router with tier-aware routing (dev/runtime modes)
- ✅ Security tier enforcement (3-tier system)
- ✅ CLI runs Phase 0 (Narrative) and Phase 3 (Prevention) only
- ❌ Phases 1-2 not orchestrated (implemented but not connected)
- ❌ No automated tests (manual testing only)
- ❌ Context passing incomplete between phases

**Key discoveries:**
- `cli.py:line 97-206` - Runs Phase 0, then jumps to Phase 3 with minimal context
- `src/atlassemi/agents/base.py:line 140-178` - Template method pattern works well
- All agents return `AgentOutput` with consistent structure (`base.py:line 46-66`)
- Clarification agent generates questions but has no answer collection mechanism
- Cost tracking works via ModelRouter (`model_router.py`)

**Architecture patterns to follow:**
- Template method pattern from BaseAgent
- JSON-structured outputs with fallback error handling
- Mode-aware prompting (excursion/improvement/operations)
- Fact vs hypothesis separation
- 8D phase tracking

## Desired End State

A production-ready v1.0 release with:

### 1. Workflow Orchestrator
- Chains all 4 phases: Narrative → Clarification → Analysis → Prevention
- Collects user answers for clarification questions
- Passes rich context between phases (not minimal context)
- Accumulates costs across full workflow
- Robust error handling with graceful degradation
- Clear progress indication for users

### 2. Comprehensive Test Suite
- Unit tests for all 4 agents (mock LLM responses)
- Integration tests for full workflow
- Model router and tier enforcer tests
- Edge case coverage (empty inputs, malformed JSON, API errors)
- Error handling scenarios
- Cost tracking verification
- Security tier blocking tests

### 3. Production Quality
- 90%+ test coverage
- Type hints throughout
- Comprehensive docstrings
- Error messages that guide users
- Logging for debugging
- Deployment documentation

### Verification

**Automated:**
- `pytest tests/ -v` - All tests pass
- `pytest --cov=atlassemi --cov-report=html` - 90%+ coverage
- `mypy src/atlassemi/` - No type errors
- `black . && isort . && flake8 .` - Code quality checks pass

**Manual:**
- Run full workflow with test narrative - all 4 phases execute
- Enter answers for clarification questions - accepted correctly
- Prevention plan references analysis from Phase 2
- Cost accumulation shows all 4 phases
- Error in Phase 1 doesn't crash entire workflow

## What We're NOT Doing

**Explicitly out of scope for MVP v1.0:**
- Session persistence / resume capability
- Partial workflow execution (e.g., start at Phase 2)
- Web interface or REST API
- RAG integration (v1.1 enhancement)
- Factory API / On-prem API implementations (v1.2/v1.3)
- Knowledge graph integration
- Real-time progress streaming
- Async/parallel agent execution
- Workflow customization / configuration
- Historical case database

## Implementation Approach

**Phase-by-phase incremental delivery:**
1. **Phase 1**: Core orchestrator structure and basic workflow
2. **Phase 2**: User input collection for clarification Q&A
3. **Phase 3**: Rich context passing between phases
4. **Phase 4**: Unit tests for all agents
5. **Phase 5**: Integration tests and edge cases
6. **Phase 6**: Documentation and deployment guide

**Why this approach:**
- Each phase is independently testable
- Can validate orchestrator logic before full test suite
- Unit tests can be written in parallel with integration
- Documentation captures learnings from testing

---

## Phase 1: Core Orchestrator Structure

### Overview
Create the basic orchestrator that can chain agents sequentially, even with minimal context passing. This establishes the structural foundation.

### Changes Required:

#### 1. Orchestrator Package Init
**File**: `src/atlassemi/orchestrator/__init__.py`
**Changes**: Create new package with exports

```python
"""ATLASsemi Workflow Orchestrator"""

from .workflow import WorkflowOrchestrator, WorkflowResult

__all__ = ["WorkflowOrchestrator", "WorkflowResult"]
```

#### 2. Workflow Orchestrator Core
**File**: `src/atlassemi/orchestrator/workflow.py`
**Changes**: Create orchestrator with basic workflow execution

```python
"""
Workflow Orchestrator - Chains all 4 agent phases

Phases:
- Phase 0: Narrative (free-form intake)
- Phase 1: Clarification (mode-aware questions)
- Phase 2: Analysis (8D mapping)
- Phase 3: Prevention (lessons learned + corrective actions)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

from atlassemi.agents.base import (
    BaseAgent,
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
    clarification_questions: List[Dict[str, str]]  # [{question, rationale}, ...]
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
        self.clarification_agent = ClarificationAgent(model_router=model_router)
        self.analysis_agent = AnalysisAgent(model_router=model_router)
        self.prevention_agent = PreventionAgent(model_router=model_router)

    def run_workflow(
        self,
        narrative: str,
        mode: ProblemMode,
        tier: SecurityTier,
        answer_collector: Optional[callable] = None
    ) -> WorkflowResult:
        """
        Execute the full 4-phase workflow.

        Args:
            narrative: User's problem description
            mode: Problem-solving mode (excursion/improvement/operations)
            tier: Security tier (general/confidential/top_secret)
            answer_collector: Function to collect user answers (defaults to CLI input)

        Returns:
            WorkflowResult with all phase outputs and metrics
        """
        phases_completed = []
        errors = []

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
        answer_collector: Optional[callable]
    ) -> tuple[List[Dict[str, str]], Dict[str, str]]:
        """
        Execute Phase 1: Clarification Questions

        Returns:
            (questions, answers) tuple
        """
        # TODO: Implement in Phase 2
        # For now, return empty questions/answers
        return [], {}

    def _execute_phase_2(
        self,
        narrative_output: AgentOutput,
        clarification_answers: Dict[str, str],
        mode: ProblemMode,
        tier: SecurityTier
    ) -> AgentOutput:
        """Execute Phase 2: 8D Analysis"""
        # TODO: Implement rich context passing in Phase 3
        # For now, minimal context
        agent_input = AgentInput(
            mode=mode,
            security_tier=tier,
            context={
                "narrative": narrative_output.metadata.get("narrative", ""),
                "observations": narrative_output.facts,
                "suspected_causes": narrative_output.hypotheses
            }
        )

        return self.analysis_agent.execute(agent_input)

    def _execute_phase_3(
        self,
        analysis_output: AgentOutput,
        narrative_output: AgentOutput,
        mode: ProblemMode,
        tier: SecurityTier
    ) -> AgentOutput:
        """Execute Phase 3: Prevention Planning"""
        # TODO: Implement rich context passing in Phase 3
        # For now, minimal context
        agent_input = AgentInput(
            mode=mode,
            security_tier=tier,
            context={
                "analysis": analysis_output.metadata,
                "root_causes": analysis_output.hypotheses,
                "narrative": narrative_output.metadata.get("narrative", "")
            }
        )

        return self.prevention_agent.execute(agent_input)
```

### Success Criteria:

#### Automated Verification:
- [ ] Orchestrator package imports: `python -c "from atlassemi.orchestrator import WorkflowOrchestrator; print('OK')"`
- [ ] Python syntax valid: `python -m py_compile src/atlassemi/orchestrator/workflow.py`
- [ ] Type hints valid: `mypy src/atlassemi/orchestrator/`
- [ ] Linting passes: `flake8 src/atlassemi/orchestrator/`

#### Manual Verification:
- [ ] Can instantiate WorkflowOrchestrator with ModelRouter
- [ ] `run_workflow()` executes without crashing
- [ ] WorkflowResult contains all expected fields
- [ ] Phases execute in correct order (0→1→2→3)

**Implementation Note**: After completing automated verification, manually test that the orchestrator can be instantiated and runs without errors before proceeding to Phase 2.

---

## Phase 2: Clarification Q&A Collection

### Overview
Implement the clarification question generation and user answer collection mechanism.

### Changes Required:

#### 1. Update Orchestrator - Phase 1 Implementation
**File**: `src/atlassemi/orchestrator/workflow.py`
**Changes**: Implement `_execute_phase_1()` method

```python
def _execute_phase_1(
    self,
    narrative_output: AgentOutput,
    mode: ProblemMode,
    tier: SecurityTier,
    answer_collector: Optional[callable]
) -> tuple[List[Dict[str, str]], Dict[str, str]]:
    """
    Execute Phase 1: Clarification Questions

    Generates mode-aware questions and collects user answers.

    Args:
        narrative_output: Output from Phase 0
        mode: Problem-solving mode
        tier: Security tier
        answer_collector: Function to collect answers (None = use default CLI)

    Returns:
        (questions, answers) tuple where:
        - questions: [{question, rationale}, ...]
        - answers: {question: answer, ...}
    """
    # Generate clarification questions
    agent_input = AgentInput(
        mode=mode,
        security_tier=tier,
        context={
            "narrative": narrative_output.metadata.get("narrative", ""),
            "observations": narrative_output.facts,
            "interpretations": narrative_output.hypotheses,
            "urgency_signals": narrative_output.metadata.get("analysis", {}).get("urgency_signals", [])
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
        print("Warning: Could not parse clarification questions. Proceeding without them.")
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

def _default_answer_collector(self, questions: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Default CLI-based answer collection.

    Args:
        questions: List of question dicts

    Returns:
        Dict mapping questions to answers
    """
    print("\n" + "=" * 80)
    print("Please answer the following questions:")
    print("(Type your answer and press Enter. Type 'skip' to skip a question.)")
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
```

### Success Criteria:

#### Automated Verification:
- [ ] Code compiles: `python -m py_compile src/atlassemi/orchestrator/workflow.py`
- [ ] Type checking passes: `mypy src/atlassemi/orchestrator/`
- [ ] No linting errors: `flake8 src/atlassemi/orchestrator/`

#### Manual Verification:
- [ ] Clarification questions are generated and displayed
- [ ] User can enter answers via CLI
- [ ] User can skip questions by typing 'skip'
- [ ] Answers are collected in dictionary format
- [ ] Empty answers are handled gracefully

**Implementation Note**: Test the Q&A flow manually with a test narrative before proceeding to Phase 3.

---

## Phase 3: Rich Context Passing

### Overview
Enhance context passing between phases so each agent receives comprehensive information from previous phases.

### Changes Required:

#### 1. Update Phase 2 Context Passing
**File**: `src/atlassemi/orchestrator/workflow.py`
**Changes**: Enhance `_execute_phase_2()` with rich context

```python
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
    # Build comprehensive context
    context = {
        "narrative": narrative_output.metadata.get("narrative", ""),
        "observations": narrative_output.facts,
        "interpretations": narrative_output.hypotheses,
        "suspected_causes": narrative_output.hypotheses,
        "clarifications": clarification_answers,
        "urgency_signals": narrative_output.metadata.get("analysis", {}).get("urgency_signals", []),
        "constraints": narrative_output.metadata.get("analysis", {}).get("constraints", []),
        "data_sources": narrative_output.metadata.get("analysis", {}).get("data_sources_mentioned", [])
    }

    agent_input = AgentInput(
        mode=mode,
        security_tier=tier,
        context=context
    )

    return self.analysis_agent.execute(agent_input)
```

#### 2. Update Phase 3 Context Passing
**File**: `src/atlassemi/orchestrator/workflow.py`
**Changes**: Enhance `_execute_phase_3()` with rich context

```python
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
        "problem_definition": eight_d_analysis.get("D2_problem_definition", ""),
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
```

### Success Criteria:

#### Automated Verification:
- [ ] Code compiles without errors
- [ ] Type checking passes
- [ ] No linting issues

#### Manual Verification:
- [ ] Phase 2 receives clarification answers in context
- [ ] Phase 3 receives full 8D analysis from Phase 2
- [ ] Prevention plan references specific findings from analysis
- [ ] Context passing doesn't break if optional fields missing

**Implementation Note**: Run full workflow and verify that each phase's output reflects context from previous phases.

---

## Phase 4: Agent Unit Tests

### Overview
Create comprehensive unit tests for all 4 agents with mock LLM responses.

### Changes Required:

#### 1. Narrative Agent Tests
**File**: `tests/test_narrative_agent.py`
**Changes**: Create new file with unit tests

```python
"""Unit tests for Narrative Agent (Phase 0)"""

import pytest
import json
from atlassemi.agents import NarrativeAgent
from atlassemi.agents.base import AgentInput, ProblemMode, SecurityTier


def test_narrative_agent_basic_execution():
    """Test narrative agent executes without model router."""
    agent = NarrativeAgent(model_router=None)

    agent_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={"narrative": "Test problem description"}
    )

    output = agent.execute(agent_input)

    assert output.agent_type == "narrative"
    assert len(output.content) > 0
    assert isinstance(output.facts, list)
    assert isinstance(output.hypotheses, list)


def test_narrative_agent_json_parsing():
    """Test narrative agent parses JSON response correctly."""
    agent = NarrativeAgent(model_router=None)

    # Mock LLM response
    mock_response = json.dumps({
        "observations": ["Yield dropped on Chamber B", "Cpk went from 1.8 to 0.9"],
        "interpretations": ["Maintenance may have caused issue"],
        "constraints": ["Ships Friday", "200 wafers at risk"],
        "urgency_signals": ["Customer critical lot"],
        "data_sources_mentioned": ["SPC charts", "Critical dimension measurements"],
        "suspected_causes": ["PM activity yesterday"],
        "reflection": "Sounds like a post-PM excursion with time pressure"
    })

    agent._call_llm = lambda **kwargs: mock_response

    agent_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={"narrative": "Test problem"}
    )

    output = agent.execute(agent_input)

    assert len(output.facts) == 2
    assert "Yield dropped" in output.facts[0]
    assert len(output.hypotheses) == 1
    assert "PM activity" in output.hypotheses[0]


def test_narrative_agent_malformed_json():
    """Test narrative agent handles malformed JSON gracefully."""
    agent = NarrativeAgent(model_router=None)

    # Mock malformed JSON response
    agent._call_llm = lambda **kwargs: "{ this is not valid JSON }"

    agent_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={"narrative": "Test problem"}
    )

    output = agent.execute(agent_input)

    # Should not crash, should have fallback behavior
    assert output.agent_type == "narrative"
    assert len(output.facts) > 0  # Should have at least fallback fact


def test_narrative_agent_empty_narrative():
    """Test narrative agent handles empty narrative."""
    agent = NarrativeAgent(model_router=None)

    agent_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={"narrative": ""}
    )

    output = agent.execute(agent_input)

    # Should execute without crashing
    assert output.agent_type == "narrative"


def test_narrative_agent_mode_awareness():
    """Test narrative agent prompt varies by mode."""
    agent = NarrativeAgent(model_router=None)

    modes = [ProblemMode.EXCURSION, ProblemMode.IMPROVEMENT, ProblemMode.OPERATIONS]

    for mode in modes:
        agent_input = AgentInput(
            mode=mode,
            security_tier=SecurityTier.GENERAL_LLM,
            context={"narrative": "Test"}
        )

        prompt = agent.generate_prompt(agent_input)
        # Prompt should contain mode-specific information
        assert len(prompt) > 0
```

#### 2. Clarification Agent Tests
**File**: `tests/test_clarification_agent.py`
**Changes**: Create new file with unit tests

```python
"""Unit tests for Clarification Agent (Phase 1)"""

import pytest
import json
from atlassemi.agents import ClarificationAgent
from atlassemi.agents.base import AgentInput, ProblemMode, SecurityTier


def test_clarification_agent_execution():
    """Test clarification agent executes."""
    agent = ClarificationAgent(model_router=None)

    agent_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={
            "narrative": "Test",
            "observations": ["Fact 1"],
            "interpretations": ["Theory 1"]
        }
    )

    output = agent.execute(agent_input)
    assert output.agent_type == "clarification"


def test_clarification_agent_question_parsing():
    """Test clarification agent parses questions correctly."""
    agent = ClarificationAgent(model_router=None)

    mock_response = json.dumps({
        "questions": [
            {"question": "When did the issue start?", "rationale": "Timeline critical"},
            {"question": "What changed recently?", "rationale": "Root cause hunting"}
        ]
    })

    agent._call_llm = lambda **kwargs: mock_response

    agent_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={"narrative": "Test"}
    )

    output = agent.execute(agent_input)

    # Verify questions were parsed
    assert len(output.content) > 0


def test_clarification_agent_mode_specific_questions():
    """Test clarification questions vary by mode."""
    agent = ClarificationAgent(model_router=None)

    excursion_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={"narrative": "Test"}
    )

    improvement_input = AgentInput(
        mode=ProblemMode.IMPROVEMENT,
        security_tier=SecurityTier.GENERAL_LLM,
        context={"narrative": "Test"}
    )

    excursion_prompt = agent.generate_prompt(excursion_input)
    improvement_prompt = agent.generate_prompt(improvement_input)

    # Prompts should be different
    assert excursion_prompt != improvement_prompt
    # Excursion should mention "when" and "what changed"
    assert "when" in excursion_prompt.lower() or "what changed" in excursion_prompt.lower()
```

#### 3. Analysis Agent Tests
**File**: `tests/test_analysis_agent.py`
**Changes**: Create new file with unit tests

```python
"""Unit tests for Analysis Agent (Phase 2)"""

import pytest
import json
from atlassemi.agents import AnalysisAgent
from atlassemi.agents.base import AgentInput, ProblemMode, SecurityTier


def test_analysis_agent_execution():
    """Test analysis agent executes."""
    agent = AnalysisAgent(model_router=None)

    agent_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={
            "narrative": "Test",
            "observations": ["Fact 1"],
            "clarifications": {"Q1": "A1"}
        }
    )

    output = agent.execute(agent_input)
    assert output.agent_type == "analysis"


def test_analysis_agent_eight_d_mapping():
    """Test analysis agent maps to 8D phases."""
    agent = AnalysisAgent(model_router=None)

    mock_response = json.dumps({
        "eight_d_mapping": {
            "D0_preparation": "Triggered by SPC alert",
            "D1_team": "Process Engineering + Maintenance",
            "D2_problem_definition": "Yield drop on Chamber B",
            "D3_containment": ["Hold lot", "Inspect other lots"],
            "D4_root_cause_analysis": ["PM procedure incomplete"],
            "D5_permanent_corrective_action": ["Update PM SOP"],
            "D6_validation": ["Monitor next 100 wafers"],
            "D7_prevent_recurrence": ["Add to PM checklist"],
            "D8_recognize_team": ["Document in knowledge base"]
        },
        "confidence": "medium",
        "gaps": ["Need metrology data"],
        "next_steps": ["Collect more data"]
    })

    agent._call_llm = lambda **kwargs: mock_response

    agent_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={"narrative": "Test"}
    )

    output = agent.execute(agent_input)

    # Should have 8D phases addressed
    assert len(output.eight_d_phases_addressed) > 0
```

#### 4. Prevention Agent Tests
**File**: `tests/test_prevention_agent.py`
**Changes**: Create new file with unit tests

```python
"""Unit tests for Prevention Agent (Phase 3)"""

import pytest
import json
from atlassemi.agents import PreventionAgent
from atlassemi.agents.base import AgentInput, ProblemMode, SecurityTier


def test_prevention_agent_execution():
    """Test prevention agent executes."""
    agent = PreventionAgent(model_router=None)

    agent_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={
            "analysis": {},
            "root_causes": ["PM procedure incomplete"]
        }
    )

    output = agent.execute(agent_input)
    assert output.agent_type == "prevention"


def test_prevention_agent_prevention_plan():
    """Test prevention agent generates prevention plan."""
    agent = PreventionAgent(model_router=None)

    mock_response = json.dumps({
        "permanent_actions": [
            {
                "action": "Update PM procedure step 5",
                "rationale": "Prevents contamination",
                "owner": "Process Engineering",
                "timeline": "Within 2 weeks",
                "success_metrics": "Zero recurrence",
                "implementation_steps": ["Review SOP", "Add clean step", "Train team"]
            }
        ],
        "systemic_prevention": [
            {
                "change": "Add SPC limit to chamber cleanliness",
                "scope": "All etch tools",
                "implementation": "Update control plan",
                "benefits": "Early detection",
                "risks": "May increase false alarms"
            }
        ],
        "lessons_learned": ["Always check PM logs", "24-hour window for PM effects"],
        "knowledge_base_updates": [
            {
                "document": "Etch Tool Handbook Section 3.2",
                "update_needed": "Add this failure mode",
                "priority": "high"
            }
        ],
        "follow_up_items": [
            {
                "item": "Review all etch PM procedures",
                "owner": "Process Engineering",
                "deadline": "End of month"
            }
        ]
    })

    agent._call_llm = lambda **kwargs: mock_response

    agent_input = AgentInput(
        mode=ProblemMode.EXCURSION,
        security_tier=SecurityTier.GENERAL_LLM,
        context={"analysis": {}, "root_causes": []}
    )

    output = agent.execute(agent_input)

    # Should extract permanent actions as facts
    assert len(output.facts) > 0
    # Should extract benefits/risks as hypotheses
    assert len(output.hypotheses) > 0
    # Should address D5, D7, D8
    assert "D5" in output.eight_d_phases_addressed
    assert "D7" in output.eight_d_phases_addressed
    assert "D8" in output.eight_d_phases_addressed


def test_prevention_agent_mode_awareness():
    """Test prevention agent adapts to problem mode."""
    agent = PreventionAgent(model_router=None)

    modes = [ProblemMode.EXCURSION, ProblemMode.IMPROVEMENT, ProblemMode.OPERATIONS]

    for mode in modes:
        agent_input = AgentInput(
            mode=mode,
            security_tier=SecurityTier.GENERAL_LLM,
            context={"analysis": {}, "root_causes": []}
        )

        prompt = agent.generate_prompt(agent_input)

        # Verify mode-specific guidance
        if mode == ProblemMode.EXCURSION:
            assert "excursion" in prompt.lower() or "containment" in prompt.lower()
        elif mode == ProblemMode.IMPROVEMENT:
            assert "improvement" in prompt.lower() or "sustainable" in prompt.lower()
        elif mode == ProblemMode.OPERATIONS:
            assert "operations" in prompt.lower() or "workflow" in prompt.lower()
```

### Success Criteria:

#### Automated Verification:
- [ ] All unit tests pass: `pytest tests/test_narrative_agent.py tests/test_clarification_agent.py tests/test_analysis_agent.py tests/test_prevention_agent.py -v`
- [ ] No test failures or errors
- [ ] Code coverage for agents: `pytest --cov=atlassemi.agents --cov-report=term-missing`

#### Manual Verification:
- [ ] Can run individual test files successfully
- [ ] Mock LLM responses work correctly
- [ ] Edge cases (empty input, malformed JSON) handled
- [ ] Tests execute quickly (no actual API calls)

**Implementation Note**: Run all unit tests and verify 90%+ coverage for agent modules before proceeding to integration tests.

---

## Phase 5: Integration Tests and Edge Cases

### Overview
Create integration tests for the full workflow and comprehensive edge case coverage.

### Changes Required:

#### 1. Orchestrator Integration Tests
**File**: `tests/test_orchestrator.py`
**Changes**: Create new file with integration tests

```python
"""Integration tests for Workflow Orchestrator"""

import pytest
import json
from atlassemi.orchestrator import WorkflowOrchestrator
from atlassemi.agents.base import ProblemMode, SecurityTier
from atlassemi.config import ModelRouter, RuntimeMode


def test_orchestrator_full_workflow_mock():
    """Test full workflow with mock LLM responses."""
    router = ModelRouter(mode=RuntimeMode.DEV)
    orchestrator = WorkflowOrchestrator(model_router=router)

    # Mock answer collector that returns predefined answers
    def mock_collector(questions):
        return {q["question"]: "Test answer" for q in questions[:3]}  # Answer first 3

    result = orchestrator.run_workflow(
        narrative="Test yield excursion on Chamber B",
        mode=ProblemMode.EXCURSION,
        tier=SecurityTier.GENERAL_LLM,
        answer_collector=mock_collector
    )

    # Verify all phases completed
    assert len(result.phases_completed) == 4
    assert "Phase 0: Narrative" in result.phases_completed
    assert "Phase 1: Clarification" in result.phases_completed
    assert "Phase 2: Analysis" in result.phases_completed
    assert "Phase 3: Prevention" in result.phases_completed

    # Verify outputs exist
    assert result.narrative_output is not None
    assert result.analysis_output is not None
    assert result.prevention_output is not None

    # Verify cost accumulation
    assert result.total_cost_usd >= 0

    # Verify metrics
    assert result.facts_identified >= 0
    assert result.hypotheses_identified >= 0


def test_orchestrator_context_passing():
    """Test that context is passed correctly between phases."""
    router = ModelRouter(mode=RuntimeMode.DEV)
    orchestrator = WorkflowOrchestrator(model_router=router)

    def mock_collector(questions):
        return {"Q1": "A1", "Q2": "A2"}

    result = orchestrator.run_workflow(
        narrative="Specific test narrative for context passing",
        mode=ProblemMode.EXCURSION,
        tier=SecurityTier.GENERAL_LLM,
        answer_collector=mock_collector
    )

    # Verify narrative was captured
    narrative_text = result.narrative_output.metadata.get("narrative", "")
    assert "Specific test narrative" in narrative_text

    # Verify clarification answers were collected
    assert len(result.clarification_answers) > 0


def test_orchestrator_cost_accumulation():
    """Test that costs accumulate across all phases."""
    router = ModelRouter(mode=RuntimeMode.DEV)
    orchestrator = WorkflowOrchestrator(model_router=router)

    def mock_collector(questions):
        return {}

    result = orchestrator.run_workflow(
        narrative="Cost test",
        mode=ProblemMode.EXCURSION,
        tier=SecurityTier.GENERAL_LLM,
        answer_collector=mock_collector
    )

    # Total cost should be sum of individual phase costs
    expected_cost = (
        result.narrative_output.cost_usd +
        result.analysis_output.cost_usd +
        result.prevention_output.cost_usd
    )

    assert abs(result.total_cost_usd - expected_cost) < 0.01  # Within rounding error


def test_orchestrator_different_modes():
    """Test orchestrator works with all problem modes."""
    router = ModelRouter(mode=RuntimeMode.DEV)
    orchestrator = WorkflowOrchestrator(model_router=router)

    modes = [ProblemMode.EXCURSION, ProblemMode.IMPROVEMENT, ProblemMode.OPERATIONS]

    for mode in modes:
        result = orchestrator.run_workflow(
            narrative=f"Test for {mode.value} mode",
            mode=mode,
            tier=SecurityTier.GENERAL_LLM,
            answer_collector=lambda q: {}
        )

        assert len(result.phases_completed) == 4
```

#### 2. Model Router Tests
**File**: `tests/test_model_router.py`
**Changes**: Create new file with tests

```python
"""Tests for Model Router"""

import pytest
from atlassemi.config import ModelRouter, RuntimeMode
from atlassemi.agents.base import SecurityTier


def test_model_router_dev_mode():
    """Test model router in dev mode."""
    router = ModelRouter(mode=RuntimeMode.DEV)

    config = router.get_model_config("reasoning", SecurityTier.GENERAL_LLM)

    # Dev mode should use Haiku
    assert "haiku" in config.model_id.lower()


def test_model_router_runtime_mode():
    """Test model router in runtime mode."""
    router = ModelRouter(mode=RuntimeMode.RUNTIME)

    config = router.get_model_config("reasoning", SecurityTier.GENERAL_LLM)

    # Runtime mode should use Sonnet or Opus
    assert "sonnet" in config.model_id.lower() or "opus" in config.model_id.lower()


def test_model_router_tier_enforcement():
    """Test model router respects security tiers."""
    router = ModelRouter(mode=RuntimeMode.DEV)

    # Tier 1 should use Anthropic
    tier1_config = router.get_model_config("reasoning", SecurityTier.GENERAL_LLM)
    assert tier1_config.provider in ["anthropic", "openai"]

    # Tier 2 should use Factory (placeholder)
    tier2_config = router.get_model_config("reasoning", SecurityTier.CONFIDENTIAL_FAB)
    assert tier2_config.provider == "factory"

    # Tier 3 should use On-prem (placeholder)
    tier3_config = router.get_model_config("reasoning", SecurityTier.TOP_SECRET)
    assert tier3_config.provider == "onprem"


def test_model_router_cost_tracking():
    """Test model router tracks costs correctly."""
    router = ModelRouter(mode=RuntimeMode.DEV)

    # Initial cost should be zero
    assert router.usage_stats["total_cost_usd"] == 0

    # Track some usage
    router.track_usage(
        task_type="reasoning",
        input_tokens=100,
        output_tokens=50,
        cost_usd=0.01
    )

    # Cost should be updated
    assert router.usage_stats["total_cost_usd"] == 0.01
```

#### 3. Tier Enforcer Tests
**File**: `tests/test_tier_enforcer.py`
**Changes**: Create new file with tests

```python
"""Tests for Security Tier Enforcer"""

import pytest
from atlassemi.security.tier_enforcer import TierEnforcer, SecurityViolationError, ToolCategory
from atlassemi.agents.base import SecurityTier


def test_tier_enforcer_general_llm():
    """Test tier 1 allows external APIs."""
    enforcer = TierEnforcer(current_tier=SecurityTier.GENERAL_LLM)

    # Should allow external APIs
    enforcer.check_tool_allowed(ToolCategory.EXTERNAL_API)  # Should not raise


def test_tier_enforcer_confidential_blocks_external():
    """Test tier 2 blocks external APIs."""
    enforcer = TierEnforcer(current_tier=SecurityTier.CONFIDENTIAL_FAB)

    # Should block external APIs
    with pytest.raises(SecurityViolationError):
        enforcer.check_tool_allowed(ToolCategory.EXTERNAL_API)


def test_tier_enforcer_top_secret_blocks_all_external():
    """Test tier 3 blocks all external access."""
    enforcer = TierEnforcer(current_tier=SecurityTier.TOP_SECRET)

    # Should block external APIs
    with pytest.raises(SecurityViolationError):
        enforcer.check_tool_allowed(ToolCategory.EXTERNAL_API)

    # Should block factory APIs
    with pytest.raises(SecurityViolationError):
        enforcer.check_tool_allowed(ToolCategory.FACTORY_API)


def test_tier_enforcer_allows_local_tools():
    """Test all tiers allow local tools."""
    tiers = [SecurityTier.GENERAL_LLM, SecurityTier.CONFIDENTIAL_FAB, SecurityTier.TOP_SECRET]

    for tier in tiers:
        enforcer = TierEnforcer(current_tier=tier)
        enforcer.check_tool_allowed(ToolCategory.LOCAL_TOOL)  # Should not raise
```

### Success Criteria:

#### Automated Verification:
- [ ] All integration tests pass: `pytest tests/test_orchestrator.py tests/test_model_router.py tests/test_tier_enforcer.py -v`
- [ ] Full test suite passes: `pytest tests/ -v`
- [ ] Test coverage 90%+: `pytest --cov=atlassemi --cov-report=html`
- [ ] No test failures or warnings

#### Manual Verification:
- [ ] Integration tests cover full workflow
- [ ] Edge cases don't crash the system
- [ ] Error messages are helpful
- [ ] Coverage report shows all critical paths tested

**Implementation Note**: Run full test suite with coverage report. Review any uncovered code paths and add tests if they represent critical functionality.

---

## Phase 6: Documentation and CLI Integration

### Overview
Update CLI to use orchestrator, add deployment documentation, and finalize production readiness.

### Changes Required:

#### 1. Update CLI to Use Orchestrator
**File**: `cli.py`
**Changes**: Replace individual phase execution with orchestrator

```python
#!/usr/bin/env python3
"""
ATLASsemi Command-Line Interface

Main entry point for fab problem-solving workflow.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from atlassemi.agents.base import ProblemMode, SecurityTier
from atlassemi.orchestrator import WorkflowOrchestrator
from atlassemi.security.tier_enforcer import TierEnforcer, SecurityViolationError
from atlassemi.config import ModelRouter, RuntimeMode
import os


def main():
    """Main CLI entry point."""
    print("=" * 80)
    print("ATLASsemi - Semiconductor Fab Problem-Solving Assistant")
    print("=" * 80)
    print()

    # Initialize model router
    runtime_mode_env = os.getenv("ATLASSEMI_RUNTIME_MODE", "dev")
    runtime_mode = RuntimeMode.RUNTIME if runtime_mode_env == "runtime" else RuntimeMode.DEV

    print(f"Runtime Mode: {runtime_mode.value.upper()}")
    print()

    model_router = ModelRouter(mode=runtime_mode)

    # Step 1: Select mode
    print("Problem-Solving Mode:")
    print("  1. Yield Excursion Response (fast containment)")
    print("  2. Yield Improvement (continuous improvement)")
    print("  3. Factory Operations (sustainment)")
    print()

    mode_choice = input("Select mode [1-3]: ").strip()

    mode_map = {
        "1": ProblemMode.EXCURSION,
        "2": ProblemMode.IMPROVEMENT,
        "3": ProblemMode.OPERATIONS,
    }

    mode = mode_map.get(mode_choice)
    if mode is None:
        print("Invalid mode selection.")
        return

    print(f"\nMode: {mode.value}")
    print()

    # Step 2: Select security tier
    print("Security Tier:")
    print("  1. General LLM (public knowledge only)")
    print("  2. Confidential Fab (factory API access)")
    print("  3. Top Secret (on-prem only)")
    print()

    tier_choice = input("Select tier [1-3]: ").strip()

    tier_map = {
        "1": SecurityTier.GENERAL_LLM,
        "2": SecurityTier.CONFIDENTIAL_FAB,
        "3": SecurityTier.TOP_SECRET,
    }

    tier = tier_map.get(tier_choice)
    if tier is None:
        print("Invalid tier selection.")
        return

    print(f"\nSecurity Tier: {tier.name}")
    print()

    # Initialize tier enforcer
    enforcer = TierEnforcer(current_tier=tier)
    print(f"Allowed tools in this tier: {', '.join(enforcer.get_allowed_tools())}")
    print()

    # Step 3: Narrative intake
    print("=" * 80)
    print("Problem Description")
    print("=" * 80)
    print()
    print("Describe the situation in your own words.")
    print("(Type your description, then press Ctrl+D on Unix or Ctrl+Z on Windows when done)")
    print()

    # Get user narrative
    narrative_lines = []
    try:
        while True:
            line = input()
            narrative_lines.append(line)
    except EOFError:
        pass

    narrative = "\n".join(narrative_lines).strip()

    if not narrative:
        print("\nNo narrative provided. Exiting.")
        return

    print()
    print("=" * 80)
    print("Running 8D Analysis Workflow...")
    print("=" * 80)
    print()

    # Execute workflow via orchestrator
    try:
        orchestrator = WorkflowOrchestrator(model_router=model_router)

        result = orchestrator.run_workflow(
            narrative=narrative,
            mode=mode,
            tier=tier,
            answer_collector=None  # Use default CLI collector
        )

        # Display results
        print("\n" + "=" * 80)
        print("WORKFLOW COMPLETE")
        print("=" * 80)
        print()

        print(f"Phases Completed: {', '.join(result.phases_completed)}")
        print(f"Facts Identified: {result.facts_identified}")
        print(f"Hypotheses Generated: {result.hypotheses_identified}")
        print(f"8D Phases Addressed: {', '.join(result.eight_d_phases_addressed)}")
        print(f"Total Cost: ${result.total_cost_usd:.4f}")

        if result.errors:
            print(f"\nWarnings/Errors: {len(result.errors)}")
            for error in result.errors:
                print(f"  - {error}")

        print()

        # Show usage summary
        print("=" * 80)
        print("Session Usage Summary")
        print("=" * 80)
        print()
        print(model_router.get_usage_summary())
        print()

    except Exception as e:
        print(f"Error during workflow: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        main()
    except SecurityViolationError as e:
        print()
        print("=" * 80)
        print("SECURITY VIOLATION")
        print("=" * 80)
        print()
        print(str(e))
        print()
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print()
        print("=" * 80)
        print("ERROR")
        print("=" * 80)
        print()
        print(f"An error occurred: {e}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

#### 2. Deployment Documentation
**File**: `docs/DEPLOYMENT.md`
**Changes**: Create comprehensive deployment guide

```markdown
# ATLASsemi Deployment Guide

## Prerequisites

- Python 3.10 or later
- Virtual environment (recommended)
- API keys for LLM providers (if using external APIs)

## Installation

### 1. Clone Repository

\```bash
git clone https://github.com/chemnteach/ATLASsemi.git
cd ATLASsemi
\```

### 2. Create Virtual Environment

\```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\```

### 3. Install Dependencies

\```bash
pip install -r requirements.txt
\```

### 4. Configure API Keys (Optional)

If using external LLM providers:

\```bash
# For General LLM tier (Tier 1)
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"

# Set runtime mode
export ATLASSEMI_RUNTIME_MODE="dev"  # or "runtime" for production models
\```

## Usage

### Basic Workflow

\```bash
python cli.py
\```

Follow the prompts to:
1. Select problem mode (excursion/improvement/operations)
2. Select security tier (general/confidential/top secret)
3. Enter problem narrative
4. Answer clarification questions
5. Review 8D analysis and prevention plan

### Example Session

\```
$ python cli.py

Problem-Solving Mode:
  1. Yield Excursion Response (fast containment)
  2. Yield Improvement (continuous improvement)
  3. Factory Operations (sustainment)

Select mode [1-3]: 1

Security Tier:
  1. General LLM (public knowledge only)
  2. Confidential Fab (factory API access)
  3. Top Secret (on-prem only)

Select tier [1-3]: 1

Problem Description:
Describe the situation in your own words.

[Enter your narrative, press Ctrl+D when done]

[Workflow executes all 4 phases...]

WORKFLOW COMPLETE
Phases Completed: Phase 0: Narrative, Phase 1: Clarification, Phase 2: Analysis, Phase 3: Prevention
Facts Identified: 12
Hypotheses Generated: 8
8D Phases Addressed: D0, D1, D2, D3, D4, D5, D6, D7, D8
Total Cost: $0.0823
\```

## Configuration

### Runtime Modes

- **dev**: Fast/cheap models for testing (Claude Haiku)
- **runtime**: Best models for production (Claude Sonnet/Opus)

Set via environment variable:
\```bash
export ATLASSEMI_RUNTIME_MODE="runtime"
\```

### Security Tiers

- **Tier 1 (General LLM)**: Public knowledge only, external APIs allowed
- **Tier 2 (Confidential Fab)**: Factory API only, no external APIs
- **Tier 3 (Top Secret)**: On-prem only, air-gapped

## Troubleshooting

### "No module named 'atlassemi'"

Ensure you're in the project directory and have activated the virtual environment.

### "API key not found"

Set API keys as environment variables:
\```bash
export ANTHROPIC_API_KEY="your-key"
\```

Or use mock mode (no API key required):
\```bash
# Mock mode is default if no API keys set
python cli.py
\```

### "Security violation" errors

You've selected a security tier that requires APIs not yet configured:
- Tier 2 requires Factory API configuration
- Tier 3 requires On-prem API configuration

Use Tier 1 (General LLM) for MVP.

## Testing

Run automated tests:

\```bash
# All tests
pytest tests/ -v

# With coverage
pytest --cov=atlassemi --cov-report=html

# Specific test file
pytest tests/test_orchestrator.py -v
\```

## Production Deployment

For production use with factory data:

1. Configure Factory API endpoint (Tier 2)
2. Configure On-prem API endpoint (Tier 3)
3. Set up audit logging
4. Enable runtime mode for best models
5. Test with real fab scenarios

See `SECURITY.md` for security tier guidelines.

## Support

- Documentation: See `CLAUDE.md`, `QUICK_START.md`
- Issues: https://github.com/chemnteach/ATLASsemi/issues
- Security: Review `SECURITY.md` before handling proprietary data
```

#### 3. Update README
**File**: `README.md`
**Changes**: Add MVP v1.0 status and deployment instructions

Add section:
```markdown
## Status

**Version:** 1.0.0 (MVP)
**Status:** ✅ Production Ready

All 4 phases implemented and tested:
- ✅ Phase 0: Narrative Analysis
- ✅ Phase 1: Clarification Questions
- ✅ Phase 2: 8D Analysis
- ✅ Phase 3: Prevention Planning

**Test Coverage:** 90%+

**Ready for:**
- Deployment with General LLM tier
- Real-world 8D problem-solving
- Incremental enhancements (RAG, APIs)

## Quick Start

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for full installation and usage guide.

\```bash
pip install -r requirements.txt
python cli.py
\```
```

### Success Criteria:

#### Automated Verification:
- [ ] CLI runs without errors: `python cli.py`
- [ ] Documentation files exist and are valid markdown
- [ ] All links in README work
- [ ] No broken references in documentation

#### Manual Verification:
- [ ] Full workflow executes via CLI using orchestrator
- [ ] Clarification Q&A works correctly
- [ ] All 4 phases display results
- [ ] Cost tracking shows accurate totals
- [ ] Deployment guide can be followed by new user
- [ ] Error messages are clear and helpful

**Implementation Note**: Run end-to-end test with orchestrator via CLI. Verify all 4 phases execute and display correctly before marking complete.

---

## Testing Strategy

### Unit Tests (Per Agent)
- **What**: Each agent independently with mock LLM
- **Coverage**: Agent logic, JSON parsing, mode awareness, error handling
- **Tools**: pytest with mocked `_call_llm` method
- **Goal**: 90%+ coverage for agent modules

### Integration Tests (Full Workflow)
- **What**: Orchestrator with all 4 agents chained
- **Coverage**: Context passing, cost accumulation, phase transitions
- **Tools**: pytest with mock LLM or real API (optional)
- **Goal**: All happy paths and critical error paths

### Edge Case Tests
- **What**: Empty inputs, malformed JSON, API failures, invalid tiers
- **Coverage**: Graceful degradation, fallback behavior, error messages
- **Tools**: pytest with error injection
- **Goal**: System never crashes, always provides useful feedback

### Manual End-to-End Test
1. Run `python cli.py`
2. Select Excursion mode, Tier 1
3. Enter realistic fab problem narrative
4. Answer clarification questions
5. Review full 8D analysis
6. Verify prevention plan references analysis
7. Check cost tracking

## Performance Considerations

- **Token budgets**: Already tuned per agent (2000-4000 tokens)
- **Network calls**: Sequential (no parallelization needed for MVP)
- **Cost optimization**: Dev mode uses Haiku (~$0.08/workflow vs $0.50+ for Sonnet)
- **Response time**: Expect 30-60 seconds for full workflow in dev mode

## Migration Notes

N/A - This is new functionality, no migration needed.

## References

- Previous implementation plan: `thoughts/shared/plans/2026-01-07-prevention-agent-phase3.md`
- Handoff document: `thoughts/shared/handoffs/atlassemi-initial-setup-handoff.md`
- Development status: `DEVELOPMENT_STATUS.md`
- Agent patterns:
  - `src/atlassemi/agents/narrative_agent.py` (Phase 0 reference)
  - `src/atlassemi/agents/clarification_agent.py` (Phase 1 reference)
  - `src/atlassemi/agents/analysis_agent.py` (Phase 2 reference)
  - `src/atlassemi/agents/prevention_agent.py` (Phase 3 reference)
- Base agent: `src/atlassemi/agents/base.py`
- Model router: `src/atlassemi/config/model_router.py`
- CLI: `cli.py`

## Implementation Notes

- Follow established patterns from existing agents
- Use same error handling approach (try/except with fallback)
- Maintain mode-aware prompting style
- Keep JSON output structure consistent
- Document all public methods with docstrings and type hints
- Add inline comments for complex logic
- Use descriptive variable names
- Follow PEP 8 style guide

## Success Indicators

**MVP v1.0 is complete when:**
1. ✅ Orchestrator chains all 4 phases automatically
2. ✅ Clarification Q&A collects user answers
3. ✅ Rich context passed between all phases
4. ✅ All unit tests pass (4 agents)
5. ✅ All integration tests pass (orchestrator, router, enforcer)
6. ✅ Test coverage 90%+
7. ✅ CLI uses orchestrator
8. ✅ Deployment documentation complete
9. ✅ End-to-end manual test successful
10. ✅ README updated with v1.0 status

**Ready for enhancement when:**
- All automated tests passing
- Manual end-to-end test successful
- Documentation reviewed and accurate
- Code formatted and linted
- Committed to git and pushed to GitHub

---

**Estimated Total Effort:** 12-15 hours
- Phase 1: 2 hours
- Phase 2: 2 hours
- Phase 3: 1 hour
- Phase 4: 4 hours
- Phase 5: 2 hours
- Phase 6: 2 hours

**Production-Ready Foundation:** This plan creates a deployable v1.0 that can be used immediately and enhanced incrementally with RAG, Factory API, and On-prem API without breaking existing functionality.
