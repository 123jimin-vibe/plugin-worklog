# Software Architecture Principles

General to software engineering, not AI-specific.

- Small and large projects **require different methodologies**.
- Development stages: Requirements → Architecture → Detail Design → Implementation → QA.
- Iterative lifecycle (Agile) usually superior. Fixed requirements are ideal but rare — true requirements are often discovered through implementation.
- Bug fix cost lowest when caught earliest.

**Requirements** — explicit, capturing *intent* (*what/why*, not *how*). Avoid programming-specific framing unless the domain is programming itself.

**Architecture** — localize impact of changing requirements:
- Record reasons behind decisions.
- Minimize components touched per requirement change.
- Building blocks: clear responsibilities, minimal dependencies, explicitly declared allowed/forbidden inter-block dependencies.
- Specify business constraints, robustness level, anticipated changes, and dangers.
- Be simple. Exclude unnecessary features.

**Detail design** — derive from architecture:
- Prefer "simple and obvious" over "clever".
- Loose coupling. High fan-in, low fan-out.
