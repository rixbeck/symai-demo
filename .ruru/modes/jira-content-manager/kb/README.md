+++
id = "JIRA-CM-KB-README-V1"
title = "Jira Content Manager Knowledge Base"
context_type = "documentation"
scope = "Overview and navigation guide for Jira Content Manager KB"
target_audience = ["jira-content-manager", "roo-commander"]
granularity = "overview"
status = "active"
last_updated = "2025-06-03"
tags = ["kb", "documentation", "jira", "content-management", "navigation"]
related_context = [
    ".ruru/modes/jira-content-manager/jira-content-manager.mode.md"
]
template_schema_doc = ".ruru/templates/toml-md/09_documentation.README.md"
+++

# Jira Content Manager Knowledge Base

## Overview

This Knowledge Base contains detailed procedures, specifications, and reference materials for the Jira Content Manager mode. The mode specializes in automated processing of content tasks from Jira, including press releases and news articles.

## Knowledge Base Structure

### Core Workflow Documentation

**[01-task-processing-workflow.md](01-task-processing-workflow.md)**
- Complete end-to-end workflow for processing Jira content tasks
- Initialization, discovery, classification, and completion phases
- Error handling and recovery procedures
- Memory management and reporting requirements

**[02-news-yaml-format.md](02-news-yaml-format.md)**
- Detailed specification for news.yaml fixture format
- hautelook/alice-bundle compliance requirements
- Content extraction and formatting rules
- Line length management and YAML syntax
- Duplicate prevention and validation procedures

**[03-jira-status-mapping.md](03-jira-status-mapping.md)**
- Jira status IDs and workflow transitions
- MCP tool implementation details
- Error handling for status updates
- Monitoring and troubleshooting guidelines

## Quick Reference

### Task Types and Processing
```
Sajtóközlemény:  Extract title from description, tag as 'sajtokozlemeny'
News:           Use summary as title, tag as 'news'  
Default:        Summarize only, no content processing
```

### Status Workflow
```
Backlog [10100] → Nyitott [1] → Folyamatban [3] → Development Done [10101]
```

### Key File Paths
```
Target:     ../fixtures/news.yaml
KB:         .ruru/modes/jira-content-manager/kb/
Mode:       .ruru/modes/jira-content-manager/jira-content-manager.mode.md
```

### MCP Dependencies
```
Required:   jira-mcp (task queries, status updates)
Required:   memory (check date persistence)  
Optional:   filesystem (for additional file operations)
```

## Usage Patterns

### Primary Invocation
The mode is typically invoked when:
- User requests "check Jira content tasks"
- Scheduled content processing is needed
- Manual content task processing is required

### Integration Points
- Memory MCP for persistent state tracking
- Jira MCP for task management and status updates
- Local file system for news.yaml fixture updates

### Error Recovery
Each KB document includes specific error handling procedures:
- Backup strategies for file modifications
- Rollback procedures for failed operations
- Diagnostic tools for troubleshooting

## Development Notes

### Extension Points
The mode can be extended to support:
- Additional content types beyond press releases and news
- Multiple fixture file targets
- Custom status workflows per project
- Enhanced content formatting options

### Configuration Options
Mode behavior can be customized through:
- File path configuration for fixture targets
- Status ID mappings for different Jira instances
- Content formatting rules and templates
- Processing frequency and scheduling

## Related Documentation

### Mode Definition
- [jira-content-manager.mode.md](../jira-content-manager.mode.md) - Primary mode specification

### Integration Guides
- Jira MCP Server configuration and setup
- Memory MCP Server for state persistence
- News fixture format documentation

### Troubleshooting
- Common error scenarios and solutions in each KB document
- MCP server connectivity and configuration issues
- YAML syntax and formatting problems
- Jira workflow and permission problems