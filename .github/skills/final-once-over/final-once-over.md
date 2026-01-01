---
name: final-once-over
description: Guide for a final once-over code whenever changes are made or asked to review. Use this as a last step after making any changes or after reviewing code.
---

To perform a final once-ver failing GitHub Actions workflows in a pull request, follow this process, using tools provided from the GitHub MCP Server:

1. Review all changed files for typos or inconsistencies with Ruff configuration
2. Review all changed files for consistencies with unchanged files
3. Check `pyproject.toml` to see if any changes or improvements could be applied
4. Check all `.github/workflows/` files to see if any changes or improvements could be applied
5. Check `README.md` to see if any changes or improvements could be applied
6. Check `mkdocs.yaml` and all `docs/` files to see if any changes or improvements could be applied
7. Check all custom copilot instructions, agents, and skills files to see if any changes or improvements could be applied
8. Run ruff to find any linting/formatting issues and apply fixes if possible
