# 知乎本地执行快照清单

执行版本：ZH-RUNTIME-V3.0-TEACHER

状态：ACTIVE

发布时间：2026-07-31 13:07:05 +03:00

发布类型：完整 runtime 发布修复

修复目标：老师结构规则进入 ACTIVE runtime，Production Card 改为结构实例化施工卡，禁止旧变量模型临场拼正文结构。

## 版本一致性校验结果

结果：PASS

一致版本：

- MASTER：ZH-RUNTIME-V3.0-TEACHER
- 执行协议：ZH-RUNTIME-V3.0-TEACHER
- 总控 Prompt：ZH-RUNTIME-V3.0-TEACHER
- 结构库快照：STRUCT-V3.0-TEACHER
- Skill006：ZH-RUNTIME-V3.0-TEACHER
- Production Card 模板：ZH-RUNTIME-V3.0-TEACHER
- 质量参数快照：ZH-RUNTIME-V3.0-TEACHER
- ACTIVE 规律快照：ZH-RUNTIME-V3.0-TEACHER

## 当前 ACTIVE 执行文件

| 模块 | 文件路径 | SHA256 | 来源权威 |
| --- | --- | --- | --- |
| MASTER | docs/08_总AI执行中心.md | 7ae7b7cce77ac14f36ec586578333727d5c94b03a384796c53d1da32a0b696e0 | 本地 MASTER |
| 执行协议 | docs/知乎OS执行协议.md | cc120456ffca3f5a336c5b2098257a3dda93ca4d9a066f88105626dd55231990 | 本地协议层 |
| 总控 Prompt | templates/知乎OS总控提示词.md | ef534aeacb7cf4f8ee2c39aa6764ef94d334f67566f0eb517b4ba12a3ef3dbe4 | 本地 Prompt 模板 |
| Production Card 模板 | templates/Production Card模板.md | 73d55b5b307096a365a8582e98605b7f03cdc11b980ec493b011dfa2455651bd | 本地模板层 |
| Production Card 生成 | skills/Skill006_知乎生产卡生成器.md | 77835c9a26e9e1b8abdc76813d3391557e294d8fe51dc4de958b2d6f645f6102 | 本地 Skill |
| Production Card 校验 | scripts/validate_production_card.py | bafb71220ba914fa42387eba9b75058d3707b74eb48bc69a08dd9ef2c7d374f7 | 本地校验脚本 |
| runtime一致性校验 | scripts/validate_runtime_consistency.py | 82dc977810792233f04dbeafa886be38e15b0ef39b18bd0609ae9a5bd0e85b31 | 本地校验脚本 |
| ACTIVE 结构 | runtime/知乎结构库快照.md | 8a0d2c841153c43667d3de9805683fc03ba84be48c1d284894dc17e3f57b76c2 | runtime 发布快照 |
| ACTIVE 规律 | runtime/知乎ACTIVE规律快照.md | 4ad77a341a9327a981ef89b77d26e90b24ca06fd04486226f99f1dda0ed06e1c | runtime 发布快照 |
| 内容质量参数 | runtime/知乎内容质量参数快照.md | 3b27c59b0cd880ee17b57967e8b78a94b3c84d45f209df0386fe4af0f18c77a8 | runtime 发布快照 |
| 账号画像 | runtime/知乎账号画像快照.md | be4bffffb6eb7916e11181b2006ce749434e1712767b547c2671dbcde72cf955 | runtime 发布快照 |
| 内容变量参数库 | production_variable_library.md | 6c19adb77971cfe34c6fbfe90049f4196c465d53fff4476ada137d62d057bdbb | 本地变量总库 |
| 历史资产检索器 | skills/Skill000_历史资产检索器.md | 82f48725cecd497a4078854bb3d94e6ab19063dc4e20d15fdac419abb100208b | 本地 Skill |
| 历史资产检索脚本 | scripts/search_historical_assets.py | c0951268d65fa5469ae378429bfbb9fa166dbe0d6d38e9ff1531620cd8a57525 | 本地脚本 |

## 当前生产链

```text
题目识别
↓
选题准入
↓
读取本清单
↓
执行历史资产检索
↓
读取 ACTIVE 老师结构
↓
L1 选择一个 ACTIVE 结构
↓
读取结构完整推进字段
↓
完成本题结构实例化
↓
读取 ACTIVE 规律和内容变量作为材料
↓
后台质量参数检查
↓
生成正文施工卡
↓
执行 validate_production_card.py
↓
交付可复制 Claude版 Production Card
↓
写入本地运行日志
```

## 生效原则

只有本清单列出的文件可以决定正式生产。

未列入清单的历史文件、草稿文件、归档文件不得进入生产调用。

Notion 是管理权威；runtime MD 是 Codex 日常生产的执行权威。Notion 内容修改不自动生效，只有完成快照发布并更新本清单版本后才进入生产链。

正式生产必须引用 `runtime/知乎结构库快照.md` 中状态为 ACTIVE 的老师结构。禁止使用 STRUCT-V2.1 等抽象通用结构临场拼装正文段式。

内容变量、PD、RR、RE、BT 和 CR 只作为后台检查与内容补充，不得决定正文骨架，不得在 Claude 施工卡中展开 26 维审计。

## 已设计 / 已发布规则

任何协议优化必须区分：

- 已设计：规则已经讨论、确认或形成草案，但尚未进入 runtime。
- 已发布：权威源修改 → runtime 重新生成 → manifest 更新 → 版本一致性校验 → 回归测试通过。

只有达到“已发布”，才允许进入正式生产调用。

## 必检脚本

- scripts/validate_production_card.py
- scripts/validate_reasoning.py
- scripts/validate_runtime_consistency.py
- scripts/assemble_writer_input_package.py
- scripts/match_structure.py
- scripts/validate_obligation_coverage.py
- scripts/search_historical_assets.py
