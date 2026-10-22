# Codex repository instructions

For humanities thesis planning, literature search/review, text assessment, translation, or citation tasks, use the `humanities-thesis` Skill registered in `.agents/skills/humanities-thesis`. Read its SKILL.md and load relevant references as needed. For general repository maintenance, do not apply the thesis interview workflow.

Run Python tools from the repository root with `.venv/bin/python` when available. Install dependencies with `python3 -m venv .venv` and `.venv/bin/python -m pip install -r requirements.txt`. Run regression checks with `.venv/bin/python -m unittest discover -s tests -v`.

Each cloud task is already isolated; use this checkout and do not create a worktree unless requested. Do not assume files uploaded in another task or background processes persist. Never fabricate literature or interpret an API failure as an empty successful search.
