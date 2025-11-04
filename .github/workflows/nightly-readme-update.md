---
on:
  schedule:
    # Midnight EST (5 AM UTC), Monday-Friday
    - cron: "0 5 * * 1-5"
  workflow_dispatch:

permissions: read-all

safe-outputs:
  create-pull-request:
    title-prefix: "chore: Update README"

tools:
  edit:
  bash:
    - "git log:*"
    - "git diff:*"
    - "git status"

timeout_minutes: 10
---
# Nightly README Update

## Objective
Check if new changes were pushed to the repository since the last workflow run. If changes exist, scan the repository structure and update the README.md with current project information, then create a pull request. If no changes, exit gracefully.

## Instructions

### Step 1: Check for Recent Changes
- Use bash to get the latest commit timestamp: `git log -1 --format=%ct`
- Calculate if commits exist within the last 24 hours
- If no recent changes found, stop execution and exit with a message: "No new changes detected. Exiting."

### Step 2: Scan Repository Structure
If changes were detected:
- Analyze the `OpenAI-API/` directory structure
- Identify all subdirectories (projects) and root Python scripts
- For each project/script:
  - Read the main Python file(s)
  - Extract docstrings, comments, and README files (if present)
  - Determine the project's purpose and current status

### Step 3: Update README.md
Update the following sections in README.md using the `edit` tool:

1. **Project List**: Update the "Code that's Currently Here" section
   - Add any new projects discovered
   - Update existing project descriptions based on code analysis
   - Maintain status tags: *(API version upgrade COMPLETED)*, *(NEW!)*, *(IN DEVELOPMENT)*, *(ONGOING!)*, *(ON HOLD)*
   - Keep the original friendly, informative tone
   - Use `edit` tool with precise old_str/new_str replacements

2. **Last Updated Timestamp**: Add or update a "Last Updated" line at the very end of the README
   - Format: `**Last Updated:** YYYY-MM-DD`
   - If it already exists, use `edit` tool to update the date
   - If it doesn't exist, append it at the end using `edit` tool

**Important:** Make each edit separately using the `edit` tool. Do NOT generate git patches or diffs. Use direct file edits only.

### Step 4: Create Pull Request
After all edits are complete:
- Use the `create-pull-request` safe output
- Title: "chore: Update README with latest project information"
- Body should include:
  - Summary of changes detected
  - List of projects added/updated
  - Note that this is an automated update

## Guidelines
- Preserve the README's existing tone and style
- Don't modify the "Random Info" or "Learnings" sections
- Only update factual information about projects
- If a project has extensive inline documentation, prioritize that over assumptions
- Be concise but informative in project descriptions
