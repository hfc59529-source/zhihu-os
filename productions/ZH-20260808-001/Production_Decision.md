Production ID: ZH-20260808-001

# Production Decision

## Status

CREATED_FROM_USER_MANUAL_TOPIC

## Topic Binding

- Topic Package: `data/topic_candidates/2026-08-08/TOPIC-20260808-001.md`
- Question: 公司实行「上四休三」，但要降薪1000元，员工不接受只能辞职，这样合理吗？换做是你会如何选择？
- Source: 用户提供的知乎创作中心截图
- Created At: 2026-08-08

## Attribution Boundary

This Production ID starts at the user manual topic selection step. All later Production Card, Draft, QA, Release, publish result, and revenue recovery artifacts must reference `ZH-20260808-001`.

## Current Gate

Topic Package exists, but `Answer_Benchmark_Top3` is not collected yet. Do not generate Production Card or draft until the question URL and default sorted top three answers are captured.

## Protocol Note

The topic is an open decision question. TOPIC-COLLECTOR-V1.1 normally rejects open decision questions by default. This run is allowed only because the user explicitly selected it as a new attribution-chain sample. The override must remain visible in downstream artifacts.
