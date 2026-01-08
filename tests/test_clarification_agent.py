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
            {
                "question": "When did the issue start?",
                "rationale": "Timeline critical"
            },
            {
                "question": "What changed recently?",
                "rationale": "Root cause hunting"
            }
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
    assert (
        "when" in excursion_prompt.lower() or
        "what changed" in excursion_prompt.lower()
    )
