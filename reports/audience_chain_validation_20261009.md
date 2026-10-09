# Audience Evidence 接入验证 — 2026-10-09

## 修改范围

- reports/audience_evidence_20261009.md：用户确认的原始画像、窗口、来源限制、解释边界及本次直接授权。
- data/production_reference.md：追加 REF-20261009-AUDIENCE，全部旧行保留。
- data/learning_loop_metadata.json：追加 DATA_FINDING 人工接受记录及两个目标文件的限定授权与证据/变更哈希；不改历史授权。
- docs/Codex选题采集协议.md：复用生产前读者校准入口和既有 Topic Package 字段，接入七步 Audience Gate。
- 本报告：保存实际检查结果。

## 实际检查

- python3 -m unittest discover -s scripts -p 'test_*.py'：34 tests，OK。
- python3 scripts/validate_l0_assets.py：290行，PASS；保留原有缺失值，不补零。
- python3 scripts/learning_loop.py validate：PASS。
- python3 scripts/learning_loop.py promotion-check：PASS。
- git diff --check：PASS。
- 读取链路断言：PASS。协议在每次 Daily_Topic_Top3 前要求读取当前清单、源报告和接受记录；新 ID 同时存在于协议、清单、metadata；源与接受文件真实存在；全部旧 Reference 行仍在。选题生成 Topic Package 进入 INPUT 前要求再次核对，记录复用现有字段。
- 边界断言：PASS。协议明确禁止固定权重/总分、画像不匹配自动 Kill，允许未来数据推翻，不要求泛商业号转型。

这是一条由 Codex 执行的文档协议读取链路，仓库没有独立自动化 Daily_Topic_Top3 生成器。本次验证证明入口与引用可达及资格完整；未采集新候选或运行真实选题，不能声称已观察到下一轮生产效果。

## Runtime 漂移（只报告）

python3 scripts/validate_runtime_consistency.py 返回1：
- INV-03 sha256 mismatch: docs/Codex选题采集协议.md
- INV-04 disk content diverges from Based On Commit: docs/Codex选题采集协议.md

只读基线复查：在校验器内将该文件哈希读取替换为 HEAD 文件字节的哈希，其余校验保持原样，仍报告相同两项错误。说明该协议在本次修改前已经偏离 Runtime Manifest；本次继续改变协议，但没有增加其他文件的漂移项。按用户要求不修改 Manifest、不发布 Runtime、不扩大历史修复范围。

START_HERE.md、AGENTS.md 在本仓库不存在；使用 README 与现有生产协议了解约定，没有借用其他项目的同名文件。
