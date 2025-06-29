+++
# --- Task/Story/Bug Metadata ---
id = "TASK-IM-501"
title = "Create mode definition file `roo-dispatch.mode.md`"
status = "⚪️ Planned"
type = "🛠️ Task"
created_date = "2025-04-28" # Use current date
updated_date = "2025-04-28" # Use current date
project_name = "intellimanage_implementation"
feature_id = "FEAT-IM-005"
# epic_id = "EPIC-IM-001" # Implied via Feature
# assigned_to = "..."
# reporter = "..."
priority = "🔥 Highest" # Foundational for the mode
# estimated_effort = "S" # Small - primarily creating and populating a definition file
# due_date = "YYYY-MM-DD"
# sprint_id = "..."
tags = ["mode", "roo-dispatch", "definition", "configuration", "setup", "coordination"]
related_docs = ["MODE-SPEC-ROO-DISPATCH-001"]
depends_on = [] # No code dependency, just the spec
# related_commits = []
# related_prs = []
# related_issues = []
+++

# Task: Create mode definition file `roo-dispatch.mode.md`

## Description ✍️

Create the actual `.mode.md` file for the `roo-dispatch` mode. This involves creating the file in the appropriate location within the Roo Code modes directory structure (e.g., `.ruru/modes/roo-dispatch/roo-dispatch.mode.md`) and populating it with the TOML frontmatter and initial Markdown documentation based *exactly* on the specification defined in `MODE-SPEC-ROO-DISPATCH-001`.

This task is about creating the static definition file; implementing the actual *logic* described within it will be covered in subsequent tasks.

## Acceptance Criteria ✅

*   - [ ] The file `.ruru/modes/roo-dispatch/roo-dispatch.mode.md` exists.
*   - [ ] The TOML frontmatter within the file accurately reflects all fields specified in `MODE-SPEC-ROO-DISPATCH-001` (id, name, version, classification, domain, sub_domain, summary, system_prompt, allowed_tool_groups, file_access, metadata, custom_instructions_dir).
*   - [ ] The system prompt in the TOML frontmatter matches the one defined in the specification.
*   - [ ] The initial Markdown content (sections like Description, Capabilities, Workflow, Limitations, Rationale) is copied or accurately represented from `MODE-SPEC-ROO-DISPATCH-001`.
*   - [ ] The file is correctly formatted (TOML syntax, Markdown syntax).
*   - [ ] The file is added to version control (Git).

## Implementation Notes / Details 📝

*   This is primarily a copy-paste and formatting task based on the approved specification document (`MODE-SPEC-ROO-DISPATCH-001`).
*   Ensure the file path and naming conventions match the Roo Code standards for mode definitions.
*   Double-check TOML syntax, especially for arrays and multi-line strings (system prompt). Pay attention to the `allowed_tool_groups` and `file_access` sections.

## Subtasks / Checklist ☑️

*   - [ ] Create the directory `.ruru/modes/roo-dispatch/`.
*   - [ ] Create the file `roo-dispatch.mode.md` within the directory.
*   - [ ] Copy and paste the TOML frontmatter from `MODE-SPEC-ROO-DISPATCH-001` into the file.
*   - [ ] Verify all TOML fields and values are correct.
*   - [ ] Copy and paste the Markdown documentation sections from `MODE-SPEC-ROO-DISPATCH-001` below the TOML frontmatter.
*   - [ ] Verify Markdown formatting.
*   - [ ] Add the new file to Git staging.