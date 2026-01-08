"""Tests for Security Tier Enforcer"""

import pytest
from atlassemi.security.tier_enforcer import (
    TierEnforcer,
    SecurityViolationError,
    SecurityTier
)


def test_tier_enforcer_general_llm():
    """Test tier 1 allows external APIs."""
    enforcer = TierEnforcer(current_tier=SecurityTier.GENERAL_LLM)

    # Should allow external APIs like Anthropic
    assert enforcer.validate_tool_use("anthropic") is True


def test_tier_enforcer_confidential_blocks_external():
    """Test tier 2 blocks external APIs."""
    enforcer = TierEnforcer(current_tier=SecurityTier.CONFIDENTIAL_FAB)

    # Should block external APIs
    with pytest.raises(SecurityViolationError):
        enforcer.validate_tool_use("anthropic")


def test_tier_enforcer_top_secret_blocks_all_external():
    """Test tier 3 blocks all external access."""
    enforcer = TierEnforcer(current_tier=SecurityTier.TOP_SECRET)

    # Should block external APIs
    with pytest.raises(SecurityViolationError):
        enforcer.validate_tool_use("anthropic")

    # Should block factory APIs
    with pytest.raises(SecurityViolationError):
        enforcer.validate_tool_use("factory_spc")


def test_tier_enforcer_allows_local_tools():
    """Test all tiers allow local tools."""
    tiers = [
        SecurityTier.GENERAL_LLM,
        SecurityTier.CONFIDENTIAL_FAB,
        SecurityTier.TOP_SECRET
    ]

    for tier in tiers:
        enforcer = TierEnforcer(current_tier=tier)
        # Should not raise
        assert enforcer.validate_tool_use("git") is True
