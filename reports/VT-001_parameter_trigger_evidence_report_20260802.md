# VT-001 Parameter Trigger Evidence Report

日期：2026-08-02

状态：EVIDENCE REPORT

执行边界：

- 使用现有数据库。
- 不新增样本。
- 不重新采集。
- 不修改系统。
- 不输出建议。
- 只按 Question → Production Card → Parameter → Match 输出事实。

样本口径：223、60、24、13、6、5。

Match 取值：MATCH / MISMATCH。

## Evidence Table

| 阅读 | Production / Run ID | Question | Production Card | Parameter | Match |
|---:|---|---|---|---|---|
| 223 | `zhihu-20260729-senior-leader-not-fired-001` | 题主问：公司高层能力不行，为什么大老板仍不裁掉他们；真实问题是高层任免为什么不按“能力差就替换”运转。 | Card 认为：表面问能力，真实问老板为什么容忍低效高层；核心不是老板看不出来，而是替换高层会触发权力、资源、责任和风险重排。 | 显式调用：`组织风险押注`；辅助变量：组织视角、风险传导、利益重分配；核心参数：PD-03 机制推导、PD-04 利益结构、PD-05 权力资源、PD-06 博弈推导、PD-08 认知升级。 | MATCH |
| 60 | `zhihu-20260729-fuzzy-responsibility-boundary-001` | 题主问：领导布置任务故意模糊责任界限，基层员工如何在不得罪人的前提下保护自己；真实问题是低权力位置如何确认责任、避免背锅。 | Card 认为：读者不是不知道要确认任务，而是不敢确认；要在权力关系、绩效评价和资源关系不受损的前提下自保。 | 显式调用：`风险传导`；辅助变量：组织视角、认知校正；核心参数：PD-03 底层逻辑推进、约束识别/权力关系、行动建议/场景覆盖、信息价值/边界澄清、BT-01 收藏动作。 | MATCH |
| 24 | `ZH-20260801-003` | 题主问：领导把任务拿走，几个月后别人干不了又想还给自己，自己该怎么做；真实问题是如何既不当冤大头，又不撕破关系。 | Card 认为：这不是原任务还给你，而是失败后的新任务；任务已变质，必须重新确认权责、资源和退出条件。 | 显式字段未列“质量参数调用”；Card 实际调用：责任边界、权责重分配、风险回流、重新立项、授权、资源、留痕、退出条件；ACTIVE-TS02 老师解决题场景施工结构。 | MATCH |
| 13 | `ZH-20260802-001` | 题主问：被提拔成部门负责人，第一件事该做什么；真实问题是从资深经办变负责人后如何避免越界、做错、被原同事看轻。 | Card 认为：第一件事不是选一个具体动作，而是先完成权力、关系和信息三重校准，否则任何动作都可能踩雷。 | 显式字段未列“质量参数调用”；Card 实际调用：决策、角色转换、权力边界、关系重置、信息真伪、授权、资源、汇报节奏；ACTIVE-TS02 老师解决题场景施工结构。 | MATCH |
| 6 | `ZH-20260801-001` | 题主问：职场中怎么改掉弱者气息；真实问题是不知道弱者气息来自性格、能力、表达，还是别人对自己的判断。 | Card 认为：弱者气息不是不够凶，而是别人看不见边界、交换价值和后果预期；正文要给三个稳定判断标准。 | 显式字段未列“质量参数调用”；Card 实际调用：成长、边界、交换价值、后果预期、组织信号、自查框架、BT-01 收藏动作；ACTIVE-TS01 老师爆款机制推进结构。 | MATCH |
| 5 | `ZH-20260731-unknown_mofish` | 题主问：老板明知员工摸鱼为什么不拆穿；从现有正文看，真实问题被处理为老板是否看见与为什么不管。 | 未找到对应 Production Card；本地仅有 `draft_mofish.md` 和 `reports/review_ZH-20260731-unknown_mofish_v1.md`，复盘记录写明 Production Card、ACTIVE、Primary Goal、Monetization Goal、Consistency Engine、四项语义审核均未找到。 | 无可验证的 Production Card 参数调用记录；只能从正文观察到管理成本、证据成本、时机成本、替代成本，但这些不是可追溯的卡片参数调用。 | MISMATCH |

## Match Count

| 分组 | 样本 | MATCH | MISMATCH |
|---|---|---:|---:|
| 高表现 | 223、60 | 2 | 0 |
| 低表现 | 24、13、6、5 | 3 | 1 |
| 合计 | 223、60、24、13、6、5 | 5 | 1 |

## Evidence Notes

| 阅读 | 证据文件 |
|---:|---|
| 223 | `reports/production_20260729_senior_leader_not_fired_card.txt` |
| 60 | `reports/production_20260729_fuzzy_responsibility_boundary_card.txt` |
| 24 | `productions/ZH-20260801-003/Card-v1.md` |
| 13 | `productions/ZH-20260802-001/Card-v1.md` |
| 6 | `productions/ZH-20260801-001/Card-v1.md` |
| 5 | `draft_mofish.md`; `reports/review_ZH-20260731-unknown_mofish_v1.md` |
