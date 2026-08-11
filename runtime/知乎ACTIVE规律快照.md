# 知乎ACTIVE规律快照

版本：RULE-V3.0-TEACHER

执行版本：ZH-RUNTIME-V3.0-TEACHER

状态：ACTIVE（快照文件有效；条目按各自执行权限调用）

来源：由 Git 权威文件和治理确认结果发布到 runtime。第二阶段起，ACTIVE规律优先来自“平台变量证据卡 → 账号实验验证 → 证据等级确认”的链路；Notion 仅可作为历史参考，不具备 Production Authority。

## Authority Provenance Patch｜2026-08-11

本文件中来源口径为“存量ACTIVE，待平台样本统计复核”的规律，当前不得再视为
Production Contract。

统一执行权限：

```text
状态：LEGACY_REVIEW
Execution Authority：ADVISORY_ONLY
```

含义：

- 可作为复盘观察标签、风险提醒或候选假设。
- 不得写入 Execution IR.required_steps / step_obligations。
- 不得写入 Execution IR.acceptance_criteria。
- 不得推荐结构并触发结构合同化。
- 不得作为 AUDIT 判定 Execution Compliance 失败的依据。
- 只有补齐“平台变量证据卡 → 账号实验验证 → 证据等级确认”链路后，才允许重新升级为 ACTIVE。

## 生产回流规则

本快照是复盘反哺生产的唯一入口。

生产链只允许读取本快照中执行权限允许的规律。内容变量只允许读取
`production_variable_library.md`。不得直接读取 L1 平台样本、变量证据卡、L2 正文变量矩阵、05 单篇复盘库或 05.5 规律验证库作为变量权威。

V3 起，ACTIVE 规律只作为结构实例化后的内容补充与风险提醒，不得替代 `runtime/知乎结构库快照.md` 中的 ACTIVE 老师结构，不得生成正文骨架。

## 规律来源口径

ACTIVE规律必须来自统计规律，不来自单篇心得。

允许来源：

```text
知乎平台高表现回答共同变量统计
↓
同题低表现回答反向分析
↓
变量证据卡
↓
写入 production_variable_library.md 同一变量记录
↓
本账号 10 篇实验验证
↓
ACTIVE 升级
```

存量本账号历史文章只负责验证，不负责直接发现规律。

规律记录必须包含：

```text
规律：
适用题型：
平台样本数：
平台命中率：
账号验证样本数：
账号成功率：
失败反证：
状态：ACTIVE / EXPERIMENT / LEGACY_REVIEW / DEPRECATED
Execution Authority：VERIFIED_CONTRACT / ADVISORY_ONLY / EXPERIMENT_ONLY
Execution IR调用方式：
```

调用时机：

```text
题型识别
↓
内容路由
↓
ACTIVE 规律回流调用
↓
COMPILE → Execution IR
```

输入：

```text
题型：
场景：
用户意图：
历史资产检索摘要：
```

输出：

```text
推荐主变量：
推荐辅助变量：
推荐结构：
禁用变量：
命中 ACTIVE 规律：
未命中原因：
```

写入规则：

- 推荐主变量只能作为 COMPILE 的变量匹配依据；只有执行权限为 `VERIFIED_CONTRACT`
  的规律，才允许写入 `Execution IR.acceptance_criteria` 的本 Run Realization Requirement。
- 推荐辅助变量最多三个，只能作为 COMPILE 的变量匹配依据；只有执行权限为
  `VERIFIED_CONTRACT` 的规律，才允许写入 `Execution IR.acceptance_criteria` 的本 Run Realization Requirement。
- 推荐结构必须与结构库校验一致；只有结构本身具备 `Contract Authority：VERIFIED_CONTRACT`
  时，才允许写入 `Execution IR.Structure` 的合同义务。
- 禁用变量不得写入 `Execution IR.acceptance_criteria` 或任何正文义务。
- 命中规律只能作为变量证据或调用理由压缩呈现，不得输出验证流水账。

未命中时，不阻塞 COMPILE；标注 `ACTIVE 规律未命中`，继续按结构库、`production_variable_library.md`、质量参数库和历史资产检索执行。

## 通用传播规律

### 开头钩子

状态：LEGACY_REVIEW

Execution Authority：ADVISORY_ONLY

来源口径：存量ACTIVE，待平台样本统计复核

规则：开头 3 秒内给出观点、冲突或反常识判断，不用背景铺垫起手。

### 情绪入口

状态：LEGACY_REVIEW

Execution Authority：ADVISORY_ONLY

来源口径：存量ACTIVE，待平台样本统计复核

规则：职场和组织题优先接住委屈、困惑、不服、释然或看清后的安全感。

### 认知增量

状态：LEGACY_REVIEW

Execution Authority：ADVISORY_ONLY

来源口径：存量ACTIVE，待平台样本统计复核

规则：正文必须给出一个新的解释框架，不能只复述“领导坏、员工难、环境差”。

### 结构节奏

状态：LEGACY_REVIEW

Execution Authority：ADVISORY_ONLY

来源口径：存量ACTIVE，待平台样本统计复核

规则：短段落推进，场景和机制交替出现，避免连续抽象段落。

### 观点锋利度

状态：LEGACY_REVIEW

Execution Authority：ADVISORY_ONLY

来源口径：存量ACTIVE，待平台样本统计复核

规则：要有明确立场，但不能靠极端化、绝对化和道德审判制造锋利。

### 收藏价值

状态：LEGACY_REVIEW

Execution Authority：ADVISORY_ONLY

来源口径：存量ACTIVE，待平台样本统计复核

规则：至少形成一句可迁移判断，帮助读者以后判断相邻问题。

## 职场组织题规律

### 组织机制优先

状态：LEGACY_REVIEW

Execution Authority：ADVISORY_ONLY

来源口径：存量ACTIVE，待平台样本统计复核

规则：把个人行为放回权责、流程、评价、授权、资源和风险分配中解释。

### 责任转移优先

状态：LEGACY_REVIEW

Execution Authority：ADVISORY_ONLY

来源口径：存量ACTIVE，待平台样本统计复核

规则：涉及领导、下属、汇报、甩锅、背责时，优先判断谁在承担风险，谁在保留选择权。

### 反道德化

状态：LEGACY_REVIEW

Execution Authority：ADVISORY_ONLY

来源口径：存量ACTIVE，待平台样本统计复核

规则：不把组织问题写成单个坏人问题，优先解释机制如何制造行为。
