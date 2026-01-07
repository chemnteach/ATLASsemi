#!/usr/bin/env python3
"""
ATLASsemi Command-Line Interface

Main entry point for fab problem-solving workflow.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from atlassemi.agents.base import ProblemMode, SecurityTier, AgentInput
from atlassemi.agents.narrative_agent import NarrativeAgent
from atlassemi.security.tier_enforcer import TierEnforcer, SecurityViolationError


def main():
    """Main CLI entry point."""
    print("=" * 60)
    print("ATLASsemi - Semiconductor Fab Problem-Solving Assistant")
    print("=" * 60)
    print()

    # Step 1: Select mode
    print("Problem-Solving Mode:")
    print("  1. Yield Excursion Response (fast containment)")
    print("  2. Yield Improvement (continuous improvement)")
    print("  3. Factory Operations (sustainment)")
    print()

    mode_choice = input("Select mode [1-3]: ").strip()

    mode_map = {
        "1": ProblemMode.EXCURSION,
        "2": ProblemMode.IMPROVEMENT,
        "3": ProblemMode.OPERATIONS,
    }

    mode = mode_map.get(mode_choice)
    if mode is None:
        print("Invalid mode selection.")
        return

    print(f"\nMode: {mode.value}")
    print()

    # Step 2: Select security tier
    print("Security Tier:")
    print("  1. General LLM (public knowledge only)")
    print("  2. Confidential Fab (factory API access)")
    print("  3. Top Secret (on-prem only)")
    print()

    tier_choice = input("Select tier [1-3]: ").strip()

    tier_map = {
        "1": SecurityTier.GENERAL_LLM,
        "2": SecurityTier.CONFIDENTIAL_FAB,
        "3": SecurityTier.TOP_SECRET,
    }

    tier = tier_map.get(tier_choice)
    if tier is None:
        print("Invalid tier selection.")
        return

    print(f"\nSecurity Tier: {tier.name}")
    print()

    # Initialize tier enforcer
    enforcer = TierEnforcer(current_tier=tier)
    print(f"Allowed tools in this tier: {', '.join(enforcer.get_allowed_tools())}")
    print()

    # Step 3: Narrative intake (Phase 0)
    print("=" * 60)
    print("Phase 0: Narrative Intake")
    print("=" * 60)
    print()

    narrative_agent = NarrativeAgent()
    print(narrative_agent.generate_intake_prompt())
    print()

    # Get user narrative
    print("(Type your description, then press Ctrl+D on Unix or Ctrl+Z on Windows when done)")
    print()

    narrative_lines = []
    try:
        while True:
            line = input()
            narrative_lines.append(line)
    except EOFError:
        pass

    narrative = "\n".join(narrative_lines).strip()

    if not narrative:
        print("\nNo narrative provided. Exiting.")
        return

    print()
    print("=" * 60)
    print("Processing narrative...")
    print("=" * 60)
    print()

    # Create agent input
    agent_input = AgentInput(
        mode=mode,
        security_tier=tier,
        context={"narrative": narrative}
    )

    # Execute narrative agent (in real implementation, this would call LLM)
    print("[Note: In this initial version, LLM integration is not yet complete]")
    print("[Narrative analysis would appear here]")
    print()
    print("Your narrative has been recorded:")
    print()
    print(narrative)
    print()

    # Next steps
    print("=" * 60)
    print("Next Steps")
    print("=" * 60)
    print()
    print("1. Implement model router for LLM calls")
    print("2. Phase 1: Adaptive clarification questions")
    print("3. Phase 2: Analysis with 8D mapping")
    print("4. Phase 3: Prevention and documentation")
    print()
    print("This is the initial ATLASsemi structure.")
    print("Core agents and security enforcement are in place.")
    print()


if __name__ == "__main__":
    try:
        main()
    except SecurityViolationError as e:
        print()
        print("=" * 60)
        print("SECURITY VIOLATION")
        print("=" * 60)
        print()
        print(str(e))
        print()
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print()
        print("=" * 60)
        print("ERROR")
        print("=" * 60)
        print()
        print(f"An error occurred: {e}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)
