# CLAUDE.md

## Project Overview

**DQ1-Sample** is an experimental project to build a Dragon Quest 1 (ドラクエ1) game implementation. The project is in its early bootstrapping phase — no source code, build system, or framework has been chosen yet.

- **Repository:** DQ1-Sample
- **Description:** ドラクエ1を試しに作ってみる (Let's try making Dragon Quest 1)
- **Status:** Initial/bootstrapping — only README.md exists

## Repository Structure

```
DQ1-Sample/
├── CLAUDE.md          # This file — AI assistant guide
└── README.md          # Project description (Japanese)
```

The repository is a greenfield project. No directories, source files, configuration files, or build tooling have been added yet.

## Development Environment

- **Version control:** Git
- **Primary branch:** `master`
- **Remote:** `origin`
- **Language/Framework:** Not yet determined

### No build system, package manager, or CI/CD pipeline is currently configured.

## Conventions

### Language

- Project documentation (README.md) is written in Japanese.
- Code comments and commit messages may be in Japanese or English — follow existing patterns as they are established.

### Git

- Commit messages should be concise and descriptive.
- Feature work should be done on dedicated branches.

## For AI Assistants

### Before making changes

1. Read `README.md` for the latest project description.
2. Check `git log` and `git status` for recent changes and current state.
3. If a build system or framework has been added since this file was last updated, read the relevant config files (e.g., `package.json`, `Cargo.toml`, `setup.py`, `Makefile`) before modifying code.

### Key guidance

- This is an early-stage project. When setting up new tooling or structure, keep things simple and avoid over-engineering.
- Dragon Quest 1 is a classic JRPG — any implementation work should focus on core RPG mechanics: maps, encounters, turn-based combat, dialogue, and progression.
- Respect the author's technology choices once established. Do not switch frameworks or languages without explicit instruction.
- When the project grows, update this file to reflect the current structure, build commands, test commands, and coding conventions.

### Updating this file

As the project evolves, this CLAUDE.md should be updated to include:

- Build and run commands
- Test commands and testing patterns
- Directory structure and module organization
- Dependency management instructions
- Code style and linting configuration
- Architecture decisions and patterns
