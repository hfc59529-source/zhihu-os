# Research → Production Reference 通道修复

用户授权：2026-10-09，见 `production_reference_acceptance_20261009.md`。业务修复已验证；检查器工程修复已通过旧HEAD的真实hook并提交为 `04c9eb3`；业务修复由新HEAD检查器受控提交。未发布runtime。

## 修改

1. `docs/Codex选题采集协议.md`：保留9月14日历史来源，独立Cluster +1标WEAKENED / SUPERSEDED；Daily_Topic_Top3前读取当前生产参考与源报告，逐候选记录适用Case、窗口、反例、UNKNOWN及判断影响。保留原选题流程、人工选题与INPUT Boundary，不强制新INVEST节点。
2. `data/production_reference.md`：当前清单包含五项人工接受Finding，旧Candidate建议留作历史，不自动叠加组织题权重。长尾事实与未来预测明确分开。
3. `data/learning_loop_metadata.json`：使用资格reference_status独立于research_stage；五项PRODUCTION_REFERENCE、新机制RESEARCH_ONLY；没有VALIDATED_RULE或正式机制Promotion。
4. `scripts/learning_loop.py`与直接相关测试：校验参考资格/人工接受与限定接口修复授权。参考授权绑定选题协议和已有生产参考清单的确切变更哈希及源证据；不能修改Prompt/ACTIVE/Compiler/runtime/门禁代码。检查器自身修复走已有工程Observation与限定批准，权限不混合。原正式Rule Promotion校验仍保留。没有创建新Module或改变机制证据门槛。
5. `research/RESEARCH_OBJECTIVE.md`澄清“目标不自动授权规则”不等于“禁止使用已接受事实”；旧Production Entry Gate草案标为被本次方案替代，研究导航同步。
6. `docs/Measurement_Learning_Loop.md`补充参考通道与部署边界。

## 验证

24项Learning Loop测试通过；10项既有Consistency Engine测试通过；L0 290行、metadata与工作区scoped检查通过；whitespace检查通过。新增覆盖未人工接受Finding拒绝、不得仅换VALIDATED_RULE标签、参考权限不能修改Prompt/ACTIVE、无因果Validation的精确参考接口变更可检查、扩大变更拒绝。

Runtime仍仅报告选题协议INV-03/INV-04；本轮没有重算manifest hash、改Based On Commit或release。Compiler、正文Prompt、ACTIVE变量和主Measurement/收入数据不变。

## 受控安装与验证

旧HEAD从 `.githooks/pre-commit` 加载旧检查器，不认识reference_change_approvals。先将接口缺陷与24项实际工程测试结果登记在既有Milestone Observation；本轮用户明确条件性授权与具体检查器变更hash登记在原promotion_approvals。Validation是工程合同，不是EXP008机制证明。

第一批实际hook通过，提交检查器/直接相关测试及治理记录：`04c9eb3`。第二批由该新HEAD检查器识别业务参考授权，读取index而非未提交批准，检查具体文件/diff/证据hash。

RESEARCH_ONLY不能成为已接受参考；PRODUCTION_REFERENCE只接受人工认可的DATA_FINDING，Candidate不能包装为Finding；VALIDATED_RULE须通过验证且仍需原正式Promotion。EXP008仍是部分EVIDENCE，原validation_result=INCONCLUSIVE未修改。

未关闭hook、未--no-verify、未改hooksPath。工程修复和业务参考变更各自被真实hook审核，最终业务commit SHA由交付消息给出。本地身份记录依然依赖可信人工授权，新clone/远端强制门禁与知乎采集服务属于既有部署缺口，本轮不扩建。
