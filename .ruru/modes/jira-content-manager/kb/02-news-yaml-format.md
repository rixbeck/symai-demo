+++
id = "JIRA-CM-KB-YAML-FORMAT-V1"
title = "Jira Content Manager: News YAML Format Specification"
context_type = "knowledge"
scope = "Detailed format requirements for news.yaml fixture processing"
target_audience = ["jira-content-manager"]
granularity = "detailed"
status = "active"
last_updated = "2025-06-03"
tags = ["yaml", "format", "hautelook", "alice-bundle", "content-structure"]
related_context = [
    ".ruru/modes/jira-content-manager/kb/01-task-processing-workflow.md",
    ".ruru/modes/jira-content-manager/kb/03-jira-status-mapping.md"
]
template_schema_doc = ".ruru/templates/toml-md/08_ai_context_source.README.md"
+++

# News YAML Format Specification

## Overview

This document defines the exact format requirements for processing content into the `news.yaml` fixture file, following the hautelook/alice-bundle format standards.

## File Structure

### Location
```
../fixtures/news.yaml
```

### Basic Structure
```yaml
# Entity definition (preserved)
App\Entity\News:
    # Existing records (preserved)
    existing_record_1:
        title: "Existing Title"
        tags: [news][2024]
        teaser: "Existing teaser text"
        body: "Existing body content"
        media: []
        created_at: "2024-01-01 10:00:00"
        updated_at: "2024-01-01 10:00:00"
    
    # NEW RECORDS INSERTED HERE (at front after entity definition)
    <new_task_key>:
        title: <new_title>
        tags: [<tag>][<year>]
        teaser: <new_teaser>
        body: <new_body>
        media: []
        created_at: <created_timestamp>
        updated_at: <created_timestamp>
```

## Record Format Specification

### Task Key Format
```
- Use the Jira task key exactly as provided (e.g., "PROJECT-123")
- Must be unique within the file
- Used for duplicate detection
```

### Title Field
```
For Sajtóközlemény:
  - Extract from description field
  - Look for patterns like "Title: ...", "Cím: ...", or first line
  - Clean HTML tags and formatting
  
For News:
  - Use the summary field from Jira task
  - Clean special characters if needed
```

### Tags Field
```
Format: [<content_type>][<year>]

Content Types:
  - "sajtokozlemeny" for press releases
  - "news" for news articles
  
Year:
  - Use current year (e.g., 2025)
  
Examples:
  - [sajtokozlemeny][2025]
  - [news][2025]
```

### Teaser Field
```
Extraction Rules:
  1. Look for 2nd paragraph in description
  2. Usually bold formatted text (**text**)
  3. Strip formatting markers
  4. Keep as plain text
  5. Maximum recommended length: 200 characters
  
Processing:
  - Remove **bold** markers
  - Remove *italic* markers  
  - Trim whitespace
  - Ensure single line format
```

### Body Field
```
HTML Formatting Requirements:
  1. Convert description paragraphs to <p> tags
  2. Split on '\r\n' boundaries for paragraph detection
  3. Each <p> block must not exceed 120 characters per line
  4. Preserve line breaks within YAML multi-line format
  
Example:
body: |
  <p>First paragraph content that wraps
  appropriately within 120 character limit
  for proper YAML formatting.</p>
  <p>Second paragraph with proper HTML
  structure and line length management.</p>
```

### Media Field
```
Always: []
(Empty array - media processing not implemented)
```

### Timestamp Fields
```
Format: "YYYY-MM-DD HH:MM:SS"
Source: Jira task creation timestamp
Both created_at and updated_at use same value
```

## Line Length Management

### YAML Body Field Rules
```
Critical Requirements:
1. No line in the body field may exceed 120 characters
2. Use YAML literal block scalar (|) for multi-line content
3. Indent content properly (typically 2 spaces from field name)
4. Break lines at word boundaries when possible
5. Preserve paragraph structure with <p> tags
```

### Implementation Strategy
```python
def format_body_for_yaml(content, max_line_length=120):
    paragraphs = content.split('\r\n')
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        if paragraph.strip():
            # Wrap in <p> tags
            p_content = f"<p>{paragraph.strip()}</p>"
            
            # Break long lines
            if len(p_content) > max_line_length:
                # Split at word boundaries
                words = p_content.split(' ')
                current_line = ""
                lines = []
                
                for word in words:
                    if len(current_line + word + 1) <= max_line_length:
                        current_line += (" " if current_line else "") + word
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word
                
                if current_line:
                    lines.append(current_line)
                    
                formatted_paragraphs.extend(lines)
            else:
                formatted_paragraphs.append(p_content)
    
    return '\n'.join(formatted_paragraphs)
```

## Duplicate Prevention

### Check Logic
```
Before inserting new record:
1. Parse existing news.yaml content
2. Check if task key exists in current records
3. If found: Skip processing, log as duplicate
4. If not found: Proceed with insertion
```

### Insertion Strategy
```
Insertion Point:
- Find the line containing "App\Entity\News:"
- Insert new record immediately after this line
- Preserve all existing records below
- Maintain proper indentation (4 spaces for record keys)
```

## YAML Syntax Compliance

### Hautelook Alice Bundle Requirements
```
1. Use 4-space indentation for record keys
2. Use 8-space indentation for field keys  
3. Maintain consistent spacing
4. Escape special YAML characters in content
5. Use proper quoting for string values
```

### Special Character Handling
```
Characters requiring escaping:
- Colons (:) in content
- Quotes (") in content  
- Backslashes (\) in content
- Line breaks (\n, \r\n)

Escaping Strategy:
- Use double quotes for string values containing special chars
- Escape internal quotes as \"
- Convert line breaks to proper YAML multi-line format
```

## Validation Requirements

### Pre-Insert Validation
```
1. Verify YAML syntax of new record
2. Check field completeness
3. Validate timestamp format
4. Confirm tag format compliance
5. Test line length compliance
```

### Post-Insert Validation  
```
1. Parse entire file to verify YAML validity
2. Confirm new record is properly positioned
3. Verify existing records unchanged
4. Test file can be loaded by alice-bundle
```

## Error Recovery

### Backup Strategy
```
Before any modification:
1. Create backup: news.yaml.backup.[timestamp]
2. Store in same directory as original
3. Include backup path in processing logs
```

### Rollback Procedures
```
On YAML syntax error:
1. Restore from backup
2. Log specific error details
3. Report failure to user with diagnostic info
4. Preserve task processing state for retry
```

## Example Complete Record

```yaml
PROJECT-123:
    title: "Company Announces Revolutionary New Product"
    tags: [news][2025]
    teaser: "Breakthrough technology promises to transform industry standards"
    body: |
        <p>Our company today announced the launch of its
        groundbreaking new product that will revolutionize
        the way businesses operate in the digital age.</p>
        <p>The innovative solution combines cutting-edge
        artificial intelligence with user-friendly design
        to deliver unprecedented value to customers.</p>
        <p>Available starting next quarter, this product
        represents years of research and development
        investment by our dedicated engineering team.</p>
    media: []
    created_at: "2025-06-03 17:30:00"
    updated_at: "2025-06-03 17:30:00"