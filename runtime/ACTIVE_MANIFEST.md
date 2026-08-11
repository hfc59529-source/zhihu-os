# Runtime Manifest

Runtime Version: ZH-RUNTIME-DRAFT
Status: TRIAL
Published At: 2026-08-11 13:20:02 UTC
Based On Commit: 7f06b81ce5a46f85b7c93f95320a47198c9c29ac

## Partitions

### Compiler Authority

| path | sha256 |
|---|---|
| docs/知乎OS Compiler V1.md | 8101224c99bf9a838a0114227811e48fe9b1582379f72bd5532409537f81356c |
| docs/内容架构总则.md | cdf1c858368dec970170f646f6d9fc98aa0d411348e1b63c0f2927e785e70714 |
| docs/知乎OS权威归属表.md | 705b59dd69b943b90d0771010a58d4f5a92b44b5d7a984029cf26141e116dd57 |

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
| templates/GPT审核清单.md | 631082a9cb7f41424b7e95801ee33e360db0c2db34d17d89f11b099812adb792 |
| docs/知乎内容质量参数库_V2.md | ebb5cdc46488b6b1426b6803521126864c4779f7a6546d860114d8cd6063d007 |
| docs/生产状态机与交接规范.md | b755809eb3c357496eb2643bf73494d69dea00e156a90a791045334c15560cd2 |
| data/Publish_Queue.md | 0e166254884230f0390e7480424efb978b4499498b527afdea66855e22839828 |
| templates/Failure Pattern模板.md | 3ea79dae80db29d8a6883fb2fe375bdcf42996d6fc2a8e9e059f00d37f52345e |

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
