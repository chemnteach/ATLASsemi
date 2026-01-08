#!/usr/bin/env python3
"""
ATLASsemi Command-Line Interface

Main entry point for fab problem-solving workflow.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from atlassemi.agents.base import ProblemMode, SecurityTier
from atlassemi.orchestrator import WorkflowOrchestrator
from atlassemi.security.tier_enforcer import (
    TierEnforcer,
    SecurityViolationError
)
from atlassemi.config import ModelRouter, RuntimeMode
import os


def main():
    """Main CLI entry point."""
    print("=" * 60)
    print("ATLASsemi - Semiconductor Fab Problem-Solving Assistant")
    print("=" * 60)
    print()

    # Initialize model router
    runtime_mode_env = os.getenv("ATLASSEMI_RUNTIME_MODE", "dev")
    runtime_mode = RuntimeMode.RUNTIME if runtime_mode_env == "runtime" else RuntimeMode.DEV

    print(f"Runtime Mode: {runtime_mode.value.upper()}")
    print()

    model_router = ModelRouter(mode=runtime_mode)

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

    # Step 3: Narrative intake
    print("=" * 60)
    print("Narrative Intake")
    print("=" * 60)
    print()
    print("Describe your problem in free-form. Be as detailed as you like.")
    print("Include symptoms, observations, timeline, and any other context.")
    print()
    print("(Type your description, then press Ctrl+D on Unix "
          "or Ctrl+Z on Windows when done)")
    print()

    # Get user narrative
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
    print("Executing 4-Phase Workflow")
    print("=" * 60)
    print()

    # Initialize orchestrator
    orchestrator = WorkflowOrchestrator(model_router=model_router)

    # Execute full workflow
    try:
        result = orchestrator.run_workflow(
            narrative=narrative,
            mode=mode,
            tier=tier,
            answer_collector=None  # Use default CLI input
        )

        # Display results
        print("\n" + "=" * 60)
        print("WORKFLOW COMPLETE")
        print("=" * 60)
        print()

        # Summary statistics
        print("**Summary:**")
        print(f"  - Phases Completed: {len(result.phases_completed)}")
        print(f"  - Facts Identified: {result.facts_identified}")
        print(f"  - Hypotheses Generated: {result.hypotheses_identified}")
        print(f"  - 8D Phases Addressed: "
              f"{', '.join(result.eight_d_phases_addressed)}")
        print(f"  - Total Cost: ${result.total_cost_usd:.4f}")
        print()

        # Display key outputs
        print("\n" + "=" * 60)
        print("KEY FINDINGS")
        print("=" * 60)
        print()

        if result.narrative_output.facts:
            print("**Facts:**")
            for fact in result.narrative_output.facts:
                print(f"  - {fact}")
            print()

        if result.analysis_output.hypotheses:
            print("**Root Cause Hypotheses:**")
            for hypothesis in result.analysis_output.hypotheses:
                print(f"  - {hypothesis}")
            print()

        print("\n" + "=" * 60)
        print("PREVENTION PLAN")
        print("=" * 60)
        print()
        print(result.prevention_output.content)
        print()

    except Exception as e:
        print(f"Error during workflow execution: {e}")
        print()
        import traceback
        traceback.print_exc()
        print()
        print("Your narrative has been recorded:")
        print()
        print(narrative)
        print()

    # Show usage summary
    print("\n" + "=" * 60)
    print("Session Usage Summary")
    print("=" * 60)
    print()
    print(model_router.get_usage_summary())
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
