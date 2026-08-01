# ZH-MILESTONE-010

复盘范围：ZH-20260801-002 至 ZH-20260801-010

复盘原则：本报告不新增协议、不新增参数、不改 Prompt、不改流程。只做证据归纳、参数有效性审计、采样验收和 Observation 治理。

## 1. 工程验收

结论：生产流水线稳定。

样本统计：

| 指标 | 结果 |
|---|---:|
| 新流程样本 | 9 |
| Clean Pass | 5 |
| Issue | 4 |
| Clean Pass 率 | 56% |
| Issue 率 | 44% |
| Final Validation 通过率 | 100% |
| Patch 后回退 | 0 |
| 误判 Issue | 0 |

工程判断：

- Codex 能稳定产出 `Top3_Context → Card-v1 → Draft-v1 → Comparison_Report`。
- Claude 已能给出 Clean Pass，不再为了证明价值而制造 Issue。
- GPT 裁决稳定在 PASS / Approve / Revise，没有重新写文章。
- Patch 后没有引入新 Bug，说明修补链路可控。
- Ledger、Publish Queue、Release-v1、Final_Validation 能追溯生产状态。

工程验收结果：PASS。

## 2. 参数验收

本节只审查当前可生产调用的 ACTIVE 参数：CV001-CV006。候选发现只保留在 Comparison_Report 和 Observation 中，不在本次直接升级。

### 参数审计表

| 参数 | 判定 | 证据摘要 | 治理建议 |
|---|---|---|---|
| CV001 认知校正 | Supports | 002-010 多数 Card 与 Draft 都依赖“把表层问题改成机制问题”：边缘化不是闲、叫醒不是礼貌、跳槽不是动作、汇报不是邀功。Top3 也普遍通过反转获得续读。 | 保留 |
| CV002 利益重分配 | Non-discriminative | 003、007 等权责题明显适用，但 004、009、010 等能力/汇报题区分力弱。不是无效，而是题型依赖强。 | 保留，题型触发更谨慎 |
| CV003 组织视角 | Supports | 004-010 高频有效：高潜、边缘化、应急升级、笨领导、跳槽、工作厉害、汇报可见化，都能用组织信息、资源、责任链解释。 | 保留，当前最稳参数之一 |
| CV004 风险传导 | Supports | 003、005、006、007、010 明显支持；Top3 常用风险场景制造判断，Draft 通过风险清单和留痕缩小差距。 | 保留 |
| CV005 身份代入 | Not observable / 弱支持 | 006 的市长视角、007 的领导安全感、010 的领导决策视野可支持，但多篇 Draft 更偏分析，未稳定证明该参数能区分 Top3 与 Draft。 | 继续观察 |
| CV006 结尾动作 | Non-discriminative | 几乎所有 Draft 都有结尾动作或判断，但 Top3 不一定依赖结尾动作取得优势。006/007 的结尾问题还说明该参数容易与施工重复混在一起。 | 保留但降权观察，不作为质量充分条件 |

### 参数验收结论

- 已有参数有解释力，但强弱不均。
- 最有解释力：认知校正、组织视角、风险传导。
- 题型依赖强：利益重分配。
- 证据不足：身份代入。
- 有效但不区分质量：结尾动作。

当前不能证明“参数已经让 Draft 接近 Top3”。能证明的是：部分参数能解释 Top3 与 Draft 的共同高价值结构，但 Comparison_Report 之前没有系统做 `Supports / Contradicts / Non-discriminative / Not observable`，参数性能测试仍需在 011 之后正式补齐。

## 3. 采样验收

结论：Top3 采样对生产有帮助，但采样质量不稳定。

支持证据：

- 003：Top3 暴露“极端立场/历史叙事/短金句”已充分表达，Draft 转向可执行边界。
- 004：Top3 多为特征清单，Draft 转向边界场景观察法。
- 006：Top3 已吃透“当然叫醒”的段子爽感，Draft 转向升级标准和汇报话术。
- 008：Top3 的“坐电梯/乘客司机”提醒 Draft 不能做抽象二选一，转向位置复利。
- 009：Top3 小动作和底层气质样本推动 Draft 选择“交付确定性”。

限制证据：

- 002、004、005、006、007、008、009、010 的 Ledger 中 Top3 Source 多写为“未记录（见 Top3_Context.md）”，结构化统计不够。
- 010 的 Top3 元信息不完整，可信度低于 006-009。
- Default Ranking 有用，但还不能证明它优于赞同排序或邀请入口；需要继续回填入口与发布表现。

采样验收结论：

- Default Ranking Top3 可以继续作为日常生产主入口。
- 但每篇必须更稳定记录 Sample Source、作者、赞同数、默认排序位置和采样可信度。
- Topic Pool 的入口实验要继续，不能提前判断哪个入口最优。

## 4. Observation 治理

| Observation | 状态 | 证据 | 处理 |
|---|---|---|---|
| Observation-01 尾段重复压缩 | Closed | 006/007 YES，008/009/010 NO | 不升级为参数或协议变更；判定局部巧合 |
| Observation-02 Card字段重叠 | Open | 010 单篇：Card 两个字段表达同一判断，Draft 忠实落地形成首尾相似 | 继续观察 011/012/013，不修改 Card |

## 5. 里程碑结论

ZH-MILESTONE-010 达成 Version 1.0 工程验收：

- 生产稳定：PASS
- 证据驱动：PASS
- 可追溯：PASS
- 可演化：PASS

但参数验收尚未完成到可升级系统的程度。下一阶段最重要的不是继续扩张流程，而是把 Comparison_Report 改成真正的参数性能测试入口：对 ACTIVE 参数逐项判断 `Supports / Contradicts / Non-discriminative / Not observable`。

本报告不直接修改协议。若要进入 Version 1.1，应另开治理任务，基于本报告处理：

- Comparison_Report 的参数审计结构化；
- Top3 Source 记录字段标准化；
- CV005 / CV006 的继续观察；
- Observation-02 的后续样本追踪。
