# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root: this repo's single glossary of domain terms.
- **`docs/adr/`**: read ADRs that touch the area you're about to work in.

If either doesn't exist, **proceed silently**. Don't flag its absence; don't suggest creating them upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/improve-codebase-architecture`) creates them lazily when terms or decisions actually get resolved.

## File structure

This repo is **single-context**: one glossary at the repo root, one ADR directory.

```
/
├── CONTEXT.md                  ← the one glossary
├── docs/
│   ├── adr/                    ← architecture decisions
│   │   ├── 0001-....md
│   │   └── 0002-....md
│   └── agents/                 ← this skill suite's own config
└── (source code)
```

There is no `CONTEXT-MAP.md` at the root and no per-subproject `CONTEXT.md`, because this repo has a single context — a root map would have nothing to point at. Nothing is scaffolded today: the root `CONTEXT.md` and `docs/adr/` are created lazily, only when the first term or decision is actually written down.

This repo names its glossary `CONTEXT.md`, not `GLOSSARY.md`: wherever a skill says "the glossary" or `GLOSSARY.md`, read and write `CONTEXT.md` at the repo root instead.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders), but worth reopening because…_
