# Runtime Manifest

Runtime Version: ZH-RUNTIME-DRAFT
Status: TRIAL
Published At: 2026-08-09 18:21:51 UTC
Based On Commit: 2d8fdbf49a70c9bb65c4b3d4c35f857d415fdc96

## Partitions

### Compiler Authority

| path | sha256 |
|---|---|
| docs/知乎OS Compiler V1.md | 5d7bed21283cc5c3a877620aaaeab75623276d26e766fa4b53c9781e6ec11589 |
| docs/内容架构总则.md | cdf1c858368dec970170f646f6d9fc98aa0d411348e1b63c0f2927e785e70714 |
| docs/知乎OS权威归属表.md | 765f3fedc4fbdb5c75715834edf38dd77eda2d878ced9dc867ee2b5b63795cd8 |

### Protocol Docs

| path | sha256 |
|---|---|
| docs/08_总AI执行中心.md | 2aaa8132326d2804a4c2e5bd9d3293164cee9c9868e3e9e720cfd22d1867c98c |
| docs/知乎OS执行协议.md | b93281e54ff3a71ecadce59bef7f954c85dcebcdf08773249378c077b761aa54 |
| templates/知乎OS总控提示词.md | 5a74d866473d5a5edb53c39c35ea953f2f22c74a9caaba6332b9e14f0f0679b4 |
| docs/Codex选题采集协议.md | 8c52b6a1128ef147411175ee8fe1c26d8c8f033174132ff05be33bcb0b81752f |
| templates/选题包模板.md | 41d97f3a9b1ce71d1df1dd105debaadcd36932dc1019ccbdbfea6b44b3309717 |

### Node Execution Assets

| path | sha256 |
|---|---|
| templates/Claude正文生产Prompt.md | 635f9082ec33a33aa45ec6cf66a7790854a0cc4fb964a33147a7b15efc93c4fd |
| templates/GPT审核清单.md | 252a04b3fdeac9ae997d7fbfd8bf0221bffdfbc7ce245cca7b6d83873c2b64a7 |
| docs/知乎内容质量参数库_V2.md | ebb5cdc46488b6b1426b6803521126864c4779f7a6546d860114d8cd6063d007 |
| docs/生产状态机与交接规范.md | 2f5c4b0e8222b99b3594f19a4e550c291492f3f9360fa015ef838fd9d761ab99 |
| data/Publish_Queue.md | c80c80562484815d8eb483ba0d2aae74f0ab5ebd2720db50c2e520a59207441a |
| templates/Failure Pattern模板.md | 1edb33ed19074e0e6ca3dd8d0418c62eca55682cc9bf2b799239f0ae767175c7 |

### Parameter & Knowledge Snapshots

| path | sha256 |
|---|---|
| production_variable_library.md | 562df06541120f4089321c0ad68c93c178636d04a708c1929709bcd9b65d31b4 |
| runtime/production_variable_snapshot.md | 5666624c9f6c1dd56ceaeb689004e58684dec42f6a899cd1be1d0c65c9a159c1 |
| runtime/知乎结构库快照.md | 8a0d2c841153c43667d3de9805683fc03ba84be48c1d284894dc17e3f57b76c2 |
| runtime/知乎ACTIVE规律快照.md | 4ad77a341a9327a981ef89b77d26e90b24ca06fd04486226f99f1dda0ed06e1c |
| runtime/知乎内容质量参数快照.md | 3b27c59b0cd880ee17b57967e8b78a94b3c84d45f209df0386fe4af0f18c77a8 |
| runtime/知乎账号画像快照.md | be4bffffb6eb7916e11181b2006ce749434e1712767b547c2671dbcde72cf955 |
| docs/知乎OS Structure Evolution V1.md | 5bd43dfd22ddb989e210bbd313aa5a264572dae7d04630427bad0b02ab9b1cf7 |

### Governance Infrastructure

| path | sha256 |
|---|---|
| scripts/validate_runtime_consistency.py | 016d77cccd1d3f051d353981f32fd8770afef149a448a29da954351befa00efb |
| scripts/release_runtime.py | 1f45ee39f777abd5ced06418e5215ac51499cdefa113590870745ca3933d607a |
| docs/00-设计原则.md | 7634ea13f99428ff3916a9d092cd1ffac6c4b0292f4aefd1670e81adfb56fe62 |

### Historical Asset Tools

| path | sha256 |
|---|---|
| skills/Skill000_历史资产检索器.md | 82f48725cecd497a4078854bb3d94e6ab19063dc4e20d15fdac419abb100208b |
| scripts/search_historical_assets.py | c0951268d65fa5469ae378429bfbb9fa166dbe0d6d38e9ff1531620cd8a57525 |

## Regression Tests

- （无；本次发布未声明可独立执行的回归测试脚本）
