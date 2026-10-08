# Gate接口修复：工程验证与受控升级

对象：既有Observation `GATE-REFERENCE-INTERFACE-20261009`，不是EXP008的新阶段或新实验。

## 审计

当前hook `.githooks/pre-commit` 从HEAD导出 `scripts/learning_loop.py` 到临时目录，调用 `check_promotion(root, staged=True)`。旧函数只读取 `promotion_approvals`，对受保护文件要求正式验证与批准；完全不读取reference_change_approvals。真实工作区旧检查器模拟拒绝了选题协议与检查器自身。

## 权限边界

Rule Promotion保持原校验：源对象Validation及反例检查PASSED、人工限定批准、文件/diff/证据hash；EXP008机制继续冻结。

Production Reference仅接受人工接受、范围明确的DATA_FINDING，不接受Candidate Mechanism，不凭标签成为VALIDATED_RULE。参考授权仅绑定选题协议及现有生产参考清单；禁止修改Compiler、Prompt、ACTIVE、runtime或门禁代码本身。生产参考载体加入保护范围，防止只编辑清单绕过校验。未知仍为未知，不设置分数或固定权重。

检查器自身的工程修复使用既有Observation及promotion_approvals承载工程验证和本轮用户明确条件性授权，引用本报告、测试和人工授权记录；它不是Production Reference许可，绝不声称EXP008 Validation通过。

## 工程Validation

实际运行 `python3 scripts/test_learning_loop.py`，24项通过。覆盖原测量/Rule Promotion、参考资格需人工接受、Candidate不可包装为Data Finding、参考权限禁止Prompt/ACTIVE/Compiler/检查器、无因果验证的合法具体接口变更通过、扩大修改拒绝、未暂存批准无效、反例及证据hash变更拒绝。

工程结果：PASSED。Counterexample Check：PASSED，含非法权限与伪装升级的拒绝案例。结果只证明接口实现满足这些合同与测试，不能证明知乎机制、身份真实性或抵抗所有人为篡改。

## 授权与两次受控提交

本轮用户直接要求完成受控提交，明确“只有Gate真正允许本次合法变更通过后才能提交”，禁止绕过hook或伪造研究Validation。本授权在工程检查通过后生效；approved_at记录条件满足并登记的时间，不冒称发生了额外逐行人工审阅。

第一批仅提交检查器、直接相关测试、既有Observation/metadata及授权证据。旧HEAD检查器必须通过此批，实际hook保持开启。

第二批提交已经实现的选题参考修复、文档与metadata的业务变更hash。第一批提交后的HEAD检查器必须识别其参考授权并实际允许hook通过。不能关闭hook、修改hooksPath或使用--no-verify。

Runtime drift只保留报告，不重算hash、不release。后续最终结果记录见修复报告。
