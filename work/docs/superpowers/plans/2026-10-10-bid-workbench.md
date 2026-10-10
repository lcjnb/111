# 招投标智能技能（Bid Workbench）实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 交付一套可复用的招投标智能技能（4 个专业角色 + 总控 + 共享工作台 + 确定性校验脚本），并用本次真实资料包跑出验证结果。

**Architecture:** 技能以 Markdown 指令（SKILL.md）形式定义角色边界与硬约束，共享项目状态通过 `projects/<项目编号>/` 下的编号分段文件承载，Python 校验脚本对标记完整性与符号计数做确定性检查。

**Tech Stack:** Markdown（SKILL.md 指令）、Python 3（工作台校验与资料抽取）、PowerShell（演示执行）

## Global Constraints

- 投标主体固定为四川省科智汇川人工智能科技有限责任公司
- 禁止编造业绩、人员、资质、参数、案例、承诺
- 所有生成内容必须带标记：`[已确认]` / `[合理拟定]` / `[待补充]` / `[待确认]` / `[禁止直接使用]`
- 无标记内容视为不合格，审查员必须退回
- 每条要求必须携带：原文引用、章节号、页码、符号标识、风险等级
- 废标项与评分项必须分表输出，禁止混表
- 符号计数校验：采购需求 ▲=12、●=10、█=3，不一致必须报告差异
- 不生成签章，不判定电子签章效力，不代替平台提交
- 当前工作目录不是 Git 仓库，所有提交步骤以文件落地代替 git commit

---

### Task 1: 共享层（标记制度 + 工作台模板 + 校验脚本）

**Files:**
- Create: `skills/shared/workbench-schema.md`
- Create: `skills/shared/tags.md`
- Create: `skills/shared/templates/*.md`
- Create: `skills/scripts/validate_workbench.py`
- Test: `skills/scripts/test_validate_workbench.py`

**Interfaces:**
- Consumes: `projects/<code>/` 目录
- Produces: `validate_workbench.py` 提供 `validate(project_dir: Path) -> dict`，返回 `{"errors": [], "warnings": [], "stats": {}}`

- [ ] **Step 1: 写失败测试** `test_validate_workbench.py` 覆盖：缺标记报错、符号计数不符报错、废标与评分混表报错
- [ ] **Step 2: 运行测试确认失败** `python skills/scripts/test_validate_workbench.py` → 期望 FAIL（模块不存在）
- [ ] **Step 3: 实现校验脚本** 检查内容标记完整性、编号文件齐全性、符号计数一致性
- [ ] **Step 4: 运行测试确认通过** → 期望 PASS
- [ ] **Step 5: 落地共享模板与标记制度文档**

### Task 2: tender-analyst 投标助理

**Files:**
- Create: `skills/tender-analyst/SKILL.md`
- Create: `skills/tender-analyst/references/extraction-rules.md`

**Interfaces:**
- Consumes: 招标 PDF/DOCX、附件
- Produces: `01_要求矩阵.md`、`02_废标项清单.md`、`03_评分点清单.md`、`04_任务清单.md`

- [ ] **Step 1: 编写 SKILL.md** 定义职责、输入、输出、硬约束、工作步骤
- [ ] **Step 2: 编写抽取规则参考** 定义符号语义、风险分级、废标判定条件、条目字段格式

### Task 3: doc-secretary 文档秘书

**Files:**
- Create: `skills/doc-secretary/SKILL.md`
- Create: `skills/doc-secretary/references/format-spec.md`

**Interfaces:**
- Consumes: `01_要求矩阵.md`、企业资料目录
- Produces: `10_证据索引.md`、`11_资料缺口清单.md`、`12_版本记录.md`、`20_格式规范.md`

- [ ] **Step 1: 编写 SKILL.md** 定义证据登记字段与缺口登记规则
- [ ] **Step 2: 编写格式规范参考** 标题层级、编号、页眉页脚、表格、命名规则

### Task 4: presales-writer 售前助手

**Files:**
- Create: `skills/presales-writer/SKILL.md`
- Create: `skills/presales-writer/references/outline-rules.md`

**Interfaces:**
- Consumes: `01_要求矩阵.md`、`03_评分点清单.md`、`10_证据索引.md`
- Produces: `30_投标文件提纲.md`、`31_方案初稿/*.md`、`32_服务应答表初稿.md`

- [ ] **Step 1: 编写 SKILL.md** 定义禁用表述与标记使用规则
- [ ] **Step 2: 编写提纲规则** 评分点必须映射到章节，缺口必须在文末列明

### Task 5: compliance-reviewer 文档审查员

**Files:**
- Create: `skills/compliance-reviewer/SKILL.md`

**Interfaces:**
- Consumes: 全部 0x/1x/3x 文件
- Produces: `40_问题清单.md`、`41_附件与签章检查表.md`、`42_最终提交检查表.md`

- [ ] **Step 1: 编写 SKILL.md** 定义三级问题分类、问题字段格式、只报不改原则

### Task 6: bid-orchestrator 总控

**Files:**
- Create: `skills/bid-orchestrator/SKILL.md`
- Create: `skills/bid-orchestrator/references/workflow.md`
- Create: `skills/company-profile/SKILL.md`
- Create: `skills/company-profile/科智汇川-资料待补充清单.md`
- Create: `skills/install.ps1`

**Interfaces:**
- Consumes: 用户指令 + 工作台状态
- Produces: 状态机流转与人工任务清单

- [ ] **Step 1: 编写总控 SKILL.md** 定义状态机与路由规则
- [ ] **Step 2: 编写流程参考** 定义 REMEDIATE 回流分类逻辑
- [ ] **Step 3: 建立企业档案** 登记已知信息与待补充资料清单
- [ ] **Step 4: 编写安装脚本** 将技能复制到 `~/.codex/skills/`

### Task 7: 真实资料包验证

**Files:**
- Create: `projects/N5100012026002044/*`（全部工作台文件）
- Create: `docs/验证报告.md`

**Interfaces:**
- Consumes: 资料包、企业档案
- Produces: 完整工作台 + 校验通过 + 验证报告

- [ ] **Step 1: 运行 tender-analyst** 产出四张分析清单
- [ ] **Step 2: 运行 doc-secretary** 产出证据索引与缺口清单
- [ ] **Step 3: 运行 presales-writer** 产出提纲与方案初稿
- [ ] **Step 4: 运行 compliance-reviewer** 产出问题清单
- [ ] **Step 5: 运行校验脚本** → 期望 errors 为空
- [ ] **Step 6: 编写验证报告** 记录运行效果与实测数据
