Production ID: ZH-20260808-001

# Production Decision

## Status

PUBLISHED_MAPPED

## Topic Binding

- Topic Package: `data/topic_candidates/2026-08-08/TOPIC-20260808-001.md`
- Question: 公司实行「上四休三」，但要降薪1000元，员工不接受只能辞职，这样合理吗？换做是你会如何选择？
- Source: 用户提供的知乎创作中心截图
- Question URL: https://www.zhihu.com/question/2068750826869413005
- Created At: 2026-08-08

## Attribution Boundary

This Production ID starts at the user manual topic selection step. All later Production Card, Draft, QA, Release, publish result, and revenue recovery artifacts must reference `ZH-20260808-001`.

## Current Gate

Answer_Benchmark_Top3 collected. Per user correction on 2026-08-08, Production Card is LEGACY_RETIRED and not part of the ACTIVE daily pipeline (README.md: Question Package → Semantic Freeze Gate → Reasoning Path → Claude Writer → QA). Card step was skipped by design, not an oversight.

Draft went through Draft-v1 → Draft-v5 under Patch discipline (Assets/Issues separation each round). A Parameter Attribution Audit was run against `production_variable_library.md` before v4; CV002/CV004/CV005 realization had been lost during the v3 Explanation Target correction and was restored in v4, with CV004 rewritten to describe cost/exit-risk distribution mechanics only (no unsupported motive attribution).

GPT QA on Draft-v5 (after the CV004 evidence-strength patch): PASS. CV001–CV006 all confirmed realized in text, no parameter conflicts, no remaining reading-experience issues. Released as `Release-v1.md`.

Known open gap (not blocking): this Production has no entry in `data/parameter_call_log.md`; the claimed-parameters declaration step was skipped when the draft was first written and only reconstructed retroactively via audit. Flagged for later log entry, not for process fix today.

Published answer captured from Zhihu question page:

- article_id: answer_2069522411372933416
- answer_url: https://www.zhihu.com/answer/2069522411372933416
- mapping authority: `data/production_article_map.csv`

Next: wait for review-window data and earnings recovery.

Collected Answer_Benchmark_Top3:

1. 侃大山：https://www.zhihu.com/question/2068750826869413005/answer/2069008603386844846
2. 弗兰克扬：https://www.zhihu.com/question/2068750826869413005/answer/2068775650681434697
3. 职业导师小全：https://www.zhihu.com/question/2068750826869413005/answer/2069000873691423203

## Protocol Note

The topic is an open decision question. TOPIC-COLLECTOR-V1.1 normally rejects open decision questions by default. This run is allowed only because the user explicitly selected it as a new attribution-chain sample. The override must remain visible in downstream artifacts.
