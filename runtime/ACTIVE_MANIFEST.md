# Runtime Manifest

Runtime Version: ZH-RUNTIME-DRAFT
Status: TRIAL
Published At: 2026-08-10 12:52:59 UTC
Based On Commit: 8b8d8d1bce663022741b40cda3f9ca7664b09cd6

## Partitions

### Compiler Authority

| path | sha256 |
|---|---|
| docs/知乎OS Compiler V1.md | 24538815db70ed4904fc51d7db7be5ab1440f38b26048f642ec565f0d8d9af50 |
| docs/内容架构总则.md | cdf1c858368dec970170f646f6d9fc98aa0d411348e1b63c0f2927e785e70714 |
| docs/知乎OS权威归属表.md | d161328f2dce7b216a45ebf8a6ff6198b9a15642249f7e08efcc092a75d303bb |

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
| templates/Claude正文生产Prompt.md | b9164c0e9ded19e883bbf85320bc20b1d0012e6060eacafc8a8253581a5c2f55 |
| templates/GPT审核清单.md | 252a04b3fdeac9ae997d7fbfd8bf0221bffdfbc7ce245cca7b6d83873c2b64a7 |
| docs/知乎内容质量参数库_V2.md | ebb5cdc46488b6b1426b6803521126864c4779f7a6546d860114d8cd6063d007 |
| docs/生产状态机与交接规范.md | 2f5c4b0e8222b99b3594f19a4e550c291492f3f9360fa015ef838fd9d761ab99 |
| data/Publish_Queue.md | c80c80562484815d8eb483ba0d2aae74f0ab5ebd2720db50c2e520a59207441a |
| templates/Failure Pattern模板.md | 1edb33ed19074e0e6ca3dd8d0418c62eca55682cc9bf2b799239f0ae767175c7 |

### Parameter & Knowledge Snapshots

| path | sha256 |
|---|---|
| production_variable_library.md | 463739bff19304810076f2beeadb414b0676cf0d212d97cf2413721eacf9259e |
| runtime/production_variable_snapshot.md | 5666624c9f6c1dd56ceaeb689004e58684dec42f6a899cd1be1d0c65c9a159c1 |
| runtime/知乎结构库快照.md | 8a0d2c841153c43667d3de9805683fc03ba84be48c1d284894dc17e3f57b76c2 |
| runtime/知乎ACTIVE规律快照.md | 4ad77a341a9327a981ef89b77d26e90b24ca06fd04486226f99f1dda0ed06e1c |
| runtime/知乎内容质量参数快照.md | 3b27c59b0cd880ee17b57967e8b78a94b3c84d45f209df0386fe4af0f18c77a8 |
| runtime/知乎账号画像快照.md | be4bffffb6eb7916e11181b2006ce749434e1712767b547c2671dbcde72cf955 |
| docs/知乎OS Structure Evolution V1.md | a16d5b025ba8e89dc387561ee91d222b57c5a6a5f66b3c36c08b17575f9c9dae |

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
