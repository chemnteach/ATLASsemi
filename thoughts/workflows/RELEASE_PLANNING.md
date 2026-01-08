# Release Planning Workflow

This workflow ensures systematic review of technical debt, dependencies, and readiness before starting work on a major release.

**Use this workflow when:**
- Planning v2.0, v3.0, etc. (major versions)
- Planning significant feature releases
- Before production deployments

---

## Step 1: Review Current State

### 1.1 Check Continuity Ledger

```bash
# Read most recent ledger
cat thoughts/ledgers/CONTINUITY_CLAUDE-*.md

# Verify:
# - What version are we at?
# - What's the status of previous release?
# - Any incomplete work from last session?
```

### 1.2 Verify Production Status

```bash
# Run full test suite
pytest tests/ -v

# Check coverage
pytest --cov=atlassemi --cov-report=term-missing

# Verify all tests passing
# Note current coverage percentage
```

### 1.3 Review Git Status

```bash
# Check for uncommitted changes
git status

# Review recent commits
git log --oneline -n 10

# Check branch status
git branch -a
```

---

## Step 2: Technical Debt Review (MANDATORY)

### 2.1 Read Technical Debt Document

```bash
# Read full technical debt inventory
cat TECHNICAL_DEBT.md
```

**Ask yourself:**
- What technical debt is marked "High Priority"?
- Are any trigger conditions met?
- Does this release depend on addressing any debt?

### 2.2 Check Triggered Debt Items

For each item in TECHNICAL_DEBT.md, check if triggers are met:

**Example Decision Tree:**
```
Item: "Increase test coverage to 90%"
Trigger: "Before v2.0 release"
Current: Planning v2.0

→ TRIGGERED: This must be addressed before v2.0
```

### 2.3 Prioritize Debt for This Release

Create a list:
```markdown
## Technical Debt to Address in This Release

### Must Address (Blocking):
- [ ] Item 1 (trigger: before v2.0)
- [ ] Item 2 (trigger: when adding Factory API)

### Should Address (Non-blocking but valuable):
- [ ] Item 3 (good opportunity)

### Deferred to Future:
- [ ] Item 4 (not related to this release)
```

---

## Step 3: Define Release Scope

### 3.1 Core Features

```markdown
## v2.0 Core Features
1. Feature A - [description]
2. Feature B - [description]
3. Feature C - [description]
```

### 3.2 Technical Debt Resolution

```markdown
## Technical Debt Resolution (from Step 2)
1. Increase test coverage to 90%
2. Add Factory API integration tests
3. [Other triggered items]
```

### 3.3 Dependencies

```markdown
## Dependencies Required
- [ ] Factory API endpoint access
- [ ] API keys for integration tests
- [ ] [Other external dependencies]
```

---

## Step 4: Effort Estimation

### 4.1 Estimate Each Component

| Component | Type | Estimated Effort | Dependencies |
|-----------|------|-----------------|--------------|
| Feature A | New | 3-5 days | None |
| Test coverage increase | Debt | 1-2 days | API keys |
| Feature B | New | 2-3 days | Factory API |
| ... | ... | ... | ... |

### 4.2 Calculate Total

- **New Features:** X days
- **Technical Debt:** Y days
- **Testing & Documentation:** Z days
- **Total:** X+Y+Z days

---

## Step 5: Create Release Plan

### 5.1 Generate Plan Document

```bash
# Create release plan
# Use naming: thoughts/shared/plans/YYYY-MM-DD-v2.0-release.md

# Structure:
# - Overview
# - Technical Debt to Address (from Step 2)
# - New Features
# - Dependencies
# - Implementation Phases
# - Testing Strategy
# - Documentation Updates
# - Deployment Plan
```

### 5.2 Create Release Ledger

```bash
# Create new continuity ledger for this release
# thoughts/ledgers/CONTINUITY_CLAUDE-v2.0-release.md

# Include:
# - Goal: v2.0 Release with [features]
# - Constraints: Must address [technical debt items]
# - State: Checklist of all work
# - Technical Debt Section: References items being addressed
```

---

## Step 6: Validate with User

### 6.1 Present Summary

```markdown
## v2.0 Release Plan Summary

**Scope:**
- 3 new features
- 2 technical debt items (triggered by this release)

**Technical Debt Being Addressed:**
1. Increase test coverage to 90% (trigger: before v2.0)
2. Factory API integration tests (trigger: adding Factory API)

**Technical Debt Deferred:**
1. Item X (reason: not related to v2.0 scope)

**Estimated Effort:** 10-15 days

**Dependencies:**
- Factory API access (confirmed available)
- API keys for integration tests (need to obtain)

**Ready to proceed?**
```

### 6.2 Get Confirmation

Wait for user approval before proceeding to implementation.

---

## Step 7: Execute Release

### 7.1 Follow Implementation Plan

Execute the plan created in Step 5.1, phase by phase.

### 7.2 Update Ledger as You Go

Mark items complete in the release ledger:
```markdown
## State
- Done:
  - [x] Technical debt: Test coverage to 90%
  - [x] Feature A implementation
- Now: [→] Feature B implementation
- Next: Feature C implementation
```

### 7.3 Track Technical Debt Resolution

As debt items are completed, update TECHNICAL_DEBT.md:
```markdown
## Resolved Technical Debt

### v2.0 Resolution

**Increase test coverage to 90%** (Resolved 2026-XX-XX)
- Was: 77% coverage
- Now: 92% coverage
- Commit: abc1234
```

---

## Step 8: Release Completion

### 8.1 Verify All Debt Addressed

```bash
# Re-read TECHNICAL_DEBT.md
cat TECHNICAL_DEBT.md

# Verify:
# - All triggered items marked as resolved
# - No high-priority items left unaddressed
```

### 8.2 Update Version Numbers

```bash
# Update README.md version
# Update package version files
# Update CLAUDE.md
```

### 8.3 Final Testing

```bash
# Run full test suite
pytest tests/ -v

# Run coverage check
pytest --cov=atlassemi --cov-report=html

# Manual testing per docs/TESTING.md
```

### 8.4 Create Release Commit

```bash
git commit -m "Release v2.0 with [features] and technical debt resolution"
git tag v2.0.0
git push origin main --tags
```

---

## Checklist Template

Use this checklist at the start of any major release:

```markdown
## Release Planning Checklist

### Step 1: Review Current State
- [ ] Read continuity ledger
- [ ] Run tests (verify all passing)
- [ ] Check coverage (note current %)
- [ ] Review git status

### Step 2: Technical Debt Review (MANDATORY)
- [ ] Read TECHNICAL_DEBT.md in full
- [ ] Identify triggered items for this release
- [ ] Categorize: Must/Should/Deferred
- [ ] Estimate effort for debt resolution

### Step 3: Define Release Scope
- [ ] List core features
- [ ] List technical debt to resolve
- [ ] Identify dependencies

### Step 4: Effort Estimation
- [ ] Estimate each component
- [ ] Calculate total effort
- [ ] Assess feasibility

### Step 5: Create Release Plan
- [ ] Generate plan document
- [ ] Create release ledger
- [ ] Include technical debt tracking

### Step 6: Validate with User
- [ ] Present summary
- [ ] Get approval to proceed

### Step 7: Execute Release
- [ ] Follow implementation plan
- [ ] Update ledger as you go
- [ ] Track debt resolution

### Step 8: Release Completion
- [ ] Verify all triggered debt addressed
- [ ] Update version numbers
- [ ] Final testing
- [ ] Create release commit and tag
```

---

## Example: Starting v2.0

```
User: "Let's start planning v2.0"

Claude: "I'll follow the Release Planning Workflow. Let me start:

**Step 1: Review Current State**
[reads ledger, runs tests, checks git]

Current state:
- Version: 1.0.0 (production ready)
- Tests: 25 passing, 77% coverage
- Git: Clean, all changes committed

**Step 2: Technical Debt Review (MANDATORY)**
[reads TECHNICAL_DEBT.md]

Found triggered debt:
1. ⚠️ 'Increase test coverage to 90%'
   - Trigger: Before v2.0 release
   - Status: TRIGGERED - must address
   - Effort: 1-2 days

2. 'Factory API integration'
   - Trigger: When adding Factory API
   - Status: Check if v2.0 includes Factory API

**Step 3: Define Release Scope**

Before I proceed, I need to understand:
1. What features are planned for v2.0?
2. Does v2.0 include Factory API integration?

Based on your answers, I'll complete the debt review and create
the full release plan."
```

---

## When to Use This Workflow

### Always Use For:
- Major version releases (v2.0, v3.0, etc.)
- Production deployments
- Significant feature additions

### Optional For:
- Minor version updates (v1.1, v1.2) - use abbreviated version
- Bug fixes - skip if no debt is triggered
- Documentation-only changes - skip

### Required Sections:
- Step 2 (Technical Debt Review) is MANDATORY for all major releases
- Other steps can be adapted based on release size

---

## Integration with Continuous Claude

### Skill Integration (Future)

This workflow could become a skill:
```
User: "/plan-release v2.0"

Skill: Automatically executes this workflow
- Reads technical debt
- Identifies triggered items
- Creates checklist
- Prompts for scope definition
- Generates release plan
```

### Ledger Integration

When starting v2.0 work, the release ledger should include:
```yaml
---
session_name: v2.0-release
constraints:
  - Must follow Release Planning Workflow
  - Must address all triggered technical debt
workflow: thoughts/workflows/RELEASE_PLANNING.md
---
```

---

**Last Updated:** 2026-01-07
**Next Review:** When planning v2.0 or next major release
