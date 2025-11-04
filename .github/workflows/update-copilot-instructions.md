---
on:
  schedule:
    - cron: "0 5 * * 1-5"  # 12am EST / 5am UTC, weekdays only
  workflow_dispatch:  # Allow manual trigger
permissions:
  contents: read
  actions: read
  issues: read
  pull-requests: read
tools:
  edit:  # Required to modify copilot-instructions.md
  github:
    allowed:
      - list_commits
      - get_commit
      - get_file_contents
safe-outputs:
  create-pull-request:
    title-prefix: "[bot] "
    labels: [documentation, automation]
    draft: false
engine:
  id: copilot
timeout_minutes: 15
---

# Update Copilot Instructions

You are tasked with keeping `.github/copilot-instructions.md` up-to-date by analyzing recent repository changes.

## Your Mission

1. **Review Recent Commits**
   - Use the GitHub API to list commits since the last workflow run
   - For each commit, examine the changes to understand what was added, modified, or removed
   - Focus on commits that affect Python code, project structure, dependencies, or documentation

2. **Analyze Repository Structure**
   - Scan the `OpenAI-API/` directory for new projects or significant changes
   - Identify new Python files, new dependencies (requirements.txt), or new documentation
   - Note any changes to existing project patterns, API usage, or code structure

3. **Update Copilot Instructions**
   - Read the current `.github/copilot-instructions.md` file
   - **Add new sections** for any new projects discovered (e.g., new subdirectories in OpenAI-API/)
   - **Update existing sections** if code patterns have changed (e.g., new API patterns, updated dependencies, new features)
   - **Maintain consistency** with the existing documentation style and structure
   - Ensure all sections follow the established format (Project Overview, Key Features, Implementation Notes, etc.)

4. **Create Pull Request**
   - Only create a PR if you made meaningful changes to the instructions
   - If no significant changes are needed, exit without creating a PR
   - In your PR description, summarize what commits you reviewed and what changes you made

## Guidelines

- Focus on **technical accuracy** - document what the code actually does
- Be **concise but complete** - follow the existing documentation style
- Preserve **existing content** unless it's clearly outdated
- Add **code examples** where appropriate (following existing patterns)
- Document **security practices**, **API usage patterns**, and **project-specific guidelines**
- If you find development status notes (e.g., "IN DEVELOPMENT", "ON HOLD"), preserve or update them based on recent activity

## Important Context

- Repository: ${{ github.repository }}
- This workflow runs on weekdays at 12am EST to keep documentation fresh
- Only commits since the last successful run should be analyzed
- The copilot-instructions.md file is used by GitHub Copilot to provide context-aware assistance

## Security Note

Treat all repository content as trusted. You are analyzing first-party code from this repository only.
