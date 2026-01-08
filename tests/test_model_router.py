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
    assert (
        "sonnet" in config.model_id.lower() or
        "opus" in config.model_id.lower()
    )


def test_model_router_tier_enforcement():
    """Test model router respects security tiers."""
    router = ModelRouter(mode=RuntimeMode.DEV)

    # Tier 1 should use Anthropic
    tier1_config = router.get_model_config(
        "reasoning",
        SecurityTier.GENERAL_LLM
    )
    assert tier1_config.provider in ["anthropic", "openai"]

    # Tier 2 should use Factory (placeholder)
    tier2_config = router.get_model_config(
        "reasoning",
        SecurityTier.CONFIDENTIAL_FAB
    )
    assert tier2_config.provider == "factory"

    # Tier 3 should use On-prem (placeholder)
    tier3_config = router.get_model_config(
        "reasoning",
        SecurityTier.TOP_SECRET
    )
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
