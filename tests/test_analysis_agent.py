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
        "phases": [
            {
                "phase": "D0",
                "title": "Preparation",
                "findings": ["Triggered by SPC alert"],
                "recommendations": ["Form investigation team"],
                "confidence": "high",
                "data_sources": ["SPC system"]
            },
            {
                "phase": "D2",
                "title": "Problem Definition",
                "findings": ["Yield drop on Chamber B"],
                "recommendations": ["Quantify impact"],
                "confidence": "medium",
                "data_sources": ["FDC data"]
            }
        ],
        "facts": ["Yield dropped 15%"],
        "hypotheses": ["PM procedure incomplete"],
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
    assert "D0" in output.eight_d_phases_addressed
    assert "D2" in output.eight_d_phases_addressed
