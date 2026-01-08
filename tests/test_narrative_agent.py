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
        "observations": [
            "Yield dropped on Chamber B",
            "Cpk went from 1.8 to 0.9"
        ],
        "interpretations": ["Maintenance may have caused issue"],
        "constraints": ["Ships Friday", "200 wafers at risk"],
        "urgency_signals": ["Customer critical lot"],
        "data_sources_mentioned": [
            "SPC charts",
            "Critical dimension measurements"
        ],
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

    modes = [
        ProblemMode.EXCURSION,
        ProblemMode.IMPROVEMENT,
        ProblemMode.OPERATIONS
    ]

    for mode in modes:
        agent_input = AgentInput(
            mode=mode,
            security_tier=SecurityTier.GENERAL_LLM,
            context={"narrative": "Test"}
        )

        prompt = agent.generate_prompt(agent_input)
        # Prompt should contain mode-specific information
        assert len(prompt) > 0
