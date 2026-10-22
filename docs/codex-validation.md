# Codex compatibility validation

Validated in the cloud environment on 2026-10-22.

## Skill discovery

The actual Codex app-server `skills/list` RPC was called with
`cwds: ["/workspace/humanities-thesis-skill"]` and `forceReload: true`.
It returned `humanities-thesis`, `enabled: true`, `scope: "repo"`, resolving to
`/workspace/humanities-thesis-skill/SKILL.md`, with no parsing errors.
The committed relative symlink `.agents/skills/humanities-thesis -> ../..`
registers the existing Skill without copying its instructions/resources.

## Skill invocation: blocked, not passed

Attempted a real independent model session:

```bash
codex exec --ephemeral --json -C /workspace/humanities-thesis-skill \
  '使用 $humanities-thesis 评估这句话的学术表达：有学者指出，文学必然改变社会。请实际运行评估工具，报告规则编号，不修改任何文件。'
```

Codex could initialize, but the model endpoint
`wss://chatgpt.com/backend-api/codex/responses` returned proxy CONNECT 403.
HTTPS fallback also failed. The retrying process was stopped. Therefore no
claim is made that a model loaded the Skill body or executed its tools in that
session. Model-service connectivity must be restored before rerunning this
check. Do not disable TLS verification. The native discovery check and Python
checks below are independent evidence; neither substitutes for this invocation.
The already-open hosted chat may use a separate Skill catalog and need a new task.

## Functional checks

- `python -m unittest discover -s tests -v`: 3 tests passed, covering merged
  duplicate metadata, ranking, citations, CLI text/Markdown/JSON rendering,
  and source-error reporting without live API dependencies.
- `python -m pip check`: passed.
- Live query `trauma narrative Chinese literature`, limit 2 per source:
  6 records returned across OpenAlex, CrossRef and CORE. Semantic Scholar
  returned HTTP 429; its live retrieval was not validated.
- Thesis-review CLI detected R1-01 for an intentionally vague citation.
- Generated PDF text was recovered by both PyMuPDF and pdfplumber;
  python-docx document save/read roundtrip passed.
- Query expansion and source-list CLI commands executed. Source-list checks
  configuration only. The sample Chinese query was returned unchanged;
  this is not evidence of translation quality.
- OCR, authenticated Chinese databases, browser integration and manuscript
  quality judgments are outside these checks.

## New tasks

Commit the registration and AGENTS.md, select this repository in the new task,
and start inside its checkout. Use `$humanities-thesis` for explicit invocation;
matching prose can trigger implicit selection. AGENTS.md reinforces use for
relevant thesis tasks. Unrelated repositories do not inherit this registration.
A published cloud snapshot is distinct from this Git commit; refresh/publish
cloud configuration when needed. See references/platform-guide.md for details.
