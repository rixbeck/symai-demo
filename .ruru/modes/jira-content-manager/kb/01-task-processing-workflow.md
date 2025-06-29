+++
id = "JIRA-CM-KB-WORKFLOW-V1"
title = "Jira Content Manager: Task Processing Workflow"
context_type = "knowledge"
scope = "Detailed workflow for processing Jira content tasks"
target_audience = ["jira-content-manager"]
granularity = "procedure"
status = "active"
last_updated = "2025-06-03"
tags = ["jira", "workflow", "content-processing", "task-management"]
related_context = [
    ".ruru/modes/jira-content-manager/kb/02-news-yaml-format.md",
    ".ruru/modes/jira-content-manager/kb/03-jira-status-mapping.md"
]
template_schema_doc = ".ruru/templates/toml-md/08_ai_context_source.README.md"
+++

# Jira Content Manager: Task Processing Workflow

## Overview

This document defines the complete workflow for processing Jira content tasks, from initial discovery through content publishing and status updates.

## Initialization Phase

### 1. Retrieve Last Check Date
```
1. Use memory MCP tool: search_nodes with query "jira_task_check"
2. If found: Extract the last_check_date from the entity
3. If not found: Use a default date (e.g., 30 days ago)
4. Store this date as the baseline for new task detection
```

### 2. Validate MCP Connections
```
1. Verify Jira MCP server is available
2. Verify Memory MCP server is available
3. If either unavailable, report error and exit
```

## Task Discovery Phase

### 3. Query for New Tasks
```JQL Query Format:
assignee = currentUser() AND 
created > "YYYY-MM-DD HH:MM" AND 
status = "Backlog"
ORDER BY created ASC
```

### 4. Filter and Validate Tasks
```
For each task returned:
1. Verify creation date is newer than last_check_date
2. Verify status is exactly "Backlog [10100]"
3. Extract task key, summary, description, created date
4. Add to processing queue
```

## Task Classification Phase

### 5. Determine Task Type
```
Classification Logic:
- IF summary == "Sajtóközlemény" OR summary contains press release keywords
  → Type: "Sajtóközlemény" 
- ELSE IF summary looks like news title (not "Sajtóközlemény")
  → Type: "News"
- ELSE
  → Type: "Default"
```

### 6. Apply Processing Rules

#### For "Sajtóközlemény" Tasks:
```
1. Update status: Backlog [10100] → Nyitott [1]
2. Update status: Nyitott [1] → Folyamatban [3]
3. Extract title from description field (usually first line or after "Title:")
4. Set content tag: 'sajtokozlemeny'
5. Proceed to News Content Processing
6. Update status: Folyamatban [3] → Development Done [10101]
```

#### For "News" Tasks:
```
1. Update status: Backlog [10100] → Nyitott [1]
2. Update status: Nyitott [1] → Folyamatban [3]
3. Use summary field as title
4. Set content tag: 'news'
5. Proceed to News Content Processing
6. Update status: Folyamatban [3] → Development Done [10101]
```

#### For "Default" Tasks:
```
1. Generate summary of the task
2. Report summary to user
3. Do not update status
4. Skip content processing
5. Mark as processed
```

## Content Processing Phase

### 7. Extract Content Components
```
From Task Description:
1. Title: Either from description (Sajtóközlemény) or summary (News)
2. Teaser: Extract 2nd paragraph, usually bold formatted text
3. Body: Extract from 3rd paragraph onwards
4. Created Date: Use task creation timestamp
```

### 8. Format Content
```
Body Formatting Rules:
1. Split text at '\r\n' boundaries
2. Create <p> tags for each paragraph
3. Ensure no line exceeds 120 characters
4. Preserve HTML formatting where appropriate
5. Escape special YAML characters
```

### 9. Check for Duplicates
```
1. Read current news.yaml file
2. Check if task key already exists
3. If exists: Skip processing, log duplicate
4. If not exists: Proceed with insertion
```

## YAML Integration Phase

### 10. Prepare YAML Record
```yaml
<task_key>:
  title: <extracted_title>
  tags: [<content_tag>][<current_year>]
  teaser: <extracted_teaser>
  body: <formatted_body>
  media: []
  created_at: <task_created_date>
  updated_at: <task_created_date>
```

### 11. Insert into news.yaml
```
1. Read current news.yaml content
2. Locate entity definition section
3. Insert new record at the front (after entity definition)
4. Preserve all existing records
5. Maintain proper YAML formatting
6. Validate YAML syntax before saving
```

## Completion Phase

### 12. Update Memory
```
1. Create or update jira_task_check entity
2. Set last_check_date to current timestamp
3. Include processing summary (tasks processed, skipped, errors)
```

### 13. Report Results
```
Generate summary report including:
- Number of tasks processed
- Number of tasks skipped (duplicates)
- Number of errors encountered
- List of updated files
- Final status of each processed task
```

## Error Handling

### Common Error Scenarios:
1. **Jira Connection Failure:** Report MCP server issue, suggest reconnection
2. **Status Update Failure:** Log error, continue with content processing
3. **YAML Parse Error:** Backup original file, report syntax issue
4. **Memory Update Failure:** Log warning, processing can continue
5. **File Access Error:** Check permissions, report file system issue

### Recovery Procedures:
- Always backup news.yaml before modifications
- Log all intermediate states for debugging
- Provide clear error messages with suggested actions
- Ensure partial progress is preserved on failure