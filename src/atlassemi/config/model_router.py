"""
Model Router for ATLASsemi

Handles:
- Dev mode vs Runtime mode selection
- Security tier-aware model routing
- Task-specific model selection
- Cost tracking
"""

import os
from typing import Dict, Any, Optional, Literal
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class RuntimeMode(Enum):
    """Runtime mode for model selection."""
    DEV = "dev"         # Development: use fast/cheap models for testing
    RUNTIME = "runtime" # Production: use best models for actual work


TaskType = Literal["reasoning", "deep_analysis", "synthesis", "fast"]


@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    provider: str           # "anthropic", "openai", "factory", "onprem"
    model_id: str          # e.g., "claude-sonnet-4", "gpt-4o"
    max_tokens: int
    temperature: float = 0.7
    cost_per_1k_input: float = 0.0   # USD
    cost_per_1k_output: float = 0.0  # USD


class ModelRouter:
    """
    Routes LLM requests to appropriate models based on:
    - Runtime mode (dev vs production)
    - Security tier
    - Task type
    """

    # Model configurations for different scenarios
    # Format: (mode, tier, task_type) -> ModelConfig
    MODEL_MATRIX: Dict[tuple, ModelConfig] = {
        # DEV MODE - GENERAL_LLM (fast/cheap for testing)
        ("dev", 1, "reasoning"): ModelConfig(
            provider="anthropic",
            model_id="claude-haiku-4",
            max_tokens=4000,
            temperature=0.7,
            cost_per_1k_input=0.25,
            cost_per_1k_output=1.25
        ),
        ("dev", 1, "deep_analysis"): ModelConfig(
            provider="anthropic",
            model_id="claude-haiku-4",
            max_tokens=8000,
            temperature=0.7,
            cost_per_1k_input=0.25,
            cost_per_1k_output=1.25
        ),
        ("dev", 1, "synthesis"): ModelConfig(
            provider="anthropic",
            model_id="claude-haiku-4",
            max_tokens=6000,
            temperature=0.7,
            cost_per_1k_input=0.25,
            cost_per_1k_output=1.25
        ),
        ("dev", 1, "fast"): ModelConfig(
            provider="anthropic",
            model_id="claude-haiku-4",
            max_tokens=2000,
            temperature=0.7,
            cost_per_1k_input=0.25,
            cost_per_1k_output=1.25
        ),

        # RUNTIME MODE - GENERAL_LLM (best public models)
        ("runtime", 1, "reasoning"): ModelConfig(
            provider="anthropic",
            model_id="claude-sonnet-4-5",
            max_tokens=8000,
            temperature=0.7,
            cost_per_1k_input=3.0,
            cost_per_1k_output=15.0
        ),
        ("runtime", 1, "deep_analysis"): ModelConfig(
            provider="anthropic",
            model_id="claude-opus-4-5",
            max_tokens=16000,
            temperature=0.7,
            cost_per_1k_input=15.0,
            cost_per_1k_output=75.0
        ),
        ("runtime", 1, "synthesis"): ModelConfig(
            provider="anthropic",
            model_id="claude-sonnet-4-5",
            max_tokens=8000,
            temperature=0.7,
            cost_per_1k_input=3.0,
            cost_per_1k_output=15.0
        ),
        ("runtime", 1, "fast"): ModelConfig(
            provider="anthropic",
            model_id="claude-haiku-4",
            max_tokens=4000,
            temperature=0.7,
            cost_per_1k_input=0.25,
            cost_per_1k_output=1.25
        ),

        # CONFIDENTIAL_FAB (tier 2) - Factory API
        # Same configs for dev and runtime (factory controls access)
        ("dev", 2, "reasoning"): ModelConfig(
            provider="factory",
            model_id="factory-reasoning",
            max_tokens=8000,
            temperature=0.7
        ),
        ("dev", 2, "deep_analysis"): ModelConfig(
            provider="factory",
            model_id="factory-analysis",
            max_tokens=16000,
            temperature=0.7
        ),
        ("dev", 2, "synthesis"): ModelConfig(
            provider="factory",
            model_id="factory-synthesis",
            max_tokens=8000,
            temperature=0.7
        ),
        ("dev", 2, "fast"): ModelConfig(
            provider="factory",
            model_id="factory-fast",
            max_tokens=4000,
            temperature=0.7
        ),
        ("runtime", 2, "reasoning"): ModelConfig(
            provider="factory",
            model_id="factory-reasoning",
            max_tokens=8000,
            temperature=0.7
        ),
        ("runtime", 2, "deep_analysis"): ModelConfig(
            provider="factory",
            model_id="factory-analysis",
            max_tokens=16000,
            temperature=0.7
        ),
        ("runtime", 2, "synthesis"): ModelConfig(
            provider="factory",
            model_id="factory-synthesis",
            max_tokens=8000,
            temperature=0.7
        ),
        ("runtime", 2, "fast"): ModelConfig(
            provider="factory",
            model_id="factory-fast",
            max_tokens=4000,
            temperature=0.7
        ),

        # TOP_SECRET (tier 3) - On-prem only
        ("dev", 3, "reasoning"): ModelConfig(
            provider="onprem",
            model_id="onprem-reasoning",
            max_tokens=8000,
            temperature=0.7
        ),
        ("dev", 3, "deep_analysis"): ModelConfig(
            provider="onprem",
            model_id="onprem-analysis",
            max_tokens=16000,
            temperature=0.7
        ),
        ("dev", 3, "synthesis"): ModelConfig(
            provider="onprem",
            model_id="onprem-synthesis",
            max_tokens=8000,
            temperature=0.7
        ),
        ("dev", 3, "fast"): ModelConfig(
            provider="onprem",
            model_id="onprem-fast",
            max_tokens=4000,
            temperature=0.7
        ),
        ("runtime", 3, "reasoning"): ModelConfig(
            provider="onprem",
            model_id="onprem-reasoning",
            max_tokens=8000,
            temperature=0.7
        ),
        ("runtime", 3, "deep_analysis"): ModelConfig(
            provider="onprem",
            model_id="onprem-analysis",
            max_tokens=16000,
            temperature=0.7
        ),
        ("runtime", 3, "synthesis"): ModelConfig(
            provider="onprem",
            model_id="onprem-synthesis",
            max_tokens=8000,
            temperature=0.7
        ),
        ("runtime", 3, "fast"): ModelConfig(
            provider="onprem",
            model_id="onprem-fast",
            max_tokens=4000,
            temperature=0.7
        ),
    }

    def __init__(
        self,
        mode: RuntimeMode = RuntimeMode.DEV,
        api_keys: Optional[Dict[str, str]] = None
    ):
        """
        Initialize model router.

        Args:
            mode: Runtime mode (dev or runtime)
            api_keys: API keys for providers (reads from env if not provided)
        """
        self.mode = mode
        self.api_keys = api_keys or self._load_api_keys_from_env()

        # Track usage for cost calculation
        self.usage_stats: Dict[str, Any] = {
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost_usd": 0.0,
            "requests_by_task": {}
        }

        logger.info(f"ModelRouter initialized in {mode.value} mode")

    def _load_api_keys_from_env(self) -> Dict[str, str]:
        """
        Load API keys from environment variables.

        Returns:
            Dictionary of provider -> API key
        """
        return {
            "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
            "openai": os.getenv("OPENAI_API_KEY", ""),
            "factory": os.getenv("FACTORY_API_KEY", ""),
            "onprem": os.getenv("ONPREM_API_KEY", ""),
        }

    def get_model_config(
        self,
        task_type: TaskType,
        tier: Any  # SecurityTier enum
    ) -> ModelConfig:
        """
        Get model configuration for task and tier.

        Args:
            task_type: Type of task (reasoning, deep_analysis, synthesis, fast)
            tier: Security tier (1=GENERAL_LLM, 2=CONFIDENTIAL_FAB, 3=TOP_SECRET)

        Returns:
            ModelConfig for this scenario

        Raises:
            ValueError: If no model configured for this combination
        """
        # Convert tier enum to integer
        tier_value = tier.value if hasattr(tier, 'value') else tier

        # Look up model config
        key = (self.mode.value, tier_value, task_type)
        config = self.MODEL_MATRIX.get(key)

        if config is None:
            raise ValueError(
                f"No model configured for mode={self.mode.value}, "
                f"tier={tier_value}, task_type={task_type}"
            )

        logger.debug(
            f"Selected model: {config.model_id} (provider={config.provider}) "
            f"for task={task_type}, tier={tier_value}, mode={self.mode.value}"
        )

        return config

    def get_model_client(
        self,
        task_type: TaskType,
        tier: Any
    ) -> 'ModelClient':
        """
        Get a model client for the given task and tier.

        Args:
            task_type: Type of task
            tier: Security tier

        Returns:
            ModelClient instance configured for this scenario
        """
        config = self.get_model_config(task_type, tier)

        # Create appropriate client based on provider
        if config.provider == "anthropic":
            return AnthropicClient(config, self.api_keys.get("anthropic", ""))
        elif config.provider == "openai":
            return OpenAIClient(config, self.api_keys.get("openai", ""))
        elif config.provider == "factory":
            return FactoryClient(config, self.api_keys.get("factory", ""))
        elif config.provider == "onprem":
            return OnPremClient(config, self.api_keys.get("onprem", ""))
        else:
            raise ValueError(f"Unknown provider: {config.provider}")

    def track_usage(
        self,
        task_type: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float
    ):
        """
        Track token usage and cost.

        Args:
            task_type: Type of task
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost_usd: Cost in USD
        """
        self.usage_stats["total_input_tokens"] += input_tokens
        self.usage_stats["total_output_tokens"] += output_tokens
        self.usage_stats["total_cost_usd"] += cost_usd

        if task_type not in self.usage_stats["requests_by_task"]:
            self.usage_stats["requests_by_task"][task_type] = {
                "count": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "cost_usd": 0.0
            }

        stats = self.usage_stats["requests_by_task"][task_type]
        stats["count"] += 1
        stats["input_tokens"] += input_tokens
        stats["output_tokens"] += output_tokens
        stats["cost_usd"] += cost_usd

    def get_usage_summary(self) -> str:
        """
        Get usage summary for this session.

        Returns:
            Formatted usage summary
        """
        lines = [
            "# Model Usage Summary",
            "",
            f"**Total Input Tokens:** {self.usage_stats['total_input_tokens']:,}",
            f"**Total Output Tokens:** {self.usage_stats['total_output_tokens']:,}",
            f"**Total Cost:** ${self.usage_stats['total_cost_usd']:.4f}",
            "",
            "## By Task Type",
            ""
        ]

        for task_type, stats in self.usage_stats["requests_by_task"].items():
            lines.extend([
                f"### {task_type}",
                f"- Requests: {stats['count']}",
                f"- Input tokens: {stats['input_tokens']:,}",
                f"- Output tokens: {stats['output_tokens']:,}",
                f"- Cost: ${stats['cost_usd']:.4f}",
                ""
            ])

        return "\n".join(lines)


class ModelClient:
    """Base class for model clients."""

    def __init__(self, config: ModelConfig, api_key: str):
        self.config = config
        self.api_key = api_key

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> tuple[str, int, int]:
        """
        Generate completion from model.

        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            max_tokens: Override max tokens (optional)

        Returns:
            Tuple of (response_text, input_tokens, output_tokens)
        """
        raise NotImplementedError("Subclass must implement generate()")


class AnthropicClient(ModelClient):
    """Anthropic API client."""

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> tuple[str, int, int]:
        """Generate completion using Anthropic API."""
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "anthropic package not installed. Run: pip install anthropic"
            )

        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

        client = anthropic.Anthropic(api_key=self.api_key)

        messages = [{"role": "user", "content": prompt}]

        response = client.messages.create(
            model=self.config.model_id,
            max_tokens=max_tokens or self.config.max_tokens,
            temperature=self.config.temperature,
            system=system_prompt or "",
            messages=messages
        )

        # Extract response and token counts
        response_text = response.content[0].text
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        return response_text, input_tokens, output_tokens


class OpenAIClient(ModelClient):
    """OpenAI API client."""

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> tuple[str, int, int]:
        """Generate completion using OpenAI API."""
        try:
            import openai
        except ImportError:
            raise ImportError(
                "openai package not installed. Run: pip install openai"
            )

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set")

        client = openai.OpenAI(api_key=self.api_key)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=self.config.model_id,
            max_tokens=max_tokens or self.config.max_tokens,
            temperature=self.config.temperature,
            messages=messages
        )

        # Extract response and token counts
        response_text = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        return response_text, input_tokens, output_tokens


class FactoryClient(ModelClient):
    """Factory API client for confidential tier."""

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> tuple[str, int, int]:
        """Generate completion using Factory API."""
        # TODO: Implement factory API integration
        # This would connect to your internal factory GenAI system

        logger.warning("Factory API not yet implemented - returning mock response")

        return (
            "[Factory API response would appear here]",
            100,  # mock input tokens
            200   # mock output tokens
        )


class OnPremClient(ModelClient):
    """On-premises API client for top secret tier."""

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> tuple[str, int, int]:
        """Generate completion using on-prem API."""
        # TODO: Implement on-prem API integration
        # This would connect to your air-gapped internal system

        logger.warning("On-prem API not yet implemented - returning mock response")

        return (
            "[On-prem API response would appear here]",
            100,  # mock input tokens
            200   # mock output tokens
        )
