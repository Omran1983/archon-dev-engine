---
name: structured-output
description: Instructions for enforcing structured JSON schemas and machine-readable AI responses.
---

# ARCHON Structured Output Skill

This skill ensures your AI-native components communicate using reliable, parseable data structures rather than conversational text.

## When to Use
- Implementing API response handlers.
- Designing communication protocols between AI agents.
- Generating system-to-system tool parameters.

## Instructions
1. **Define Schema**: Always provide output as a valid JSON object.
2. **Remove Fluff**: Strip all conversational prefixes and suffixes (no "Certainly!", "I hope this helps").
3. **Status Enums**: Use standardized uppercase status codes: `SUCCESS`, `PARTIAL_SUCCESS`, `FAILURE`.
4. **Machine-First**: Prioritize parseability and schema adherence over human readability.

### Standard Response Format
```json
{
  "status": "SUCCESS",
  "data": { ... },
  "trace_id": "uuid-v4",
  "execution": { "duration_ms": 120 }
}
```
