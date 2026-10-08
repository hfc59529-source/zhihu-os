# Measurement + Learning Loop 执行契约

适用：发布后的测量与研究基础设施。不是内容规律、选题权重或正文规则，不进入 runtime；不修改《系统治理原则》的对象生命周期或生产验收权。

## 复用与权威

- 身份：`data/production_article_map.csv`；原有 run_id 映射继续使用。
- 日常快照：`data/review_data_snapshots.csv`；收益原始观察：`data/revenue_observations.csv`，本实现不重写二者。
- 固定窗口与日级累计端点：扩展已有 `data/distribution_velocity_snapshots.csv`，不是另一个主快照数据库。
- 研究正文、Case、Experiment、Observation 和 Parameter 保持原权威文件；`data/learning_loop_metadata.json` 只保存其阶段、生命周期观察和限定批准的辅助元数据，不复制证据正文，不新建 Evidence/Governance 对象。
- 人工验收仍使用现有治理和生产 REVIEW。Scoped Promotion Approval 不替代正文 USER_APPROVED，也不替代 runtime Release Approval。

## 唯一启动动作

```sh
python3 scripts/learning_loop.py refresh
```

读取已获得的数据并校验，生成 Measurement Due Tasks、数值增量、历史分类、EXP008 Evidence Collection Queue 与隔离的 PAIR-02 输入。命令没有网络采集和研究阶段推进能力。当前无 scheduler / persistent collector，状态为 `DEPLOYMENT_GAP_NO_SCHEDULER_OR_PERSISTENT_COLLECTOR`。关闭应用后不会准点运行；本地 Git hook 也不是 scheduler。

未来发布登记必须在现有发布映射中保留 article_id、production_id、精确时区时间及来源。脚本只信任含秒与时区的 ISO 时间；日期、近似时间、无时区一律降级。若补充精确时间，用辅助 metadata 的 `publication_metadata` 记录原映射 ID、`published_at`、`status=CONFIRMED` 和 `evidence_reference`；不猜测历史时间。

## Measurement

窗口：1h / 3h / 6h / 12h / 24h / 72h / 7d / 14d / 28d。

保留原 velocity 表字段，增加 production_id、target_window、due_at、observed_at、actual_age、timing_delta、timing_status、measurement_source、measurement_status、measurement_id、evidence_reference，以及阅读/收益有效窗口和归因状态。`checkpoint/collected_at/source` 作为兼容字段同步；时间差和实际年龄单位为秒。

任务状态：SCHEDULED / DUE / CAPTURED / OVERDUE_MISSING_WINDOW / PUBLISH_TIME_UNCERTAIN。只对精确对齐且 views 可得的记录标 CAPTURED；已有迟采记录不消除窗口遗漏。每次 refresh 根据原始数据重建任务视图，不覆盖研究决定。L0中没有发布映射的内容列为 MAPPING_REQUIRED，避免“没有任务”等同“没有缺口”。

ON_TIME 严格表示实际 observed_at 等于 due_at；没有隐含容差。任何偏差保留 EARLY / LATE。30h 数据仍是30h端点，24h任务仍显示错过。不精确发布时间的 due_at、偏差和年龄保持 UNKNOWN。若今后需要操作容差，应另行明确审核，不把容差内值当作精确时点。

采集者取得原始证据后，用 JSON 数组提交：

```sh
python3 scripts/learning_loop.py ingest --input /absolute/path/acquired_measurements.json
```

最小单条示例（值仅示范，不写入历史）：

```json
{
  "measurement_id": "article-id:24h:actual-observation-time",
  "article_id": "现有发布映射中的ID",
  "production_id": "现有Production ID",
  "target_window": "24h",
  "observed_at": "2026-10-10T12:00:00+03:00",
  "views": 100,
  "likes": 2,
  "comments": 0,
  "favorites": 3,
  "earnings": "UNKNOWN",
  "measurement_source": "知乎内容管理累计值",
  "evidence_reference": ["data/raw_exports/真实采集文件"]
}
```

全批通过身份、时间、数值、来源证据校验后原子入库。重复 measurement_id 的相同记录不重复写；不同记录拒绝覆盖。views等指标允许未知，未知不成为0。`REVIEW_DAY` / `HISTORICAL_BACKFILL` 也可作为非固定 target_window 保存已取得的日级端点；不能以这些数据窗冒充九个固定窗口。历史主表不会自动转入固定窗口表。

## Distribution / Monetization 分轨

Distribution 研究顺序：Question Context → Entry → Initial Distribution → Engagement → Further Distribution → Reactivation → Long-tail。它表达待观察关系，不预设因果。

Monetization：Question Context → Audience Composition（Candidate）→ Distribution → Monetization。Audience Composition 仍未验证。

分别保留 measurement_window_start/end、earnings_window_start/end、earnings_match_status 与 attribution_status。仅在同 article_id、相同有效累计起止窗口，并有证据支持时，才允许填固定观察行的 earnings；弱标题匹配和不同收益 cutoff 拒绝合并。不可对齐时 earnings=UNKNOWN，收益仍留原收入表，标 ATTRIBUTION_UNKNOWN。即使窗口对齐，也只标 `WINDOW_ALIGNED_CAUSAL_ATTRIBUTION_UNKNOWN`，不是因果归因完成。禁止把盐粒/阅读解释成稳定RPM。

## Lifecycle Observation

辅助 metadata 的 `lifecycle_observations` 每条包含 article_id、phase、phase_start/end、evidence_reference、confidence、status、review_status。phase 允许 INITIAL_DISTRIBUTION / STAGNATION / REACTIVATION / LONG_TAIL / UNKNOWN；confidence 可为 UNKNOWN。

允许重复、跳跃、重叠和未知边界。不自动推断 phase。系统仅对同篇、同测量来源的累计端点计算阅读增量、时间增量与每小时 velocity；回退计数、缺指标或零时间差保留 UNKNOWN_OR_COUNTER_REVISION，不能解读成负分发或激活。来源本身必须保留一致口径，平台口径变更应更换 source 并另记证据。

phase 最终接受需要人工 review_status=APPROVED、reviewed_by、reviewed_at；待审核可 PENDING，否定可 REJECTED。批准记录不能仅靠 Codex 推断填写。本轮没有把旧研究报告描述批量升级为已批准生命周期记录。

## Research Stage

辅助 metadata 中 `research_stage_records` 是追加记录，引用既有 source_object（Observation / Parameter / Case / Experiment）、source_object_id、source_reference。每次记录 research_stage、track、evidence_reference、transition_reason、transition_at、transition_by。

阶段：OBSERVATION / CASE / HYPOTHESIS / EVIDENCE / VALIDATION / RULE_CANDIDATE。不是对象类型，不替换 OPEN/VALIDATING/SUPPORTED 或 CANDIDATE/REVIEW/ACTIVE 等原生命周期。不要求逐阶段走完；允许撤回、失败、证据不足、回到早期阶段，永远不进入Rule。

维护者根据明确证据或人工确认追加 metadata，然后运行 validate；refresh 不修改这些记录。VALIDATION 要有 validation_result（PASSED / FAILED / INCONCLUSIVE）与 counterexample_check；FAILED / INCONCLUSIVE 不可进入 RULE_CANDIDATE。RULE_CANDIDATE 仍不具备生产触发资格。

## Scoped Promotion Gate

批准记录仍是现有研究对象的辅助记录，至少包含：research_object/id/reference、validated_claim、validation_result、counterexample_check、evidence_references；target_file、target_section（变量可在此标变量ID）、proposed_change、change_version；approved_by/at、approval_scope/status、human_approval_reference、promotion_timestamp；以及 before_sha256、after_sha256、diff_sha256 和 evidence_sha256（所有研究/证据/人工批准文件的路径哈希映射）。

必须有 PASSED Validation、PASSED 反例检查、明确人工批准文件，时间先后合法，且范围对应具体生产入口。批准绑定完整文件变更和 Git diff：审核后额外改变一字即失效；证据文件变化也使批准失效。不会自动改生产文件或 ACTIVE。EXP008 来源在本轮实现中硬性冻结，任何候选都不能获准Promotion；解冻需后续独立审核，不是本次任务的一部分。

```sh
python3 scripts/learning_loop.py promotion-check --staged
```

`.githooks/pre-commit` 对 staged index 执行上述校验：优先从 HEAD 取可信 gate 代码，不使用工作区未提交的 gate 替身；批准记录从 index 读取，相关证据文件必须与 index 一致。生产协议、模板、变量库、知识快照及门禁代码变更，无对应批准即阻止提交。生产运行日志不受规则Promotion门禁约束。

本次首次安装仅允许新增 gate/hook 自身；已有生产文件无 bootstrap 豁免。后续修改/删除 gate、hook 也须批准。该hook是本地提交防线，不能阻止 `--no-verify`、改Git配置或直接编辑文件；跨机器和远端需安装hook或接入CI。它也不能凭JSON证明审核人身份；真实人工批准必须有可信审核来源，禁止执行者伪造。

仓库本地安装：`git config --local core.hooksPath .githooks`。新 clone 需安装；本轮不修改 manifest/release脚本，不宣称 runtime 已接受这些新基础设施。

## UNKNOWN 与历史迁移

数值 validator 接受空值、UNKNOWN、NA、N/A、NULL为缺失，返回None，不换成0。旧代码只有空值或部分模块UNKNOWN约定，未发现统一NA/N/A/NULL业务语义；本次仅定义其数值缺失含义，不据此宣布“不适用”。原字符串保留，需进一步区分“不适用”时另行提供证据。

历史迁移只生成 `reports/measurement_historical_metadata.json`：源行引用/哈希、原window、生产ID或UNKNOWN、固定窗口/发布时间/归因未知状态。不覆盖原CSV、不改历史EXP008、不拆分收益窗口、不插值。收益报表 window 字段继续是其真实报告窗口，不能改为内容年龄。

## 验证

```sh
python3 scripts/test_learning_loop.py
python3 scripts/test_validate_consistency_engine.py
python3 scripts/validate_l0_assets.py
python3 scripts/learning_loop.py validate
python3 scripts/validate_runtime_consistency.py
```

Runtime consistency 的既有 drift 单独报告；不得以自动重算hash、替换Based On Commit或重新release把失败变成通过。
