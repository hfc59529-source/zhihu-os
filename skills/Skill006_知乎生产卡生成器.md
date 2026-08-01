# Skill006｜知乎生产卡生成器 V2.0

Status：ACTIVE

执行版本：ZH-RUNTIME-V3.0-TEACHER

## 目标

将已经完成的 L1 结构实例装配成 Claude 可直接执行的正文施工卡。

Codex 不负责正文创作。

Codex 不负责重新设计正文结构。

Claude 不负责读取 Notion、runtime 或后台参数。

## Codex 职责

Codex 只做三件事：

1. 读取。
2. 压缩。
3. 校验。

日常正式生产模式下，Codex 只交付可复制 Production Card。只有用户明确要求“生产正文”“写回答”“调用正文节点”“按完整链路生产”时，才在 Production Card 校验通过后继续调用正文生产节点。

## 固定读取

1. `docs/08_总AI执行中心.md`
2. `docs/知乎OS执行协议.md`
3. `templates/知乎OS总控提示词.md`
4. `runtime/ACTIVE_MANIFEST.md`
5. `runtime/知乎结构库快照.md`
6. `runtime/知乎ACTIVE规律快照.md`
7. `production_variable_library.md`
8. `runtime/production_variable_snapshot.md`
9. `runtime/知乎内容质量参数快照.md`
10. `runtime/知乎账号画像快照.md`
11. `templates/Production Card模板.md`
12. `Skill000｜历史资产检索器`输出

## 准入规则

只要以下系统参数读取成功，即可进入 Claude 版 Production Card 生成：

1. 当前选题可完整识别。
2. 已执行历史资产检索；命中不足时必须标注“历史证据不足”，但不得单独阻止 Production Card。
3. `runtime/知乎结构库快照.md` 中存在可调用 ACTIVE 老师结构。
4. 已选择唯一 ACTIVE 结构。
5. 已读取该结构完整推进字段。
6. 已完成本题结构实例化。
7. 已生成本题因果追问链和推导终点。
8. 已为每段写出具体内容、现实场景或例子、推进关系。
9. 已生成或刷新 `runtime/production_variable_snapshot.md`；变量只作为内容材料，不作为正文骨架。
10. 已校验变量快照满足六层筛选顺序和标准字段。
11. 后台质量参数检查已完成。

## 结构权威规则

Production Card 的正文骨架只能来自 `runtime/知乎结构库快照.md` 中状态为 ACTIVE 的结构。

禁止：

- 根据主变量和辅助变量现场设计正文段式。
- 使用 STRUCT-V2.1 等抽象通用结构临场拼装七段。
- 由 Skill006 重新进行结构设计。
- 只写“反转、机制、承接、升华、收藏价值”等抽象标签。

Skill006 只能把已完成的结构实例装配进模板。

## 后台参数规则

后台可继续读取：

- PD
- RR
- RE
- BT
- CR
- 内容变量

这些只用于检查、补充和风险限制，不得决定正文骨架，不得在交给 Claude 的施工卡中展开 26 维审计。

质量参数检查必须与 Claude 施工卡分开输出。

## 输出

日常输出必须同时包含：

1. 题目识别。
2. ACTIVE 结构调用。
3. 本题结构实例化摘要。
4. 历史资产命中摘要。
5. 后台变量材料摘要。
6. 后台参数检查摘要。
7. 可复制 Claude版 Production Card。
8. Production Card 校验结果。

输出文件必须严格按照 `templates/Production Card模板.md`。

输出给 Claude 时必须使用固定接口：

```text
===Production Card Begin===
...
===Production Card End===
```

只有 Begin 和 End 中间的内容属于 Claude 输入。

后台审计报告不得放入 Begin / End 之间。

## 自动填充规则

### 1. ACTIVE 结构实例化

输入：

```text
问题：
题型：
读者真实困惑：
读者原始理解：
历史资产检索摘要：
后台变量材料：
```

输出：

```text
ACTIVE结构名称：
ACTIVE结构ID：
结构版本：
开头具体困惑或反差：
核心反转句：
续读动力：
因果追问链：
因果追问终点：
核心判断位置：
结尾回收方式：
分段施工说明：
```

每个段落节点必须包含：

```text
段落目标：
具体内容：
现实场景或例子：
推进关系：
```

### 2. 内容变量材料

内容变量只允许作为：

- 具体内容补充
- 风险边界补充
- 结尾判断补充
- 后台审计依据

内容变量不得作为：

- 正文结构
- 段落顺序
- 一级标题
- Claude 施工卡中的显性后台术语

变量快照必须按以下顺序完成筛选：

```text
生产权限
↓
禁用边界
↓
适用题型
↓
触发条件
↓
去重 / 冲突
↓
权重
```

每条推荐变量必须记录：

```text
变量编码：
生产权限：
适用题型检查：
触发条件检查：
禁用边界检查：
去重 / 冲突检查：
调用权重：
命中依据：
本题用途：
是否实际调用：
未调用理由：
```

`ACTIVE` 只代表变量具备生产调用资格，不代表本题默认必用。推荐变量和实际调用变量必须分开；实际调用只能保留完成本题推导所需的最少集合。

### 3. 后台质量参数检查

后台质量参数检查只输出摘要，不展开 26 维清单。

最低检查：

- 是否有具体场景或例子。
- 是否有因果追问链。
- 是否有推导终点。
- 是否避免后台术语。
- 是否避免无来源数字。
- 是否避免投资承诺、荐股、荐币、理财配置方案。

## 失败条件

出现以下任一情况，必须停止并返回错误码：

- FAIL-STRUCTURE-NOT-ACTIVE：未引用结构库中的 ACTIVE 结构。
- FAIL-STRUCTURE-INVENTED：正文段式不是结构库原始步骤的本题实例，而是临场创造。
- FAIL-CARD-ABSTRACT：任一段只有抽象标签，没有具体内容。
- FAIL-CARD-NO-SCENE：需要现实承接的段落没有具体场景或例子。
- FAIL-CARD-NO-CAUSAL-CHAIN：卡片没有明确因果追问链和推导终点。
- FAIL-RUNTIME-VERSION-MISMATCH：MASTER、执行协议、总控 Prompt、结构库、Skill006 和模板版本不一致。
