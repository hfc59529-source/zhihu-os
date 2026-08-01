# Card Audit Report

Production ID: ZH-20260801-011
Audit Object: Card-v1.md
Audit Type: Question-fit / Zhihu-answer-fit
Status: CARD_REWORK_REQUIRED

## Original Question

你们知道为什么好多公司推行绩效考核失败吗？

Question Link:
https://www.zhihu.com/question/1907358768624280756

## Conclusion

Card-v1.md is internally coherent, but it over-specifies a complete management framework. The resulting article faithfully follows the Card, yet answers closer to "what good performance management requires" than the sharper Zhihu question "why performance appraisal fails."

This is a Card-level issue, not a Claude Patch issue.

## Evidence

### Issue-01: The Card Converts A Causal Question Into A Management Framework

Location:
Card-v1.md lines 25-35

Evidence:
- "绩效考核失败，通常不是因为表格不够复杂，而是组织没有把目标、权责、反馈和利益分配真正接起来。"
- "能用四个断裂检查一套绩效制度：目标是否真实、权责是否匹配、反馈是否及时、分配是否兑现。"

Problem:
The original question asks why many companies fail when implementing performance appraisal. The Card turns this into a four-part diagnostic framework. That makes the article aim for full coverage instead of staying on one conflict.

Risk:
The writer will try to cover every dimension completely, producing a management explainer rather than a high-tension Zhihu answer.

### Issue-02: The Continuation Hook Forces Four-Part Coverage

Location:
Card-v1.md lines 62-63

Evidence:
"后文拆四个失败原因：目标断裂、权责断裂、反馈断裂、分配断裂；最后给员工和管理者各自的判断。"

Problem:
This tells the writer to proceed by enumeration. Even if explicit numbering is later removed, the underlying reading experience remains list-like.

Risk:
The opening conflict is diluted after the first screen. The article becomes "four reasons explained" instead of repeatedly proving the central reversal.

### Issue-03: Segment Instructions Reward Completeness Over Reading Tension

Location:
Card-v1.md lines 82-151

Evidence:
The Card requires separate construction for:
- 目标断裂
- 权责断裂
- 反馈断裂
- 分配断裂
- 员工和管理者迁移判断
- 结尾判断

Problem:
Each segment is framed as a required module with its own content, scene, and progression. This encourages the writer to complete every module rather than compress around the strongest causal chain.

Risk:
The article becomes correct but instructional. It lacks repeated "you thought X, actually Y" turns that match Zhihu reading behavior.

### Issue-04: The Core Conflict Is Strong But Not Made Into The Article Engine

Location:
Card-v1.md lines 43-44 and 59-60

Evidence:
- "绩效考核失败，不是因为公司不会打分，而是因为公司想用一张表，替代目标澄清、过程反馈、责任分配和利益兑现。"
- "绩效不是一张表，绩效是组织平时怎么定义价值、分配责任和兑现利益。"

Problem:
The central conflict is good. But the later Card fields convert it into categories to explain, instead of requiring every section to keep proving "companies use performance appraisal to replace management."

Risk:
The best sentence appears early, then the article loses conflict and turns into a lesson.

### Issue-05: Expression Constraint Prevents The Writer From Correcting A Bad Card Shape

Location:
Card-v1.md lines 159-162

Evidence:
"只执行本卡，不重新选择题型、结构、变量、证据、核心判断或段落顺序"

Problem:
Once the Card has over-specified the four-part structure, Claude is not allowed to collapse it into a sharper Zhihu answer.

Risk:
The execution model can only be loyal to a flawed Card. Patching the article will not solve the root cause.

## Decision

Current Draft / Article-Patched should not proceed to Patch Validation or User Review.

Next state:
CARD_REWORK_REQUIRED

## Required Next Action

Codex should regenerate the Production Card around one dominant conflict:

"很多公司不是不会做绩效，而是想用绩效代替管理。"

The new Card should:

- Keep the original question and link.
- Preserve the causal answer to "why it fails."
- Avoid requiring complete coverage of target, authority, feedback, and distribution as four equal modules.
- Use the four dimensions only as evidence serving one conflict, not as the article skeleton.
- Require repeated cognition turns: "你以为 X，其实 Y."

## Boundary

This report does not modify Draft-v1.md, Article-Patched-v1.md, or Card-v1.md.

Claude should not Patch the current article until a new Card is produced and validated.
