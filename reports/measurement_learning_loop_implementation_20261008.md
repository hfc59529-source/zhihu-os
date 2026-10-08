# Measurement + Learning Loop 实施与验收

基线：`1452378`；本轮只修改测量/研究基础设施，未推广EXP008候选，未改选题权重、Compiler、正文Prompt、ACTIVE变量、系统治理原则或runtime发布资产。

## 1. 修改前后架构

修改前已有发布映射、主快照、收益观察、空的velocity表、Observation/Parameter治理与runtime一致性校验；固定窗口只有文档约定，研究到生产缺少可执行的限定批准校验。

修改后复用这些载体：发布映射 → Measurement Task → 人工/平台采集（部署缺口）→ 批量校验入库 → 数值增量与待判断任务 → 既有Observation/Case/Experiment研究 → 显式Validation结果 → Human Review → Scoped Promotion Approval → 具体生产变更校验。不会把记录类型按阶段转换，不要求所有研究最终成为规则。

## 2. 修改文件

- `scripts/learning_loop.py`：任务刷新、数据校验入库、数值增量、队列/历史metadata视图、限定Promotion校验。
- `scripts/validate_l0_assets.py`：合法缺失数值解析与缺失标记统计。
- `scripts/test_learning_loop.py`：19个直接相关测试。
- `.githooks/pre-commit`：提交前读取可信gate代码，检查暂存区批准及生产变更。
- `data/distribution_velocity_snapshots.csv`：只扩展既有空表字段，未增加历史固定窗口记录。
- `data/learning_loop_metadata.json`：一个既有EXP008阶段引用、四个UNKNOWN/PENDING生命周期随访登记；批准为空。
- `docs/Measurement_Learning_Loop.md`：执行契约、字段与Human Review边界。
- `reports/measurement_due_tasks.json`：派生到期任务与身份映射缺口。
- `reports/measurement_historical_metadata.json`：历史源行分类与哈希。
- `reports/lifecycle_numeric_deltas.json`：数值增量派生视图；当前为空。
- `reports/exp008_evidence_collection_queue.json`：三项待采集研究任务。
- `reports/exp008_pair02_blind_input.json`：不含结果/身份映射的两个入口片段。
- 本报告与README导航链接。

## 3. Schema与历史分类

velocity保留原13字段，新增production_id、target_window、due_at、observed_at、actual_age、timing_delta、timing_status、measurement_source、measurement_status、measurement_id、evidence_reference、measurement_window_start/end、earnings_window_start/end、earnings_match_status、attribution_status。单位为秒；未知值保持UNKNOWN。

`learning_loop_metadata.json` 仅为既有对象增加 publication_metadata / research_stage_records / lifecycle_observations / promotion_approvals 字段集合，不复制研究正文。批准除审核字段外绑定文件前后哈希、具体Git diff和证据文件哈希。

124条历史主快照只生成引用分类，不转成固定窗口；原始主快照、收益观察、L0、盲标、EXP008及其10月历史报告均保持字节不变。收益窗口保留原口径，没有插值、平均、收益缺失补0或反推小时窗口。

## 4. Measurement Task

启动执行 `python3 scripts/learning_loop.py refresh`。12条现有发布映射生成108个任务；当前108项均为PUBLISH_TIME_UNCERTAIN，因为没有可信含秒与时区的精确发布记录。L0中另外283个ID没有对应发布映射，明确显示MAPPING_REQUIRED，不假造Production ID。

未来精确登记的发布会产生due_at，区分SCHEDULED/DUE/CAPTURED/OVERDUE_MISSING_WINDOW。ON_TIME无隐含容差；迟采/早采保留偏差。已经得到的数据经ingest原子写入；同ID幂等，冲突拒绝。未采集或错过窗口不会被当前累计数据补齐。

## 5. Lifecycle Observation

四个Case-Control对象登记为UNKNOWN、证据采集待完成、Human Review PENDING。允许重复、跳跃和重叠，不自动标注REACTIVATION或LONG_TAIL。数值增量只比较同篇同来源累计端点，不用收益阅读替代内容管理阅读。阶段边界、置信度可UNKNOWN；批准须真实审核人和审核时间。

## 6. Research Stage

现有EXP008已到部分EVIDENCE，记录为现状metadata，不是机制Validation或新实验。之后由维护者根据证据/人工确认追加阶段记录，保留source_object/id/reference、track和transition字段；refresh不推进阶段。FAILED/INCONCLUSIVE可留在Validation或退回，不得进入RULE_CANDIDATE；它也不是ACTIVE。

Distribution和Monetization在契约中分轨；收益窗口和身份未核实时，earnings拒绝合并，保留ATTRIBUTION_UNKNOWN。窗口对齐也不构成因果证明。

## 7. Promotion Gate / 自动化边界

允许自动化：任务与缺口生成、数据校验/入库、时差与增量计算、研究队列与隔离材料生成、限定变更校验。

必须Human Review：生命周期解释、研究阶段决定、验证结论、反例检验、独立盲标、具体生产变更批准。PAIR-02仍是历史片段与当前350字片段；历史版本一致性UNKNOWN，整篇字段仍需全文。当前执行者未填写任何blind annotation。

Promotion要求源对象已通过Validation与反例检查，人工批准引用存在，批准范围对应目标，具体变更与全部证据哈希一致。未批准、FAILED/INCONCLUSIVE、证据变更、批准后扩大修改、EXP008来源均被拒绝。记录为空时不会因研究报告“已完成”而进入生产。

本地已安装core.hooksPath=.githooks；hook使用HEAD中gate代码校验index，避免未提交批准或gate替身放行。正常Topic Pool/Publish Queue/运行日志更新不被误认为研究规律推广。首次仅安装新的gate/hook，既有生产规则无豁免。该防线不能阻止人为绕过Git hook、修改配置或直接写磁盘；新clone和远端CI仍须部署，也不能凭JSON自行证明批准者身份。

## 8. UNKNOWN Validator

修复前：L0校验在10个数值单元格的UNKNOWN上失败。

修复后：空白、UNKNOWN、NA、N/A、NULL按合法缺失返回None；0仍是0，千/万单位沿用；非法与非有限数值仍拒绝。打印缺失标记统计。当前290行L0验证通过：477个空白数值单元格、10个UNKNOWN。没有改写历史数据，没有将未知收益变0。旧系统未建立NA/N/A/NULL统一业务含义，本轮只定义数值缺失含义，不擅自解释为“不适用”。

## 9. Runtime Drift诊断

- surface：manifest Protocol Docs → `docs/Codex选题采集协议.md`；影响日常选题排序权威的一致性。
- expected：Based On Commit `75535fa7b21de9d7f67c20a6330d8c6f5fef397e`；manifest SHA256 `5f0b1945d1efce3c813d6f74b3fde5011ed4988e33f131dca41fe1f64f566a87`。
- actual：SHA256 `d225418802e5e0363de9efe620ff8395c12b447c17cc8d6038cea5d94af79649`。
- source located：`905c9cb`（2026-09-14）增加Topic Priority Research Weight，领导/组织需求簇排序+1；文件已变，runtime仍以8月25日commit/hash为准。
- 本轮不判断该旧变更是否曾在其他渠道获批，不重算hash、不改Based On Commit、不rollback权重、不release。Runtime consistency仍原样报告INV-03/INV-04；需要单独治理决定。

## 10. 测试与保护校验

- Learning Loop：19个测试通过（时差/历史禁伪造/身份/收益对齐/原子幂等/阶段重复与未知/失败验证/反例/证据变化/限定diff/index隔离/运营记录边界）。
- 既有Consistency Engine：10个测试通过。
- L0 validation：290行通过。
- learning metadata / acquired measurement validation：通过。
- scoped promotion gate：通过，无生产变更获准或发生。
- runtime consistency：仍失败，仅上述既有INV-03/INV-04，未增加runtime漂移。
- 冻结源文件逐字节对比基线通过；Git diff whitespace校验通过。

## 11. Deployment Gap / UNKNOWN

没有后台scheduler、持久登录collector和远端强制门禁。所有当前映射的精确发布时间未知；历史固定年龄窗口仍未知；283个L0 ID缺Production映射。收益有效归因、受众、版本一致性、激活来源/日期/条件未验证。当前没有已获得的可信固定窗口样本，数值delta视图为空。指标来自平台显示，口径一致性仍须来源证据/人工检查。

## 12. 下次启动唯一第一动作

```sh
python3 scripts/learning_loop.py refresh
```

先看生成的到期/缺口任务，再由采集者取得真实数据。该动作不会自动运行知乎、完成盲标、推进研究或发布规则。
