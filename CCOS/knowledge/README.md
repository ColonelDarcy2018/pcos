---
CCOS-Index:
  id: ccos-knowledge-overview
  domain: knowledge
  tags: [ccos, overview]
  related:
    - ../protocol/p0-rules.md
    - ../protocol/ai-playbook.md
  created: 2026-03-03
  updated: 2026-03-03
---

# 知识库总览

## 目录用途

本目录存放项目的结构化知识资产，包括业务逻辑、架构设计、决策记录和可复用模式。

## 一级目录

- `business-logic/`：业务流程、隐性规则、执行链路
- `architecture/`：系统架构、方案设计、演进路线
- `decisions/`：关键决策记录（ADR）
- `patterns/`：可复用工程模式与模板
- `rpa/`：RPA 案例与资产规范

## 当前重点文档

- 架构方案：`architecture/ccos-governance-dedup-and-daily-automation-v1.md`
- 架构方案：`architecture/remote-codex-control-mvp.md`
- 关键决策：`decisions/adr-20260303-cloud-control-plane.md`
- 接入决策：`decisions/adr-20260303-no-public-ip-access.md`

## 维护约束

- 参考 `CCOS/protocol/p0-rules.md`
- 知识文档改动后执行 `python3 CCOS/scripts/ccos_p0.py sync`
