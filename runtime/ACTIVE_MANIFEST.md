# Runtime Manifest

Runtime Version: ZH-RUNTIME-DRAFT
Status: DRAFT
Published At:
Based On Commit:

## Partitions

### Compiler Authority

| path | sha256 |
|---|---|
| docs/知乎OS Compiler V1.md | |
| docs/内容架构总则.md | |
| docs/知乎OS权威归属表.md | |

### Protocol Docs

| path | sha256 |
|---|---|
| docs/08_总AI执行中心.md | |
| docs/知乎OS执行协议.md | |
| templates/知乎OS总控提示词.md | |
| docs/Codex选题采集协议.md | |
| templates/选题包模板.md | |

### Node Execution Assets

| path | sha256 |
|---|---|
| templates/Claude正文生产Prompt.md | |
| templates/GPT审核清单.md | |
| docs/知乎内容质量参数库_V2.md | |
| docs/生产状态机与交接规范.md | |
| data/Publish_Queue.md | |
| templates/Failure Pattern模板.md | |

### Parameter & Knowledge Snapshots

| path | sha256 |
|---|---|
| production_variable_library.md | |
| runtime/production_variable_snapshot.md | |
| runtime/知乎结构库快照.md | |
| runtime/知乎ACTIVE规律快照.md | |
| runtime/知乎内容质量参数快照.md | |
| runtime/知乎账号画像快照.md | |
| docs/知乎OS Structure Evolution V1.md | |

### Governance Infrastructure

| path | sha256 |
|---|---|
| scripts/validate_runtime_consistency.py | |
| scripts/release_runtime.py | |
| docs/00-设计原则.md | |

### Historical Asset Tools

| path | sha256 |
|---|---|
| skills/Skill000_历史资产检索器.md | |
| scripts/search_historical_assets.py | |

## Regression Tests

- （无；本次迁移未声明可独立执行的回归测试脚本，见说明）

## 变更说明（相对上一版 DRAFT）

- 移除 `Production Card Assets` partition（`templates/Production Card模板.md`、`skills/Skill006_知乎生产卡生成器.md`、`scripts/validate_production_card.py`）：三者均为 `LEGACY_RETIRED`，不再是执行资产，见 `docs/知乎OS权威归属表.md`。
- 新增 `Compiler Authority` partition：`docs/知乎OS Compiler V1.md` 首次被纳入 Partitions（此前 Status: DESIGN_FROZEN 但从未进入任何 Runtime Release，本次 DRAFT 重建后仍需经 `scripts/release_runtime.py --status TRIAL` 才具备执行权威）。
- 新增 `Node Execution Assets` partition：把 AUDIT（GPT审核清单）、WRITE（Claude正文生产Prompt）、RELEASE（生产状态机与交接规范、Publish_Queue）对应的现行执行文件正式纳入 Partitions——此前这些文件从未出现在任何 Manifest 中。
- `Parameter & Knowledge Snapshots` 新增 `docs/知乎OS Structure Evolution V1.md`（COMPILE 结构选择能力的 Research Layer 权威）。
- `Governance Infrastructure` 新增 `docs/00-设计原则.md`。
- 本次仅重建 Partitions 列表，未运行 `scripts/release_runtime.py`，sha256 / Based On Commit 保持留空；Status 仍为 DRAFT，不具备执行权威。发布 TRIAL 需要显式运行该脚本并声明 `--status TRIAL`，是独立的人工批准动作，本次不代为执行。
