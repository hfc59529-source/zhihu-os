# Runtime Manifest

Runtime Version: ZH-RUNTIME-DRAFT
Status: TRIAL
Published At: 2026-08-11 13:58:20 UTC
Based On Commit: fe8276f

## Partitions

### Compiler Authority

| path | sha256 |
|---|---|
| docs/知乎OS Compiler V1.md | 310ef2fbcb9b6cddc72d14a87335ccb5c4832230d7febc8c1528eb123052b646 |
| docs/内容架构总则.md | cdf1c858368dec970170f646f6d9fc98aa0d411348e1b63c0f2927e785e70714 |
| docs/知乎OS权威归属表.md | 2bd83233918b3b438d8465b3c24aa52b925ec7aa3ae4946d1dd9a29ff9b771dd |

### Protocol Docs

| path | sha256 |
|---|---|
| docs/08_总AI执行中心.md | a47d710be44361af3727363298f0b9a39d07d160bea1f65c8f7504fab8b27887 |
| docs/知乎OS执行协议.md | 43db9f6b8653769514dec0018c9e3462c5d7a019fd203bb5f174dd4cafe776c9 |
| templates/知乎OS总控提示词.md | 5a74d866473d5a5edb53c39c35ea953f2f22c74a9caaba6332b9e14f0f0679b4 |
| docs/Codex选题采集协议.md | d878a821107b1dc73f071e4d88f87ff802ceafb5683126ccff890a156bafe8f1 |
| templates/选题包模板.md | 41d97f3a9b1ce71d1df1dd105debaadcd36932dc1019ccbdbfea6b44b3309717 |

### Node Execution Assets

| path | sha256 |
|---|---|
| templates/Claude正文生产Prompt.md | 56677d26616dd7b045a71e49d11578456846722686bc446411e86b23f5c858e5 |
| templates/GPT审核清单.md | 631082a9cb7f41424b7e95801ee33e360db0c2db34d17d89f11b099812adb792 |
| docs/知乎内容质量参数库_V2.md | 1dd44575e99ea381a5a4bff10c25c27dbea64d6b0be96c193081b275e48fcea0 |
| docs/生产状态机与交接规范.md | edec195ba4d13b8b0cf0aff3ad9ed49bfe8def2a3339b78121ab8cdb521cb92c |
| data/Publish_Queue.md | 0e166254884230f0390e7480424efb978b4499498b527afdea66855e22839828 |
| templates/Failure Pattern模板.md | 3ea79dae80db29d8a6883fb2fe375bdcf42996d6fc2a8e9e059f00d37f52345e |

### Parameter & Knowledge Snapshots

| path | sha256 |
|---|---|
| production_variable_library.md | a3ae0358b4ec343abbfa3a4da95a62100e56472bf410360583fd9e7281c26944 |
| runtime/production_variable_snapshot.md | ee39d808cfdb09e86743a11164f0559d312e4e1ec0554b198f2e24e1522731c1 |
| runtime/知乎结构库快照.md | af28fa7c8530b56dd973f68ce4b5e05c84c3f0b534984bc055f8529a964affbe |
| runtime/知乎ACTIVE规律快照.md | 7d4239ffa5e3447c27f34d0de9abe3d3ccc33331707614cef0685e980ebbe045 |
| runtime/知乎内容质量参数快照.md | a5df4370eaee5fc84b45cff5b065e3d7118f4c08cec3b8c00f15c993b5ac815a |
| runtime/知乎账号画像快照.md | be4bffffb6eb7916e11181b2006ce749434e1712767b547c2671dbcde72cf955 |
| docs/知乎OS Structure Evolution V1.md | a16d5b025ba8e89dc387561ee91d222b57c5a6a5f66b3c36c08b17575f9c9dae |

### Governance Infrastructure

| path | sha256 |
|---|---|
| scripts/validate_runtime_consistency.py | 016d77cccd1d3f051d353981f32fd8770afef149a448a29da954351befa00efb |
| scripts/release_runtime.py | 1f45ee39f777abd5ced06418e5215ac51499cdefa113590870745ca3933d607a |
| docs/00-设计原则.md | 2a11524167fb4f1b24e7e2d8cf478adce3465ab3a27158f85ebe81b591f14e67 |

### Historical Asset Tools

| path | sha256 |
|---|---|
| skills/Skill000_历史资产检索器.md | 5c04e5aba74d92d6d4b518a20d48dbfff16bcbd847b32ffcbdc4c7ed3e8c0cda |
| scripts/search_historical_assets.py | 4051e8e1630ddb984b45db90073ea5497fef2cef0794e4bd72c2fb59e163e091 |

## Regression Tests

- （无；本次发布未声明可独立执行的回归测试脚本）
