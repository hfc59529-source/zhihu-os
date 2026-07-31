# 正式生产自动继续回归测试

时间：2026-07-28 19:50:41 EAT

## 测试目标

验证知乎系统收到问题、截图选题或“写文案”指令后，不停在候选题、Production Card 或 QA 阶段，而是按正式生产模式自动调用 Claude 正文生产节点，并由 GPT 检查后交付通过 QA 的正文。

## 测试 1：单个文字问题

输入类型：单个知乎文字问题。

问题：老板十分敬业，大事小情事无巨细都亲力亲为，这样的老板可以追随吗？

结果：

- 正确读取 ACTIVE_MANIFEST：PASS
- 成功选择问题：PASS
- 成功命中 ACTIVE 结构：PASS，职场组织型回答结构
- 成功生成 Production Card：PASS
- Production Card 校验：PASS
- 成功调用 Claude 正文生产节点：PASS
- 推理校验：PASS
- QA：PASS
- 最终直接交付通过 QA 的 Claude 正文：PASS
- 中间没有等待人工确认：PASS

## 测试 2：截图中包含多个问题

输入类型：截图候选题列表中的多问题场景。

选中问题：57 岁处级干部每天 11 点“消失”，全科室视而不见，背后反映了哪些问题？

结果：

- 正确读取 ACTIVE_MANIFEST：PASS
- 成功选择问题：PASS
- 成功命中 ACTIVE 结构：PASS，职场组织型回答结构
- 成功生成 Production Card：PASS
- Production Card 校验：PASS
- 成功调用 Claude 正文生产节点：PASS
- 推理校验：PASS
- QA：PASS
- 最终直接交付通过 QA 的 Claude 正文：PASS
- 中间没有等待人工确认：PASS

## 测试 3：“写文案”并附一个问题

输入类型：明确生产指令。

指令：写文案：领导逼你主动辞职怎么办？

结果：

- 正确读取 ACTIVE_MANIFEST：PASS
- 成功选择问题：PASS
- 成功命中 ACTIVE 结构：PASS，职场组织型回答结构
- 成功生成 Production Card：PASS
- Production Card 校验：PASS
- 成功调用 Claude 正文生产节点：PASS
- 推理校验：PASS
- QA：PASS
- 最终直接交付通过 QA 的 Claude 正文：PASS
- 中间没有等待人工确认：PASS

## 校验命令结果

- `python3 scripts/validate_runtime_consistency.py`：PASS
- `python3 scripts/validate_production_card.py reports/regression_autocontinue_test1_card.txt`：PASS
- `python3 scripts/validate_production_card.py reports/regression_autocontinue_test2_card.txt`：PASS
- `python3 scripts/validate_production_card.py reports/regression_autocontinue_test3_card.txt`：PASS
- `python3 scripts/validate_reasoning.py reports/regression_autocontinue_test1_article.txt`：PASS
- `python3 scripts/validate_reasoning.py reports/regression_autocontinue_test2_article.txt`：PASS
- `python3 scripts/validate_reasoning.py reports/regression_autocontinue_test3_article.txt`：PASS

## 结论

当前协议已支持：用户发送知乎问题或截图并要求写文案后，系统自动进入正式生产模式，Production Card 校验通过后不再等待人工确认，继续调用 Claude 正文生产节点、执行推理校验和 Skill007 QA，并由 GPT 直接交付通过 QA 的 Claude 正文。
