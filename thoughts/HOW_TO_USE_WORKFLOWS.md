# How to Use Workflows for Technical Debt Management

Quick reference guide for using the workflow system to ensure technical debt is addressed at the right time.

---

## The Problem We're Solving

**Question:** "How do we remember to address technical debt (like test coverage) when we start v2.0?"

**Answer:** Use the **Release Planning Workflow** that systematically reviews debt before any major release.

---

## The Three-Part System

### 1. Technical Debt Inventory
**File:** `TECHNICAL_DEBT.md`

This is your passive documentation - a list of all known debt with:
- What's deferred
- Why it's deferred
- When to address it (trigger conditions)
- How to implement it

### 2. Release Planning Workflow
**File:** `thoughts/workflows/RELEASE_PLANNING.md`

This is your process - 8 steps to follow when planning any major release:
- **Step 2 is MANDATORY:** Review technical debt
- Identifies triggered items
- Forces decision: address now or justify deferral

### 3. Release Ledger Template
**File:** `thoughts/ledgers/TEMPLATE-major-release.md`

This is your enforcement mechanism - copy this to start v2.0:
- References the workflow in YAML header
- Claude sees it and follows the workflow
- Prevents skipping debt review

---

## How It Works in Practice

### Starting v2.0 (The Right Way)

**Step 1: Copy the template**
```bash
cp thoughts/ledgers/TEMPLATE-major-release.md \
   thoughts/ledgers/CONTINUITY_CLAUDE-v2.0-release.md
```

**Step 2: Edit the copy**
```yaml
---
session_name: v2.0-release
workflow: thoughts/workflows/RELEASE_PLANNING.md  # This is the key!
---
```

**Step 3: Start Claude session**
```
You: "Let's start planning v2.0"

Claude: *loads ledger*
Claude: "I see this ledger references Release Planning Workflow.
        I'll follow that workflow.

        Step 1: Review Current State
        [runs tests, checks git, reads ledger]

        Step 2: Technical Debt Review (MANDATORY)
        [reads TECHNICAL_DEBT.md]

        I found the following triggered debt items:

        1. Increase test coverage to 90%
           Trigger: 'Before v2.0 release' ✅ TRIGGERED
           Effort: 1-2 days
           Priority: MUST address

        Before we define v2.0 scope, we need to decide:
        - Should we address this debt first?
        - Include it in v2.0 timeline?
        - Or justify deferring it?"

You: "Yes, let's address it as part of v2.0"

Claude: "Great. I'll include that in the release plan.

        Step 3: Define Release Scope
        What new features should v2.0 include?
        (I'll add test coverage improvement to the plan)"
```

**The key:** Claude **can't proceed** without addressing Step 2 because:
- The ledger references the workflow
- The workflow makes Step 2 mandatory
- Claude follows the workflow systematically

---

## What Happens at Each Stage

### 🚀 During Planning (Steps 1-6)

**Step 2: Technical Debt Review**
1. Claude reads `TECHNICAL_DEBT.md`
2. For each item, checks if trigger conditions are met
3. Creates categorized list:
   - TRIGGERED (must address or justify deferring)
   - NOT TRIGGERED (safely deferred)

**Step 3: Define Scope**
- User provides new features
- Claude adds triggered debt items
- Scope = features + debt

**Step 5: Create Release Plan**
- Phases include both features AND debt resolution
- Plan document includes debt tracking

### ⚙️ During Implementation (Step 7)

Claude updates the release ledger:
```markdown
## State
- Done:
  - [x] Technical debt: Test coverage to 90%
  - [x] Feature A
- Now: [→] Feature B
```

### ✅ During Completion (Step 8)

Claude updates `TECHNICAL_DEBT.md`:
```markdown
## Resolved Technical Debt

### v2.0 Resolution (2026-XX-XX)

**Increase test coverage to 90%** ✅
- Was: 77% coverage
- Now: 92% coverage
- Commit: abc1234
- Resolved by: v2.0 release
```

---

## Why This Works Better Than Reminders

### Traditional Approach (Unreliable):
```
You: Set calendar reminder "Check technical debt"
     [3 months later]
     Did I remember to check? What was I supposed to check?
```

### Workflow Approach (Systematic):
```
You: Copy template ledger for v2.0
Claude: *sees workflow reference in ledger*
Claude: "Following Release Planning Workflow..."
Claude: "Step 2: Reading TECHNICAL_DEBT.md..."
Claude: "Found triggered item: test coverage..."
```

**Advantages:**
- ✅ Can't be forgotten (enforced by template)
- ✅ Systematic (same process every time)
- ✅ Documented (creates artifacts as it goes)
- ✅ Transferable (new team members follow same workflow)

---

## When Claude WILL Mention Technical Debt

### ✅ Guaranteed:
1. **When using the release ledger template**
   - Workflow reference forces Step 2
   - Claude must review debt before proceeding

2. **When you explicitly ask**
   - "What technical debt do we have?"
   - "Should we address test coverage now?"

### ⚠️ Likely (but not guaranteed):
1. **When working on related features**
   - You: "Let's add Factory API"
   - Claude *might* notice: "TECHNICAL_DEBT.md says to address
     test coverage when adding Tier 2 APIs"

   (Depends on Claude making the connection)

### ❌ Won't happen:
1. **When working on unrelated tasks**
   - You: "Fix typo in README"
   - Claude: *proceeds with fix, doesn't mention debt*

   (Correct behavior - debt isn't blocking this work)

---

## Quick Reference Commands

### Check Technical Debt
```bash
cat TECHNICAL_DEBT.md
```

### Start v2.0 Planning
```bash
# 1. Copy template
cp thoughts/ledgers/TEMPLATE-major-release.md \
   thoughts/ledgers/CONTINUITY_CLAUDE-v2.0-release.md

# 2. Edit version numbers in the copy

# 3. Tell Claude:
"Let's start planning v2.0"
```

### Check Workflow
```bash
cat thoughts/workflows/RELEASE_PLANNING.md
```

### See What Debt is Triggered
```bash
# Look for items with trigger: "Before v2.0"
grep -A 3 "When:" TECHNICAL_DEBT.md
```

---

## Example: Full v2.0 Flow

### Week 1: Planning

```bash
# Copy template
cp thoughts/ledgers/TEMPLATE-major-release.md \
   thoughts/ledgers/CONTINUITY_CLAUDE-v2.0-release.md
```

```
You: "Let's start planning v2.0"

Claude: [Follows workflow]
        [Step 2: Reviews TECHNICAL_DEBT.md]
        [Identifies: Test coverage triggered]
        [Creates comprehensive release plan]
        [Includes both features AND debt]
```

### Weeks 2-3: Implementation

```
Claude: [Works through plan phases]
        [Updates ledger as work completes]
        [Marks debt items as resolved]
```

### Week 4: Release

```
Claude: [Step 8: Release completion]
        [Updates TECHNICAL_DEBT.md - marks item resolved]
        [Tags v2.0 in git]
        [Creates release notes]
```

**Result:**
- ✅ Test coverage now at 92%
- ✅ Debt resolved and documented
- ✅ v2.0 shipped with no forgotten work

---

## FAQ

### Q: What if I forget to copy the template?

**A:** The debt is still in TECHNICAL_DEBT.md. If you say "let's start v2.0", Claude might mention it (but not guaranteed). Better to use the template.

### Q: Can I skip the workflow for minor releases (v1.1)?

**A:** Yes. The workflow is for major releases (v2.0, v3.0). For minor versions:
- Optionally review TECHNICAL_DEBT.md manually
- Use abbreviated planning
- Full workflow not required

### Q: What if I want to defer triggered debt?

**A:** That's fine! The workflow forces you to make a **conscious decision**:
- Address it now, OR
- Document why you're deferring it

The point is: don't accidentally forget it.

### Q: Does this work for other projects?

**A:** Yes! The pattern is reusable:
1. TECHNICAL_DEBT.md with trigger conditions
2. Workflow document with mandatory debt review
3. Release template that references the workflow

---

## Summary

**The magic is in the template ledger:**

```yaml
workflow: thoughts/workflows/RELEASE_PLANNING.md
```

This one line ensures Claude:
1. Loads the workflow
2. Follows it systematically
3. Can't skip Step 2 (debt review)
4. Forces conscious decisions about debt

**When you start v2.0:**
- Copy the template
- Tell Claude "let's start planning v2.0"
- Claude does the rest

---

**Created:** 2026-01-07
**Last Updated:** 2026-01-07
