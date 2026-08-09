# Input Rules V1

Status：DESIGN_FROZEN（尚未进入 Runtime Release，不具备执行权威；执行权威只来自已发布的 Runtime Manifest，见 `runtime/ACTIVE_MANIFEST.md`）

本文件是七节点流水线 INPUT 节点的唯一 Rules 来源，定义见 `docs/知乎OS Compiler V1.md` 第3节。本文件只回答一个问题：**进入一个 Run 之后，什么构成合法的 Input Package。**

## 1. 不在本文件范围内的东西

选题发现、候选题排序、值不值得回答、推荐级别、`Daily_Topic_Top3`、参数命中、参数缺口发现、`Possible_Current_Gap`——这些属于 Run 开始之前的 Pre-Run 系统（选题采集与筛选），继续由 `docs/Codex选题采集协议.md`、`templates/选题包模板.md` 承载，不进入这次 Runtime 的 Partitions，不受本文件约束。一个题目一旦被 Pre-Run 系统选定、以 Run 的形式进入 INPUT，本文件才开始生效。

`skills/Skill000_历史资产检索器.md` 与 `scripts/search_historical_assets.py` 的完整能力（推荐结构、推荐变量、共同机制、是否建议进入 Production Card）同样不进入本文件——那是面向已退役的 Production Card 的生产前建议工具，属于 COMPILE 侧能力，不是 INPUT 的重复检查。本文件只复用其中 `tokenize()` / `similarity()` 两个函数承担的标题相似度计算能力，见第3节。

## 2. Source Facts 完整性判定

`Input Package.source_facts` 视为完整，当且仅当以下字段均非空：

```text
question              原问题标题
question_url          真实问题链接
question_description  问题描述（若原问题无描述，记录"无额外描述；题目本身即为核心问题"）
necessary_background  必要背景事实（可为空数组，但字段必须存在）
platform_signals      至少包含来源渠道（如 P0/P1/P2/P3/P4 或用户手动提供）
```

缺少 `question_url` 或 `question` 时，INPUT 不得产出 Input Package，只能回复选题包需要退回补充事实。

## 3. Benchmark Context 采集判定

`benchmark_context.answers` 采集同题当前默认排序前三条有效高赞回答，每条记录：

```text
rank / author / summary / url
```

`summary` 只允许是对该回答论点的客观摘要，不得混入 INPUT 自己的判断、结论或推荐。摘要内容属于 Benchmark Context，不是 Source Facts——第4条禁止事项的隔离要求同样适用于此处产出环节，不只适用于下游消费环节。

采集不足三条有效回答时，如实记录实际采集数量，不得编造。

## 4. 重复检查（duplicate_check）

判定方法：

```text
1. 对 question 做 tokenize()（2/3/4-gram 切分 + 中文单字过滤停用词，
   复用 scripts/search_historical_assets.py 的 tokenize 函数定义）
2. 与 data/l0_content_assets.csv 中历史标题逐条计算 similarity()
   （复用同文件的 similarity 函数定义：n-gram 重叠占比 + 领域关键词命中加权）
3. 取相似度最高的历史记录作为候选匹配
```

这一步只产出**排序后的候选匹配**，不产出机械判定的布尔值——现有实现里 `similarity()` 没有固定阈值，达到多高的相似度算"重复"始终需要判断，不是查表。因此：

```text
duplicate_check.is_duplicate  = INPUT 判断，需要人工/Claude 对照候选匹配的
                                  标题和核心矛盾做最终判断，不是分数自动决定
duplicate_check.matched_history_id = 候选匹配对应的历史记录 ID（如有）
```

这个判断权属于 INPUT（对应 Compiler V1 §3 Decision Right"判断是否与历史选题重复"），不是脱离 INPUT 的另一个节点或工具的裁量——工具只提供候选排序，不替 INPUT 下结论。

## 5. Forbidden（与 Compiler V1 §3 一致，此处不重复展开）

不得判断"这题该不该答""这题该怎么答"；不得写入任何已经带解释性质的字段；不得把 Benchmark Context 中的观点当作 Source Facts。
