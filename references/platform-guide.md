# Agent 适配说明

本 skill 适配 **Codex**、**Claude Code** 和 **OpenClaw**。

---

## Codex 适配与持续调用

仓库根目录的 `SKILL.md` 本身不保证 Codex 自动发现。本仓库提交了 `.agents/skills/humanities-thesis -> ../..`，让 Codex 从标准仓库 Skill 目录发现同一份主文件及其资源，无需复制内容。

在选择本仓库、工作目录位于仓库内的新 Codex 任务中：

1. 显式调用：`$humanities-thesis 请检查这份论文草稿`。
2. 隐式调用：描述论文选题、文献检索等需求，由 Skill description 匹配；`AGENTS.md` 也明确要求相关任务使用此 Skill。自动发现不代表每个无关任务都强制执行。
3. 安装依赖后，按 SKILL.md 的目录约定调用工具。只需指导时不要求 Python；检索和文档处理需要 Python 依赖及网络。

新会话会重新发现仓库内已提交的 Skill。已有会话可能需要重新打开任务；云端聊天的可用 Skill 列表由宿主提供，CLI 验证不能证明已打开聊天会动态刷新。其他仓库不会继承本仓库的注册。需要跨仓库使用时，把完整 Skill 安装到该 Codex 实例支持的用户 Skill 目录（如 `~/.agents/skills/humanities-thesis`），或在目标仓库注册完整 Skill；不要依赖指向临时任务工作区的绝对链接。

真实发现验证可使用 Codex app-server 的 `skills/list`，检查名称 `humanities-thesis`、`enabled: true`、`scope: repo` 及无解析错误。真实调用验证：

```bash
codex exec -C /path/to/humanities-thesis-skill \
  '使用 $humanities-thesis 评估：有学者指出，文学必然改变社会。请实际运行评估工具并报告规则编号。'
```

检查执行轨迹中确实加载 SKILL.md 并运行 review.py，而不仅是模型自称使用了 Skill。此验证需要 Codex 自身可用的认证和模型服务；Python 测试不能替代它。

## 文件结构总览

```
humanities-thesis/
├── SKILL.md                          ← 核心指令（agent 启动时加载）
├── README.md                         ← 项目说明
├── references/                       ← 参考文档（按需加载）
│   ├── writing-templates.md          ← 写作模板
│   ├── theory-frameworks.md          ← 理论家速查（16位）
│   ├── terminology-bilingual.md      ← 术语对照表（224条）
│   ├── formatting-guide.md           ← 格式规范
│   ├── literature-review.md          ← 文献综述与搜索策略
│   ├── literature-analysis.md        ← 核心文献拆解流程
│   ├── material-integration.md       ← 材料整合工作流
│   ├── english-translation.md        ← 英文翻译与投稿
│   └── platform-guide.md             ← 本文件
└── scripts/                          ← 文献搜索脚本
    ├── search.py                     ← 统一搜索入口
    ├── .env.example                  ← 配置模板
    ├── lib/                          ← 公共模块
    │   ├── schema.py                 ← 数据模型
    │   ├── http_client.py            ← HTTP 封装
    │   ├── utils.py                  ← 工具函数
    │   ├── query.py                  ← 查询预处理
    │   ├── score.py                  ← 评分排序
    │   ├── dedupe.py                 ← 去重
    │   ├── render.py                 ← 输出渲染
    │   └── citation.py               ← 引文生成
    └── sources/                      ← 数据源模块（8个）
        ├── source_cnki.py            ← 知网
        ├── source_ncpssd.py          ← 国家哲社文献中心
        ├── source_wanfang.py         ← 万方
        ├── source_openalex.py        ← OpenAlex
        ├── source_core.py            ← CORE
        ├── source_google_scholar.py  ← Google Scholar
        ├── source_semantic_scholar.py ← Semantic Scholar
        └── source_crossref.py        ← CrossRef
```

---

## Claude Code 适配

### 安装与启动

```bash
# 在项目目录下，Claude Code 会自动读取 SKILL.md
# 也可以手动指定
claude --skill ./SKILL.md
```

### 能力对照

| 本 skill 需要的能力 | Claude Code 支持情况 | 调用方式 |
|-------------------|-------------------|---------|
| 读取 SKILL.md | ✓ 自动读取 | 放在项目根目录即可 |
| 按需加载 references/ | ✓ 文件读取 | `cat references/xxx.md` |
| 执行搜索脚本 | ✓ bash 执行 | `python scripts/search.py "关键词"` |
| 读取用户上传的 PDF | ✓ Python 环境 | 用 PyMuPDF/pdfplumber 提取文本 |
| 读取用户上传的 DOCX | ✓ Python 环境 | 用 python-docx 读取 |
| 联网搜索 | ✓ 内置 | 直接使用联网能力搜索术语/文献 |
| 生成 DOCX/PDF 输出 | ✓ Python 环境 | 用 python-docx / reportlab 生成 |

### 安装依赖

```bash
pip install PyMuPDF pdfplumber python-docx beautifulsoup4 requests
```

### 文件读取流程

用户上传文件后，Claude Code 可以直接访问文件：

```python
# PDF 文本提取
import fitz  # PyMuPDF
doc = fitz.open("/path/to/file.pdf")
for page in doc:
    text = page.get_text()

# DOCX 文本提取
from docx import Document
doc = Document("/path/to/file.docx")
for para in doc.paragraphs:
    text = para.text
```

---

## OpenClaw 适配

### 安装与启动

将整个项目目录作为 skill 导入 OpenClaw。SKILL.md 会被自动识别为主指令文件。

### 能力对照

| 本 skill 需要的能力 | OpenClaw 支持情况 | 调用方式 |
|-------------------|-----------------|---------|
| 读取 SKILL.md | ✓ 自动读取 | skill 主文件 |
| 按需加载 references/ | ✓ 文件读取 | 读取 skill 目录下的文件 |
| 执行搜索脚本 | ✓ 代码执行 | 在代码执行环境中运行 Python |
| 读取用户上传的文件 | 视配置 | 检查 agent 提供的文件处理工具 |
| 联网搜索 | ✓ 内置 | 使用 agent 的搜索能力 |

### 注意事项

- OpenClaw 的文件处理能力取决于具体配置，如果不支持直接读取 PDF，引导用户粘贴文献内容
- 脚本执行环境可能需要预装依赖，在 skill 配置中声明 `requirements.txt`

---

## 关于 Rules 的执行

SKILL.md 中的 Rules（R1-R4）是硬性规则，两个 agent 环境都必须遵守。其核心目的是防止模型幻觉在学术场景中造成严重后果（编造文献、虚构引文）。

具体来说：
- **Claude Code**：Claude 模型本身的幻觉率较低，但在生成文献信息时仍然可能出错。Rules 的作用是在 skill 层面再加一道检查
- **OpenClaw**：如果底层使用的模型幻觉率较高（如某些开源模型），Rules 的约束尤为重要。建议在 agent 配置中将 temperature 设为较低值（0.3-0.5），并开启自我检查

无论哪个 agent，生成的论文内容中如果涉及具体文献信息，都应提醒用户核实。
