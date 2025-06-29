+++
id = "JIRA-CM-KB-STATUS-MAPPING-V1"
title = "Jira Content Manager: Status Mapping and Workflow"
context_type = "knowledge"
scope = "Jira status transitions and workflow management for content tasks"
target_audience = ["jira-content-manager"]
granularity = "detailed"
status = "active"
last_updated = "2025-06-03"
tags = ["jira", "status", "workflow", "transitions", "mapping"]
related_context = [
    ".ruru/modes/jira-content-manager/kb/01-task-processing-workflow.md",
    ".ruru/modes/jira-content-manager/kb/02-news-yaml-format.md"
]
template_schema_doc = ".ruru/templates/toml-md/08_ai_context_source.README.md"
+++

# Jira Status Mapping and Workflow

## Overview

This document defines the exact Jira status IDs and workflow transitions used by the Jira Content Manager for processing content tasks.

## Status ID Mapping

### Core Status Values
```
Status Name             | Status ID    | Description
------------------------|--------------|----------------------------------
Backlog                 | "10100"      | Initial state for new tasks
Nyitott (Open)          | "1"          | Task opened for processing  
Folyamatban (In Progress)| "3"          | Task actively being processed
Development Done        | "10101"      | Task processing completed
```

### Status Identification
```
When querying tasks:
- Use string values for status IDs in API calls
- Match exact status names for filtering
- Verify status transitions are available before attempting
```

## Workflow Transitions

### Sajtóközlemény (Press Release) Workflow
```
Step 1: Backlog [10100] → Nyitott [1]
  - API Call: updateTaskStatus(taskId, "1")
  - Verify: Check response for successful transition
  - Log: Record status change with timestamp

Step 2: Nyitott [1] → Folyamatban [3]  
  - API Call: updateTaskStatus(taskId, "3")
  - Verify: Check response for successful transition
  - Log: Record status change with timestamp

Step 3: [Process Content - See workflow KB]

Step 4: Folyamatban [3] → Development Done [10101]
  - API Call: updateTaskStatus(taskId, "10101")
  - Verify: Check response for successful transition
  - Log: Record final status with completion timestamp
```

### News Article Workflow
```
Step 1: Backlog [10100] → Nyitott [1]
  - API Call: updateTaskStatus(taskId, "1")
  - Verify: Check response for successful transition
  - Log: Record status change with timestamp

Step 2: Nyitott [1] → Folyamatban [3]
  - API Call: updateTaskStatus(taskId, "3") 
  - Verify: Check response for successful transition
  - Log: Record status change with timestamp

Step 3: [Process Content - See workflow KB]

Step 4: Folyamatban [3] → Development Done [10101]
  - API Call: updateTaskStatus(taskId, "10101")
  - Verify: Check response for successful transition
  - Log: Record final status with completion timestamp
```

### Default Task Workflow
```
No status changes required:
- Tasks remain in Backlog [10100] status
- Only generate summary and report to user
- Log processing as "summarized, no status change"
```

## MCP Tool Implementation

### Status Update Tool Usage
```
Tool: updateTaskStatus
Server: jira-mcp

Parameters:
- taskId: String (Jira task key, e.g., "PROJECT-123")  
- statusId: String (target status ID from mapping above)

Example Call:
use_mcp_tool(
  server_name: "jira-mcp",
  tool_name: "updateTaskStatus", 
  arguments: {
    "taskId": "PROJECT-123",
    "statusId": "1"
  }
)
```

### Status Verification
```
Tool: getTask
Server: jira-mcp

Parameters:
- taskId: String (Jira task key)

Use for:
- Verifying current status before transitions
- Confirming successful status updates
- Debugging workflow issues
```

### Available Status Check
```
Tool: getAvailableStatuses  
Server: jira-mcp

Parameters:
- taskId: String (Jira task key)

Use for:
- Checking available transitions for a task
- Validating workflow permissions
- Troubleshooting blocked transitions
```

## Error Handling

### Transition Failures
```
Common Failure Scenarios:
1. Status transition not allowed
2. Insufficient permissions
3. Task not found
4. Network/API errors

Recovery Actions:
- Log specific error details
- Check available statuses for task
- Verify task permissions
- Continue processing if possible
- Report status update failures separately
```

### Status Validation
```
Before Each Transition:
1. Verify current task status matches expected
2. Check if target status is available
3. Confirm user has permission for transition
4. Log any validation warnings

Validation Example:
current_status = getTask(taskId).status
if current_status != expected_status:
    log_warning(f"Unexpected status: {current_status}, expected: {expected_status}")
    # Decide whether to proceed or abort
```

## Workflow State Management

### Processing State Tracking
```
Track for each task:
- Initial status when processing started
- Each status transition with timestamp  
- Final status achieved
- Any failed transition attempts
- Content processing completion state
```

### Rollback Considerations
```
Status rollback is NOT implemented:
- Jira status changes are considered permanent
- Content processing failures do not trigger status rollback
- Manual intervention required for status corrections
- Log all state changes for audit trail
```

## Integration Points

### With Task Discovery
```
Task Query JQL must include:
status = "Backlog"

This ensures only tasks in initial state are processed
```

### With Content Processing
```
Status updates occur at specific workflow points:
1. Before content extraction (Open → In Progress)
2. After successful content publishing (In Progress → Done)
3. Never during content processing errors
```

### With Memory Management
```
Status information stored in processing logs:
- Task key and final status in memory
- Transition timestamps for audit
- Error details for troubleshooting
```

## Monitoring and Logging

### Status Change Logging
```
For each status transition, log:
- Task key
- Source status ID and name
- Target status ID and name  
- Timestamp of change
- API response details
- Success/failure status
```

### Workflow Monitoring
```
Track metrics:
- Tasks processed per run
- Successful status transitions
- Failed status transitions
- Tasks stuck in intermediate states
- Average processing time per task type
```

## Configuration Management

### Environment-Specific Mappings
```
Status IDs may vary between Jira instances:
- Development: Use configured dev status IDs
- Production: Use configured prod status IDs
- Staging: Use configured staging status IDs

Configuration location: Mode config section
```

### Workflow Customization
```
For different projects, status mappings may need:
- Different status ID values
- Additional intermediate states
- Modified transition sequences
- Custom validation rules

These should be configurable in mode metadata
```

## Troubleshooting Guide

### Common Issues
```
1. "Transition not allowed"
   - Check getAvailableStatuses for task
   - Verify user permissions
   - Confirm workflow configuration

2. "Status ID not found"  
   - Verify status ID mapping is correct
   - Check Jira instance configuration
   - Confirm status exists in project

3. "Task not found"
   - Verify task key format
   - Check task exists and is accessible
   - Confirm user has read permissions
```

### Diagnostic Tools
```
1. getTask(taskId) - Check current task state
2. getAvailableStatuses(taskId) - See allowed transitions  
3. getProjects() - Verify project access
4. Jira audit log - Review status change history