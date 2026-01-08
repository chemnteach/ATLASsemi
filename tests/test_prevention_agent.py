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
                "implementation_steps": [
                    "Review SOP",
                    "Add clean step",
                    "Train team"
                ]
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
        "lessons_learned": [
            "Always check PM logs",
            "24-hour window for PM effects"
        ],
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

    modes = [
        ProblemMode.EXCURSION,
        ProblemMode.IMPROVEMENT,
        ProblemMode.OPERATIONS
    ]

    for mode in modes:
        agent_input = AgentInput(
            mode=mode,
            security_tier=SecurityTier.GENERAL_LLM,
            context={"analysis": {}, "root_causes": []}
        )

        prompt = agent.generate_prompt(agent_input)

        # Verify mode-specific guidance
        if mode == ProblemMode.EXCURSION:
            assert (
                "excursion" in prompt.lower() or
                "containment" in prompt.lower()
            )
        elif mode == ProblemMode.IMPROVEMENT:
            assert (
                "improvement" in prompt.lower() or
                "sustainable" in prompt.lower()
            )
        elif mode == ProblemMode.OPERATIONS:
            assert (
                "operations" in prompt.lower() or
                "workflow" in prompt.lower()
            )
