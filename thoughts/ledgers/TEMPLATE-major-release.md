# Continuity Ledger: [Version] Release

**TEMPLATE: Copy this when starting a major release (v2.0, v3.0, etc.)**

```yaml
---
session_name: v2.0-release  # Change version number
problem_mode: operations
security_tier: general_llm  # Or appropriate tier
api_routing: anthropic
started: YYYY-MM-DD
last_updated: YYYY-MM-DD HH:MM
workflow: thoughts/workflows/RELEASE_PLANNING.md  # MANDATORY
---
```

## Goal

Release [Version Number] with:
- [Feature 1]
- [Feature 2]
- [Technical Debt Items - see below]

**Success Criteria:**
- All new features implemented and tested
- All TRIGGERED technical debt addressed (see Step 2 of workflow)
- Test coverage meets target (specify %)
- Documentation updated
- Ready to deploy to production

## Constraints

- **MANDATORY:** Must follow Release Planning Workflow (thoughts/workflows/RELEASE_PLANNING.md)
- **MANDATORY:** Must complete Step 2 (Technical Debt Review) before defining scope
- **Security Tier:** [Specify tier for this work]
- **Dependencies:** [List external dependencies]
- **Timeline:** [If applicable]

## State

**IMPORTANT:** Do not start implementation until Release Planning Workflow is complete!

- Pre-Planning:
  - [ ] Step 1: Review Current State (workflow)
  - [ ] Step 2: Technical Debt Review (workflow) ⚠️ MANDATORY
  - [ ] Step 3: Define Release Scope (workflow)
  - [ ] Step 4: Effort Estimation (workflow)
  - [ ] Step 5: Create Release Plan (workflow)
  - [ ] Step 6: User Approval (workflow)

- Implementation:
  - [ ] [Phase 1 from release plan]
  - [ ] [Phase 2 from release plan]
  - [ ] [Technical debt items]

- Completion:
  - [ ] Step 8: Release Completion (workflow)
  - [ ] All tests passing
  - [ ] Coverage target met
  - [ ] Documentation updated
  - [ ] Version tagged in git

## Technical Debt Resolution

**Source:** TECHNICAL_DEBT.md (read during Step 2 of workflow)

### Triggered by This Release:
*Fill this in during Step 2 of Release Planning Workflow*

Example:
- [ ] Increase test coverage to 90%
  - Trigger: "Before v2.0 release" ✅ TRIGGERED
  - Effort: 1-2 days
  - Priority: MUST address

### Not Triggered (Deferred):
*List items reviewed but not applicable*

Example:
- Knowledge Graph integration
  - Trigger: "When ready to implement"
  - Status: Not triggered by v2.0 scope
  - Deferred to: v3.0 or later

## Key Decisions

*Document decisions made during planning and implementation*

1. **Decision:** [Decision name]
   - **Rationale:** [Why]
   - **Impact:** [Effect on release]

## Open Questions

*Track questions that need answers before proceeding*

- UNCONFIRMED: [Question that needs resolution]

## Working Set

**Branch:** [branch name]

**Release Plan:** thoughts/shared/plans/YYYY-MM-DD-v2.0-release.md

**Key Commands:**
```bash
# Run tests
pytest tests/ -v

# Check coverage
pytest --cov=atlassemi --cov-report=html

# Review technical debt
cat TECHNICAL_DEBT.md

# Follow release workflow
cat thoughts/workflows/RELEASE_PLANNING.md
```

## Progress Notes

### [Date] - Planning Phase

**Started Release Planning Workflow:**

**Step 1: Current State Review:**
- Version: [current version]
- Tests: [X passing, Y% coverage]
- Git: [status]

**Step 2: Technical Debt Review:**
- Read TECHNICAL_DEBT.md
- Identified triggered items:
  1. [Item 1 - trigger met]
  2. [Item 2 - trigger met]
- Deferred items:
  1. [Item 3 - not triggered]

**Step 3: Release Scope:**
[Define after Step 2 complete]

**Step 4: Effort Estimation:**
[Calculate after scope defined]

**Step 5-6: Plan & Approval:**
[Create plan and get user approval]

### [Date] - Implementation Phase

[Track progress as work proceeds]

### [Date] - Completion

[Final status and release]

## Cost Tracking

**Planning Phase:** $[amount]
**Implementation Phase:** $[amount]
**Total Release Cost:** $[amount]

## Security Notes

**Current Tier:** [Specify]

**Data Handling:**
- [Note any security considerations]

## Technical Notes

[Architecture decisions, patterns followed, etc.]

---

## HOW TO USE THIS TEMPLATE

### 1. When Starting a Major Release:

```bash
# Copy this template
cp thoughts/ledgers/TEMPLATE-major-release.md \
   thoughts/ledgers/CONTINUITY_CLAUDE-v2.0-release.md

# Edit the copy:
# - Change version numbers
# - Update dates
# - Keep workflow reference
```

### 2. First Session Message:

```
You: "Let's start planning v2.0"

Claude: *loads ledger*
Claude: "I see this ledger references the Release Planning Workflow.
        I'll follow that workflow to ensure we review technical
        debt before defining scope. Starting with Step 1..."
```

### 3. Claude Will Automatically:

- See `workflow: thoughts/workflows/RELEASE_PLANNING.md` in YAML
- Read the workflow document
- Follow the steps systematically
- MANDATORY Step 2: Review technical debt
- Prevent skipping debt review

### 4. Progress Tracking:

Update the State section as you complete each step:
```markdown
- Pre-Planning:
  - [x] Step 1: Review Current State ✓
  - [x] Step 2: Technical Debt Review ✓
  - [x] Step 3: Define Release Scope ✓
  - [ ] Step 4: Effort Estimation (in progress)
```

---

**Template Version:** 1.0
**Created:** 2026-01-07
**Use For:** All major version releases (v2.0, v3.0, v4.0, etc.)
