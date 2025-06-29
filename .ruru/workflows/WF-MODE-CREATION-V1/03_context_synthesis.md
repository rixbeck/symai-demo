+++
# --- Basic Metadata ---
id = "WF-MODE-CREATION-V1-03-CONTEXT-SYNTHESIS"
title = "Context Synthesis"
step_number = 3
workflow_id = "WF-MODE-CREATION-V1" # Added workflow ID
next_step_id = "WF-MODE-CREATION-V1-04-SAVE-CONTEXT" # Points to the next step file
prev_step_id = "WF-MODE-CREATION-V1-02-AI-ASSESSMENT" # Points to the previous step file
status = "active" # Updated status
created_date = "2025-04-29"
updated_date = "2025-04-29"
version = "1.0"
tags = ["workflow-step", "context-synthesis", "json", "delegation", "mode-creation", "mcp-preference", "synthesis-templates"]

# --- Workflow Step Specific Fields ---
description = "Delegates context synthesis to a specialized agent, using appropriate task templates to generate structured JSON output."
delegation_mode = "Context Synthesizer (e.g., agent-context-condenser)" # Primary mode responsible for this step
inputs = [
    "gathered_context_sources", # List[String]: From Step 01
    "mode_purpose",             # String: From Step 00
    "mode_classification"       # String: From Step 00
]
outputs = [
    "synthesized_context_json"  # String: JSON structure as a string, containing {filename: string, content: string} array
]
error_handling = "If agent fails to process context or use synthesis templates, retry. Check template validity. If persistent, notify User, consider manual synthesis or abandon." # Specific error handling for this step (optional)
related_docs = [
    ".ruru/templates/synthesis-task-sets/README.md"
]
related_templates = [
    ".ruru/templates/toml-md/25_workflow_step_standard.md",
    ".ruru/templates/synthesis-task-sets/*.toml"
]
template_schema_doc = ".ruru/templates/toml-md/25_workflow_step_standard.README.md"
+++

# Step 03: Context Synthesis

**Responsible Mode:** Coordinator (Roo Commander) delegates to **Context Synthesizer** (e.g., `agent-context-condenser`)

## Procedure

1.  **Delegate Task:**
    *   Coordinator instructs the Context Synthesizer agent (e.g., `agent-context-condenser`) to process the gathered information (output from **[Step 01](./01_context_gathering.md)**).

2.  **Instructions for Context Synthesizer:**
    *   The instructions provided by the Coordinator **MUST** include:
        *   The gathered context sources.
        *   The mode's purpose and classification (determined in **[Step 00](./00_start.md)**).
        *   Instruction to identify and use the appropriate `[type]-tasks.toml` template from `.ruru/templates/synthesis-task-sets/` based on the mode's purpose/classification (fallback to `generic-tasks.toml`).
        *   Instruction to identify and use the appropriate `[type]-tasks.toml` template from `.ruru/templates/synthesis-task-sets/` based on the mode's purpose/classification (fallback to `generic-tasks.toml`).
        *   Instruction to execute the synthesis tasks defined in the TOML template **iteratively**.
        *   Instruction to output the results as a **JSON structure**. This structure should be an array of objects, where each object contains `filename` and `content` keys.
            *   `filename`: Corresponds to the `output_filename` from the TOML task. **This should be a generic filename (e.g., `installation.md`, `usage.md`) without any subfolder path.** Step 09 will handle placing it in a subfolder if needed.
            *   `content`: The synthesized Markdown content for that file.
        *   Preference for using MCP tools where available, with the requirement to handle fallbacks gracefully.

3.  **Await Completion:**
    *   Coordinator awaits the completion signal and the resulting **JSON structure** from the Context Synthesizer.

4.  **Proceed:** Upon successful completion, proceed to the next step: **[04_save_context.md](./04_save_context.md)**.

## Error Handling
*   If the Context Synthesizer agent fails to process context or use the synthesis templates correctly:
    *   Coordinator should attempt to retry the delegation.
    *   Verify the validity of the selected synthesis template (`.toml` file).
    *   If failure persists, notify the User.
    *   Consider attempting manual synthesis or abandoning the workflow.