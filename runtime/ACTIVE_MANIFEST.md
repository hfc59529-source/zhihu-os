# Runtime Manifest

Runtime Version: ZH-RUNTIME-DRAFT
Status: TRIAL
Published At: 2026-08-25 07:59:56 UTC
Based On Commit: 75535fa7b21de9d7f67c20a6330d8c6f5fef397e

## Partitions

### Compiler Authority

| path | sha256 |
|---|---|
| docs/知乎OS Compiler V1.md | cf3a7a48207496350a1338d231b9eda13cb9af094fda418d032441dc445606a8 |
| docs/内容架构总则.md | cdf1c858368dec970170f646f6d9fc98aa0d411348e1b63c0f2927e785e70714 |
| docs/知乎OS权威归属表.md | 013d3472a960977d9942f6853e89ea36e4a2ed30cd1c046bfdf0ddf371fa7664 |

### Protocol Docs

| path | sha256 |
|---|---|
| docs/08_总AI执行中心.md | a47d710be44361af3727363298f0b9a39d07d160bea1f65c8f7504fab8b27887 |
| docs/知乎OS执行协议.md | 43db9f6b8653769514dec0018c9e3462c5d7a019fd203bb5f174dd4cafe776c9 |
| templates/知乎OS总控提示词.md | 5a74d866473d5a5edb53c39c35ea953f2f22c74a9caaba6332b9e14f0f0679b4 |
| docs/Codex选题采集协议.md | 5f0b1945d1efce3c813d6f74b3fde5011ed4988e33f131dca41fe1f64f566a87 |
| templates/选题包模板.md | 1f42eb653ed60a5564ed59e443bdeb5628eaa3d01eddc73b9cbc88405cd369fc |

### Node Execution Assets

| path | sha256 |
|---|---|
| templates/Claude正文生产Prompt.md | 441f4f310a3e37459375ceef1964d74cecf04ccef7a0b88747fdc5f343670e66 |
| templates/GPT审核清单.md | 6db1a209139e3b97365f790afcb2f99d45f1b76b9a382bb39da4bf00e52b7abe |
| docs/知乎内容质量参数库_V2.md | 30533a3f4d9e656c669e9c432e5b3bb67cf0d2b080c1d4090f07efd53bee7586 |
| docs/生产状态机与交接规范.md | 7809fd027f30c63f64c6b4fa68d2e720bf18843236037cf41c087fac293de999 |
| data/Publish_Queue.md | 1cea7902a7c7e97835bd355bcdcafddc197841fdd69659e3e6bba48db0e52548 |
| templates/Failure Pattern模板.md | 3ea79dae80db29d8a6883fb2fe375bdcf42996d6fc2a8e9e059f00d37f52345e |

### Parameter & Knowledge Snapshots

| path | sha256 |
|---|---|
| production_variable_library.md | a3ae0358b4ec343abbfa3a4da95a62100e56472bf410360583fd9e7281c26944 |
| runtime/production_variable_snapshot.md | ee39d808cfdb09e86743a11164f0559d312e4e1ec0554b198f2e24e1522731c1 |
| runtime/知乎结构库快照.md | 4b3881d0ae2b6c56cdbb0f5fb58f2714225352e4b6089c3adc8ebcbb2442d5e2 |
| runtime/知乎ACTIVE规律快照.md | 8af2dacb4385ef2b710d6d279e6bc2e71e0d7b567bb17e6063b3625b7ae11665 |
| runtime/知乎内容质量参数快照.md | 3a782e2fca077df22e99af67560b80338107b021f90f6f4301fa842665321700 |
| runtime/知乎账号画像快照.md | be4bffffb6eb7916e11181b2006ce749434e1712767b547c2671dbcde72cf955 |
| docs/知乎OS Structure Evolution V1.md | a16d5b025ba8e89dc387561ee91d222b57c5a6a5f66b3c36c08b17575f9c9dae |

### Governance Infrastructure

| path | sha256 |
|---|---|
| scripts/validate_runtime_consistency.py | 9e1f00f2f35bd9edea4354cface7ca69c64680bf3609d34bf4eb03ff5c769fa0 |
| scripts/release_runtime.py | 1f45ee39f777abd5ced06418e5215ac51499cdefa113590870745ca3933d607a |
| docs/00-设计原则.md | 2a11524167fb4f1b24e7e2d8cf478adce3465ab3a27158f85ebe81b591f14e67 |

### Historical Asset Tools

| path | sha256 |
|---|---|
| skills/Skill000_历史资产检索器.md | 5c04e5aba74d92d6d4b518a20d48dbfff16bcbd847b32ffcbdc4c7ed3e8c0cda |
| scripts/search_historical_assets.py | 4051e8e1630ddb984b45db90073ea5497fef2cef0794e4bd72c2fb59e163e091 |

## Regression Tests

- （无；本次发布未声明可独立执行的回归测试脚本）
