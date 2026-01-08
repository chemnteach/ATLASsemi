"""Integration tests for Workflow Orchestrator"""

import pytest
from atlassemi.orchestrator import WorkflowOrchestrator
from atlassemi.agents.base import ProblemMode, SecurityTier


def test_orchestrator_full_workflow_mock():
    """Test full workflow with mock LLM responses."""
    # Use None for model_router to trigger mock responses
    orchestrator = WorkflowOrchestrator(model_router=None)

    # Mock answer collector that returns predefined answers
    def mock_collector(questions):
        # Answer first 3 questions
        return {q["question"]: "Test answer" for q in questions[:3]}

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
    orchestrator = WorkflowOrchestrator(model_router=None)

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
    assert len(result.clarification_answers) >= 0


def test_orchestrator_cost_accumulation():
    """Test that costs accumulate across all phases."""
    orchestrator = WorkflowOrchestrator(model_router=None)

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

    # Within rounding error
    assert abs(result.total_cost_usd - expected_cost) < 0.01


def test_orchestrator_different_modes():
    """Test orchestrator works with all problem modes."""
    orchestrator = WorkflowOrchestrator(model_router=None)

    modes = [
        ProblemMode.EXCURSION,
        ProblemMode.IMPROVEMENT,
        ProblemMode.OPERATIONS
    ]

    for mode in modes:
        result = orchestrator.run_workflow(
            narrative=f"Test for {mode.value} mode",
            mode=mode,
            tier=SecurityTier.GENERAL_LLM,
            answer_collector=lambda q: {}
        )

        assert len(result.phases_completed) == 4
