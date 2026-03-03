# CCOS Protocol

本目录存放 CCOS 协议层文档，是项目内 AI 与知识资产治理的执行入口。

## 文件说明

- `p0-rules.md`：P0 公共约束（规则权威源）。
- `ai-playbook.md`：AI 会话操作清单（执行流程）。
- `multi-ai-collaboration.md`：多 AI 协作防冲突协议（认领/锁/冲突处理）。

## 使用顺序

1. 先读 `p0-rules.md`，确认 MUST/SHOULD 约束。
2. 再读 `ai-playbook.md`，按会话生命周期执行。
3. 多 AI 并行时补读 `multi-ai-collaboration.md`。
4. 若涉及知识文档改动，执行 `python3 CCOS/scripts/ccos_p0.py sync`。
