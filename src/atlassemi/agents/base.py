"""
Base agent class for ATLASsemi fab problem-solving agents.

All specialized agents (narrative, clarification, analysis, prevention)
inherit from BaseAgent.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum


class ProblemMode(Enum):
    """Problem-solving modes."""
    EXCURSION = "excursion"           # Mode A: Yield excursion response
    IMPROVEMENT = "improvement"        # Mode B: Continuous improvement
    OPERATIONS = "operations"          # Mode C: Factory operations


class SecurityTier(Enum):
    """Security tier for data access."""
    GENERAL_LLM = 1          # Public knowledge only
    CONFIDENTIAL_FAB = 2     # Factory API + approved docs
    TOP_SECRET = 3           # On-prem only, no external


@dataclass
class AgentInput:
    """Input to an agent."""

    mode: ProblemMode
    security_tier: SecurityTier
    context: Dict[str, Any]  # Narrative, clarifications, data, etc.
    instructions: Optional[str] = None

    # 8D phase context
    eight_d_phase: Optional[str] = None  # D0-D8

    # Session metadata
    session_id: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass
class AgentOutput:
    """Output from an agent."""

    agent_type: str
    content: str
    metadata: Dict[str, Any]

    # 8D mapping
    eight_d_phases_addressed: List[str] = field(default_factory=list)

    # Facts vs hypotheses
    facts: List[str] = field(default_factory=list)
    hypotheses: List[str] = field(default_factory=list)
    open_questions: List[str] = field(default_factory=list)

    # Cost tracking
    cost_usd: float = 0.0

    # Quality metrics
    quality_metrics: Dict[str, float] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Base class for all ATLASsemi fab problem-solving agents.

    Provides common functionality for:
    - LLM interaction (with tier enforcement)
    - 8D methodology mapping
    - Fact vs hypothesis separation
    - State management
    """

    def __init__(
        self,
        agent_type: str,
        model_router: Optional[Any] = None  # ModelRouter from config
    ):
        """
        Initialize base agent.

        Args:
            agent_type: Type of agent (narrative, clarification, analysis, prevention)
            model_router: ModelRouter for LLM calls (handles tier enforcement)
        """
        self.agent_type = agent_type
        self.model_router = model_router

    @abstractmethod
    def generate_prompt(self, agent_input: AgentInput) -> str:
        """
        Generate prompt for this agent.

        Must be implemented by subclasses.

        Args:
            agent_input: Input context and instructions

        Returns:
            Formatted prompt string
        """
        pass

    @abstractmethod
    def process_response(
        self,
        response: str,
        agent_input: AgentInput
    ) -> AgentOutput:
        """
        Process LLM response into AgentOutput.

        Must be implemented by subclasses.

        Args:
            response: Raw LLM response
            agent_input: Original input

        Returns:
            Processed AgentOutput
        """
        pass

    def get_max_tokens(self) -> int:
        """
        Get maximum tokens for this agent.

        Subclasses can override to request more tokens.

        Returns:
            Maximum tokens to generate
        """
        return 4000  # Default

    def execute(self, agent_input: AgentInput) -> AgentOutput:
        """
        Execute agent workflow.

        This is the template method that orchestrates:
        1. Prompt generation
        2. LLM call (with tier enforcement)
        3. Response processing

        Args:
            agent_input: Input for this agent

        Returns:
            AgentOutput with results
        """
        # Generate prompt
        prompt = self.generate_prompt(agent_input)

        # Get model client (tier-aware)
        if self.model_router:
            client = self.model_router.get_model_client(
                task_type=self._get_task_type(),
                tier=agent_input.security_tier
            )
        else:
            # Fallback for testing without router
            client = None

        # Execute LLM call
        response = self._call_llm(
            prompt=prompt,
            client=client,
            max_tokens=self.get_max_tokens()
        )

        # Process response
        output = self.process_response(response, agent_input)

        return output

    def _call_llm(
        self,
        prompt: str,
        client: Optional[Any],
        max_tokens: int
    ) -> str:
        """
        Call LLM with prompt.

        Args:
            prompt: Prompt string
            client: Model client (tier-aware)
            max_tokens: Maximum tokens to generate

        Returns:
            LLM response string
        """
        if client is None:
            # For testing without actual LLM
            return f"[Mock LLM response for: {prompt[:100]}...]"

        # Call model via client
        try:
            response_text, input_tokens, output_tokens = client.generate(
                prompt=prompt,
                max_tokens=max_tokens
            )

            # Track usage if router is available
            if self.model_router:
                cost_usd = self._calculate_cost(
                    client.config,
                    input_tokens,
                    output_tokens
                )
                self.model_router.track_usage(
                    task_type=self._get_task_type(),
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost_usd=cost_usd
                )

            return response_text

        except Exception as e:
            raise RuntimeError(f"LLM call failed: {e}")

    def _calculate_cost(
        self,
        config: Any,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """
        Calculate cost for LLM call.

        Args:
            config: ModelConfig with pricing
            input_tokens: Input token count
            output_tokens: Output token count

        Returns:
            Cost in USD
        """
        input_cost = (input_tokens / 1000.0) * config.cost_per_1k_input
        output_cost = (output_tokens / 1000.0) * config.cost_per_1k_output
        return input_cost + output_cost

    def _get_task_type(self) -> str:
        """
        Get task type for model selection.

        Returns:
            Task type string
        """
        task_type_map = {
            'narrative': 'reasoning',
            'clarification': 'reasoning',
            'analysis': 'deep_analysis',
            'prevention': 'synthesis'
        }
        return task_type_map.get(self.agent_type, 'reasoning')

    def format_context(self, agent_input: AgentInput) -> str:
        """
        Format context information for prompt.

        Args:
            agent_input: Input with context

        Returns:
            Formatted context string
        """
        lines = []

        # Mode and tier
        lines.append(f"## Mode: {agent_input.mode.value}")
        lines.append(f"## Security Tier: {agent_input.security_tier.name}")
        lines.append("")

        # 8D phase if specified
        if agent_input.eight_d_phase:
            lines.append(f"## 8D Phase: {agent_input.eight_d_phase}")
            lines.append("")

        # Narrative if present
        if 'narrative' in agent_input.context:
            lines.append("## User Narrative")
            lines.append("")
            lines.append(agent_input.context['narrative'])
            lines.append("")

        # Clarifications if present
        if 'clarifications' in agent_input.context:
            lines.append("## Clarifications")
            lines.append("")
            for q, a in agent_input.context['clarifications'].items():
                lines.append(f"**Q:** {q}")
                lines.append(f"**A:** {a}")
                lines.append("")

        # Previous analysis if present
        if 'previous_analysis' in agent_input.context:
            lines.append("## Previous Analysis")
            lines.append("")
            lines.append(str(agent_input.context['previous_analysis'])[:500] + "...")
            lines.append("")

        return "\n".join(lines)

    def extract_eight_d_mapping(self, content: str) -> List[str]:
        """
        Extract which 8D phases this content addresses.

        Args:
            content: Content to analyze

        Returns:
            List of 8D phases (e.g., ["D0", "D1", "D2"])
        """
        # Simple keyword-based extraction
        # TODO: Make this more sophisticated
        phases = []

        keywords = {
            "D0": ["preparation", "trigger", "alert", "initiated"],
            "D1": ["team", "owner", "responsible", "lead"],
            "D2": ["problem definition", "symptom", "scope", "timeline"],
            "D3": ["containment", "hold", "interim", "temporary"],
            "D4": ["root cause", "why", "analysis", "hypothesis"],
            "D5": ["permanent", "corrective action", "solution", "fix"],
            "D6": ["validation", "verification", "confirm", "test"],
            "D7": ["prevention", "systemic", "process change", "SOP"],
            "D8": ["lessons learned", "documentation", "share"]
        }

        content_lower = content.lower()

        for phase, terms in keywords.items():
            if any(term in content_lower for term in terms):
                phases.append(phase)

        return phases
