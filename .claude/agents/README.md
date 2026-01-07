# ATLASsemi Custom Agents

This directory can contain custom Claude Code agents specific to ATLASsemi workflows.

## Built-in Agents Available

From Continuous Claude v2 global installation:

- `general-purpose` - Research, search, multi-step tasks
- `Explore` - Fast codebase exploration
- `Plan` - Software architecture planning
- `repo-research-analyst` - Repository analysis
- And others...

## Future Custom Agents

Potential ATLASsemi-specific agents:

### 1. 8D Analyst Agent
**Purpose:** Specialized in reviewing 8D reports for completeness

```yaml
name: 8d-analyst
description: Reviews 8D reports for completeness and quality
tools:
  - Read
  - Grep
entry_point: .claude/agents/8d-analyst.md
```

### 2. Security Tier Advisor Agent
**Purpose:** Recommends appropriate security tier for a given problem

```yaml
name: security-tier-advisor
description: Recommends security tier based on problem description
tools:
  - Read
entry_point: .claude/agents/security-tier-advisor.md
```

### 3. Knowledge Graph Query Agent
**Purpose:** Searches knowledge graph for similar historical cases

```yaml
name: kg-query
description: Queries knowledge graph for relevant historical 8Ds
tools:
  - Bash
  - Read
entry_point: .claude/agents/kg-query.md
```

## Creating Custom Agents

See Continuous Claude documentation for agent creation patterns.

Agents are typically:
1. Markdown files with YAML frontmatter
2. Define allowed tools
3. Provide clear instructions and examples
