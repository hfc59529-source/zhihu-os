# RR 阅读体验参数树深化与执行闭环建设｜2026-07-29

## 结论

本轮已完成 RR 阅读体验参数树兼容式重构，并接入 Production Card 调用口径、Claude 正文 Prompt、Skill007 正文 QA 和程序化辅助校验脚本。

验收结论：PASS。

## 修改文件清单

| 文件 | 修改摘要 |
| --- | --- |
| `runtime/知乎内容质量参数快照.md` | 将 RR 从 6 个旧模块扩展为 8 个阅读体验模块，补充固定定义结构、QA 检查、严重级别、参数关系和迁移表。 |
| `docs/知乎内容质量参数库_V2.md` | 追加 RR 阅读体验参数树深化说明、调用纪律、历史迁移表和执行闭环。 |
| `skills/Skill006_知乎生产卡生成器.md` | 将质量参数审计口径从 24 维更新为 26 维；RR 目录改为 8 个阅读体验模块。 |
| `templates/Claude正文生产Prompt.md` | 新增阅读体验执行顺序、RR-07 阅读疲劳自检和 RR-08 认知吸收自检。 |
| `skills/Skill007_正文QA协议.md` | 将 RR 硬闸门升级为阅读负荷审计，增加 PASS / REVISE / BLOCK 判定。 |
| `scripts/validate_reading_experience.py` | 新增程序化 RR 辅助检测脚本，只统计可量化信号，不判断语义。 |
| `scripts/validate_runtime_consistency.py` | 将新 RR 检测脚本纳入 runtime 一致性必需脚本。 |
| `README.md`、`docs/08_总AI执行中心.md`、`docs/知乎OS执行协议.md`、`runtime/ACTIVE_MANIFEST.md`、`templates/单次任务模板.md` | 将质量参数审计口径统一为 26 维。 |

## RR 参数完整目录

1. RR-01｜认知负荷控制
2. RR-02｜信息密度控制
3. RR-03｜认知缓冲
4. RR-04｜阅读节奏
5. RR-05｜现实承接
6. RR-06｜阅读奖励
7. RR-07｜阅读疲劳检测
8. RR-08｜认知吸收校验

## 旧参数迁移表

| 旧参数编号 | 旧参数名称 | 新归属 | 是否保留编号 | 是否废弃旧定义 | 兼容说明 |
| --- | --- | --- | --- | --- | --- |
| RR-01 | 阅读类型切换 | RR-01 认知负荷控制 / RR-04 阅读节奏 | 是 | 否 | 原“连续解释切换”并入 RR-04-04，RR-01 扩展为认知负荷总控。 |
| RR-02 | 单段推进 | RR-02 信息密度控制 / RR-01-02 单段认知任务 | 是 | 否 | 原“每段新增信息”保留，改为密度和单段任务约束。 |
| RR-03 | 现实观察率 | RR-03 认知缓冲 / RR-05 现实承接 | 是 | 否 | 原现实观察率保留，固定字数要求降级为机制节点和场景绑定。 |
| RR-04 | 认知奖励频率 | RR-04 阅读节奏 / RR-06 阅读奖励 | 是 | 否 | 原关键推导后奖励保留，增加奖励数量上限。 |
| RR-05 | 节奏起伏 | RR-04 阅读节奏 | 是 | 否 | 原节奏起伏并入 RR-04 总控，保留历史调用兼容。 |
| RR-06 | 阅读疲劳检测 | RR-07 阅读疲劳检测 / RR-08 认知吸收校验 | 是 | 否 | 原生成后自检升级为可量化疲劳检测和语义吸收校验。 |

## Claude Prompt 新增内容

- 生成前确定唯一主判断。
- 全文最多三个认知任务。
- 每个认知任务绑定现实场景。
- 按“场景→解释→判断→缓冲→下一层解释”生成。
- 连续两个新判断后插入场景、对话、动作、观察或停顿。
- 行动建议阶段降低认知密度。
- 结尾不得新增理论。
- 完成 RR-07 与 RR-08 自检。

## QA 新增内容

新增“阅读负荷审计”：

- 唯一主判断
- 独立判断数量
- 连续抽象段落最大值
- 连续解释段落最大值
- 现实场景数量
- 人物语言数量
- 超长句数量
- 抽象名词密集区
- 一句话复述
- 普通读者理解
- 最终结论：PASS / REVISE / BLOCK

## 校验脚本说明

新增 `scripts/validate_reading_experience.py`，检测：

- 句子长度统计
- 段落长度分布
- 连续无人物 / 动作 / 场景段落数
- 连续解释段落数
- 抽象词密度
- 培训式表达频率
- 一句话一段比例

脚本不判断：

- 是否存在唯一主判断
- 场景是否真正承担理解功能
- 是否像讲课
- 普通读者是否能理解
- 是否出现重复解释

## 三篇测试结果

### 测试一｜认知较浅但阅读轻松旧文

文件：`reports/production_20260728_partner_split_article.txt`

- RR 检测结果：高风险
- 主要疲劳点：连续 17 段无人物、动作、场景或具体对象；一句话一段比例 0.89
- 应删内容：重复的短句判断
- 应转场景内容：抽象判断后的现实分手、沟通或关系场景
- 应保留核心判断：原文主判断
- 优化前后字数：未自动修改
- 优化前后核心判断数量：未自动修改
- 优化前后连续抽象段落数量：17 → 待人工或正文模型修订
- 一句话复述结果：需 AI QA 判断
- 是否达到 PASS：否，进入 REVISE/BLOCK 候选

### 测试二｜机制完整但认知过载正文

文件：`reports/production_20260728_cognition_judgment_article.txt`

- RR 检测结果：高风险
- 主要疲劳点：连续 19 段无人物、动作、场景或具体对象；一句话一段比例 0.94
- 应删内容：连续抽象判断
- 应转场景内容：认知判断后的现实观察和具体对象
- 应保留核心判断：原文主判断
- 优化前后字数：未自动修改
- 优化前后核心判断数量：未自动修改
- 优化前后连续抽象段落数量：19 → 待人工或正文模型修订
- 一句话复述结果：需 AI QA 判断
- 是否达到 PASS：否，进入 REVISE/BLOCK 候选

### 测试三｜当前“所有人支持错误决策”

文件：`reports/production_20260729_decision_flaw_everyone_supports_article.txt`

- RR 检测结果：高风险
- 主要疲劳点：连续 5 段无人物、动作、场景或具体对象；存在抽象名词密集区；一句话一段比例 0.87
- 应删内容：重复解释责任、成本、共识的段落
- 应转场景内容：表达成本、权力固化共识、失败责任下移三处机制
- 应保留核心判断：所有人支持不一定代表所有人认为它正确，很多时候只是反对成本高于支持成本
- 优化前后字数：未自动修改
- 优化前后核心判断数量：未自动修改
- 优化前后连续抽象段落数量：5 → 待正文模型修订
- 一句话复述结果：通过候选，需 AI QA 最终判断
- 是否达到 PASS：否，进入 REVISE

## 未修改项确认

- 未修改 Production Card 字段结构。
- 未新增日常生产字段。
- 未新增生产步骤。
- 未修改 Skill001-Skill007 调用顺序。
- 未修改 PD 推导深度参数。
- 未修改 CR 认知奖励参数。
- 未修改选题、结构路由、证据冻结逻辑。
- 未把 RR 拆成新的一级系统。
- 未重构知乎 OS。
- 未新增数据库。
- 未批量修改历史 Production Card。
- 未自动修改历史正文。

## 潜在冲突说明

- RR 模块数量从 6 个扩展到 8 个后，总质量参数审计口径从 24 维调整为 26 维；相关入口文件已同步。
- 历史 Production Card 中引用 RR-02、RR-03、RR-04、RR-06 仍兼容，不物理删除旧定义。
- 新脚本输出高风险不等于自动 FAIL；语义类判断仍由 Skill007 QA 完成。

## 验收命令

```bash
python3 scripts/validate_runtime_consistency.py
python3 scripts/validate_production_card.py reports/production_20260729_decision_flaw_everyone_supports_card.txt
python3 scripts/validate_reading_experience.py reports/production_20260729_decision_flaw_everyone_supports_article.txt
python3 scripts/validate_reading_experience.py reports/production_20260728_partner_split_article.txt
python3 scripts/validate_reading_experience.py reports/production_20260728_cognition_judgment_article.txt
```

结果：

- runtime 一致性：Pass
- 当前 Production Card：Pass
- 三篇正文 RR 检测：均识别出阅读疲劳风险，符合脚本辅助检测预期
