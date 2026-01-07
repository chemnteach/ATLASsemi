"""
Security Tier Enforcement

HARD enforcement of security tiers - blocks (not just warns) tier violations.
"""

from enum import Enum
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class SecurityTier(Enum):
    """Security tier for data access."""
    GENERAL_LLM = 1          # Public knowledge only
    CONFIDENTIAL_FAB = 2     # Factory API + approved docs
    TOP_SECRET = 3           # On-prem only, no external


class ToolCategory(Enum):
    """Tool categories for tier routing."""
    EXTERNAL_API = "external_api"        # OpenAI, Anthropic, etc.
    FACTORY_API = "factory_api"          # Internal factory APIs
    ONPREM_API = "onprem_api"           # On-premises only
    LOCAL_TOOL = "local_tool"            # Local filesystem, git, etc.
    KNOWLEDGE_GRAPH = "knowledge_graph"  # Internal knowledge base


@dataclass
class TierViolation:
    """Represents a security tier violation."""
    tool_name: str
    current_tier: SecurityTier
    required_tier: SecurityTier
    reason: str
    suggestion: str


class TierEnforcer:
    """
    Enforces security tier boundaries.

    This is NON-NEGOTIABLE. Violations are BLOCKED, not just logged.
    """

    # Tool to category mapping
    TOOL_CATEGORIES: Dict[str, ToolCategory] = {
        # External APIs (Tier 1 only)
        "openai": ToolCategory.EXTERNAL_API,
        "anthropic": ToolCategory.EXTERNAL_API,
        "google_gemini": ToolCategory.EXTERNAL_API,
        "perplexity": ToolCategory.EXTERNAL_API,

        # Factory APIs (Tier 2+)
        "factory_spc": ToolCategory.FACTORY_API,
        "factory_fdc": ToolCategory.FACTORY_API,
        "factory_metrology": ToolCategory.FACTORY_API,
        "factory_genai": ToolCategory.FACTORY_API,

        # On-prem only (Tier 3 only)
        "onprem_llm": ToolCategory.ONPREM_API,
        "recipe_database": ToolCategory.ONPREM_API,

        # Local tools (all tiers)
        "git": ToolCategory.LOCAL_TOOL,
        "ast-grep": ToolCategory.LOCAL_TOOL,
        "local_files": ToolCategory.LOCAL_TOOL,

        # Knowledge graph (Tier 2+)
        "knowledge_graph": ToolCategory.KNOWLEDGE_GRAPH,
    }

    # Tier permissions
    TIER_PERMISSIONS: Dict[SecurityTier, Set[ToolCategory]] = {
        SecurityTier.GENERAL_LLM: {
            ToolCategory.EXTERNAL_API,
            ToolCategory.LOCAL_TOOL,
        },
        SecurityTier.CONFIDENTIAL_FAB: {
            ToolCategory.FACTORY_API,
            ToolCategory.LOCAL_TOOL,
            ToolCategory.KNOWLEDGE_GRAPH,
            # NO external APIs
        },
        SecurityTier.TOP_SECRET: {
            ToolCategory.ONPREM_API,
            ToolCategory.LOCAL_TOOL,
            # NO external or factory APIs
        },
    }

    def __init__(self, current_tier: SecurityTier):
        """
        Initialize tier enforcer.

        Args:
            current_tier: Current security tier for this session
        """
        self.current_tier = current_tier
        self.violations: List[TierViolation] = []

    def validate_tool_use(self, tool_name: str) -> bool:
        """
        Validate if a tool can be used in the current tier.

        Args:
            tool_name: Tool to validate

        Returns:
            True if allowed, False if blocked

        Raises:
            SecurityViolationError: If tool use would violate tier
        """
        # Get tool category
        category = self.TOOL_CATEGORIES.get(tool_name)

        if category is None:
            # Unknown tool - default to most restrictive
            logger.warning(f"Unknown tool '{tool_name}' - defaulting to BLOCK")
            return False

        # Check if category is allowed in current tier
        allowed_categories = self.TIER_PERMISSIONS.get(self.current_tier, set())

        if category not in allowed_categories:
            violation = self._create_violation(tool_name, category)
            self.violations.append(violation)

            # Log violation
            logger.error(
                f"SECURITY VIOLATION: Tool '{tool_name}' (category: {category.value}) "
                f"not allowed in tier {self.current_tier.name}"
            )

            # BLOCK
            raise SecurityViolationError(violation)

        return True

    def _create_violation(
        self,
        tool_name: str,
        category: ToolCategory
    ) -> TierViolation:
        """
        Create a TierViolation with helpful suggestion.

        Args:
            tool_name: Tool that was blocked
            category: Category of the tool

        Returns:
            TierViolation with details
        """
        suggestions = {
            (SecurityTier.CONFIDENTIAL_FAB, ToolCategory.EXTERNAL_API):
                f"Use factory_genai API instead of {tool_name}",

            (SecurityTier.TOP_SECRET, ToolCategory.EXTERNAL_API):
                f"Use onprem_llm instead of {tool_name}",

            (SecurityTier.TOP_SECRET, ToolCategory.FACTORY_API):
                f"Factory APIs not available in Top Secret tier. Use onprem_llm.",

            (SecurityTier.GENERAL_LLM, ToolCategory.FACTORY_API):
                f"Factory APIs require Confidential tier or higher",

            (SecurityTier.GENERAL_LLM, ToolCategory.ONPREM_API):
                f"On-prem APIs require Top Secret tier",
        }

        suggestion = suggestions.get(
            (self.current_tier, category),
            f"Tool '{tool_name}' not available in {self.current_tier.name} tier"
        )

        return TierViolation(
            tool_name=tool_name,
            current_tier=self.current_tier,
            required_tier=self._get_required_tier(category),
            reason=f"Tool category '{category.value}' not permitted in {self.current_tier.name}",
            suggestion=suggestion
        )

    def _get_required_tier(self, category: ToolCategory) -> SecurityTier:
        """
        Get minimum required tier for a tool category.

        Args:
            category: Tool category

        Returns:
            Minimum SecurityTier required
        """
        if category == ToolCategory.EXTERNAL_API:
            return SecurityTier.GENERAL_LLM
        elif category == ToolCategory.FACTORY_API:
            return SecurityTier.CONFIDENTIAL_FAB
        elif category == ToolCategory.ONPREM_API:
            return SecurityTier.TOP_SECRET
        else:
            return SecurityTier.GENERAL_LLM

    def get_allowed_tools(self) -> List[str]:
        """
        Get list of allowed tools in current tier.

        Returns:
            List of tool names
        """
        allowed_categories = self.TIER_PERMISSIONS.get(self.current_tier, set())

        allowed_tools = [
            tool_name
            for tool_name, category in self.TOOL_CATEGORIES.items()
            if category in allowed_categories
        ]

        return sorted(allowed_tools)

    def get_violations_summary(self) -> str:
        """
        Get summary of violations in this session.

        Returns:
            Markdown-formatted violation summary
        """
        if not self.violations:
            return "No security violations in this session."

        lines = [
            f"# Security Violations ({len(self.violations)})",
            "",
            f"Current Tier: {self.current_tier.name}",
            ""
        ]

        for i, violation in enumerate(self.violations, 1):
            lines.extend([
                f"## Violation {i}",
                f"- **Tool:** {violation.tool_name}",
                f"- **Current Tier:** {violation.current_tier.name}",
                f"- **Required Tier:** {violation.required_tier.name}",
                f"- **Reason:** {violation.reason}",
                f"- **Suggestion:** {violation.suggestion}",
                ""
            ])

        return "\n".join(lines)


class SecurityViolationError(Exception):
    """Raised when a security tier violation occurs."""

    def __init__(self, violation: TierViolation):
        self.violation = violation
        message = (
            f"Security Violation: {violation.tool_name} not allowed in "
            f"{violation.current_tier.name} tier. {violation.suggestion}"
        )
        super().__init__(message)
