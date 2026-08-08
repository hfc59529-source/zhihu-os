Production ID: ZH-20260808-001

# Production Decision

## Status

TOPIC_PACKAGE_READY_FOR_PRODUCTION_CARD

## Topic Binding

- Topic Package: `data/topic_candidates/2026-08-08/TOPIC-20260808-001.md`
- Question: 公司实行「上四休三」，但要降薪1000元，员工不接受只能辞职，这样合理吗？换做是你会如何选择？
- Source: 用户提供的知乎创作中心截图
- Question URL: https://www.zhihu.com/question/2068750826869413005
- Created At: 2026-08-08

## Attribution Boundary

This Production ID starts at the user manual topic selection step. All later Production Card, Draft, QA, Release, publish result, and revenue recovery artifacts must reference `ZH-20260808-001`.

## Current Gate

Topic Package exists and `Answer_Benchmark_Top3` has been collected from the question page default sort.

Production Card may be generated next. Do not skip directly to draft/body.

Collected Answer_Benchmark_Top3:

1. 侃大山：https://www.zhihu.com/question/2068750826869413005/answer/2069008603386844846
2. 弗兰克扬：https://www.zhihu.com/question/2068750826869413005/answer/2068775650681434697
3. 职业导师小全：https://www.zhihu.com/question/2068750826869413005/answer/2069000873691423203

## Protocol Note

The topic is an open decision question. TOPIC-COLLECTOR-V1.1 normally rejects open decision questions by default. This run is allowed only because the user explicitly selected it as a new attribution-chain sample. The override must remain visible in downstream artifacts.
