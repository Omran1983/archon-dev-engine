# ARCHON Dev Engine

> ARCHON Dev Engine enforces engineering discipline in AI-native systems — before production breaks it.

**ARCHON Dev Engine** is a Cursor Plugin that enforces high-performance engineering standards. Designed for AI-first startups, it ensures your agents build systems that are async-first, deterministic, and production-ready.

## The A.R.C.H.O.N. Doctrine

- **A**sync Sovereignty: Resilient, non-blocking architecture.
- **R**eproducible Intelligence: Structured, versioned AI outputs.
- **C**ompliance Embedded: Risk-aware systems by design.
- **H**ardened Execution: Observable, failure-transparent workflows.
- **O**perational Discipline: Deterministic structure and config layering.
- **N**ative Enforcement: Strict rule-based adherence.

## Features

- **Portability**: v0.1.0 is dependency-free and works across any local environment.
- **Sovereign Rules**: Persistent guidance for async-first and structured system design.
- **ARCHON Architect**: A specialized system designer agent.
- **Structured Output Skill**: Enforces machine-readable system communication.

## ARCHON Guard (Fail-Closed Enforcement)

To enforce the doctrine at the commit level, install the ARCHON Guard:

```bash
python scripts/install-guard.py
```

This installs a git `pre-commit` hook that vetoes any code violating the Async-First doctrine.

## Installation

1. Open Cursor Settings.
2. Navigate to **Plugins** -> **Development**.
3. Select **Load Plugin from Folder**.
4. Choose the `archon-dev-engine` directory.

## About
Built by **A-ONE GLOBAL RESOURCING LTD** to standardize the future of AI-native engineering.

## License
MIT
