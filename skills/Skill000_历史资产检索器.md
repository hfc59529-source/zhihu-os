# Skill000｜历史资产检索器 V1.0

Status：ACTIVE

## 目标

在 COMPILE 生成 Execution IR 之前，先从 `04｜内容资产库` 对应的本地 L0 总账中检索相似历史样本，输出可供 COMPILE 使用的历史证据摘要。

本技能只负责历史资产检索，不负责正文创作，不负责复盘，不负责升级 ACTIVE。

## 输入

固定输入：

```text
知乎问题标题
```

可选输入：

```text
用户补充的题型、关键词、目标平台
```

## 固定数据源

只读取：

```text
data/l0_content_assets.csv
```

不得读取历史实验、旧协议、TEST、Candidate 或历史 Prompt 来生成生产结论。

## 执行方式

在仓库根目录运行：

```bash
python3 scripts/search_historical_assets.py "知乎问题标题"
```

如需保存结果：

```bash
python3 scripts/search_historical_assets.py "知乎问题标题" --output reports/historical_asset_match_YYYYMMDD_slug.md
```

## 输出格式

必须输出：

```text
==========历史资产命中==========
输入问题：
检索范围：
历史命中：

最相似：
-

最高收益：
-

最高千阅读：
-

最低收益：
-

推荐结构：
-

推荐变量：
-

共同机制：
-

历史风险：
-

是否建议进入COMPILE：YES/NO
使用边界：
```

## 证据解释规则

1. `最相似` 主要基于标题文本相似度，覆盖全量 L0。
2. `最高收益` 只基于已补齐 `earnings` 的样本。
3. `最高千阅读` 只基于已补齐 `earnings_per_1k_views` 的样本。
4. `推荐结构`、`推荐变量`、`共同机制` 只统计非空且非 `UNKNOWN` 字段。
5. 如果标签字段仍为 `UNKNOWN`，必须明确提示“历史标签证据不足”，不得伪造变量或结构。
6. C层样本代表“高阅读低收益”风险，必须在历史风险中提示。

## 接入 COMPILE 的规则

COMPILE 生成 Execution IR 前，可以读取 Skill000 输出，并把可用结论压缩进：

- Decision 旁证
- 变量证据
- Structure 匹配依据
- Material Boundary
- Acceptance Criteria 候选义务

不得把 Skill000 原始检索日志、完整数据库字段、相似度细节交给 Claude。

Execution IR 中只允许引用被压缩后的结论，例如：

```text
变量证据：
本 Run Realization Requirement：
来源：ACTIVE变量库 + 历史资产命中样本
调用理由：历史相似样本中反复出现组织信任/风险责任相关机制
证据等级：HISTORICAL_RAW + ACTIVE
```

## 边界

- 历史资产是生产前证据增强，不是生产权威。
- runtime ACTIVE 快照仍是正式生产权威。
- 历史样本不得直接升级 ACTIVE。
- 历史样本只能生成候选规律，进入05.5验证后再决定是否升级 ACTIVE。
- 当历史命中不足、收益覆盖不足或字段为 `UNKNOWN` 时，必须降级为弱参考。
- Skill000 输出为 `NO` 时，不阻止 COMPILE 继续生成 Execution IR，但必须在 Material Boundary 或结构匹配依据中标注“历史证据不足”。
