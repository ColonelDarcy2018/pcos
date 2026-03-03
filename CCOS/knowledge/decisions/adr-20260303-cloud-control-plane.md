---
CCOS-Index:
  id: adr-remote-control-cloud-control-plane-20260303
  domain: decisions
  tags: [adr, remote-control, codex, architecture]
  related:
    - ../../protocol/p0-rules.md
    - ../architecture/remote-codex-control-mvp.md
  created: 2026-03-03
  updated: 2026-03-03
---

# ADR-20260303：远程控制架构选型

## 状态

`accepted`

## 背景

目标是让手机在异地网络下可远程监督和控制 PC 上 Codex 任务。候选架构：

1. 手机直连 PC（公网暴露端口或打洞）
2. 云中转控制平面 + PC Agent 主动外连
3. 纯远程桌面方案（向日葵/ToDesk 类）

## 决策

采用“云中转控制平面 + PC Agent 主动外连”作为 MVP 基线。

## 决策理由

1. 跨网络稳定性更高，避免家庭宽带 NAT 和动态 IP 难题。
2. 安全边界更清晰，可集中做鉴权、审计和命令白名单。
3. 与“任务级控制”目标匹配，复杂度低于全远控桌面。
4. 后续可平滑扩展小程序与多端协同。

## 权衡

### 优点

1. 可靠性和可维护性高。
2. 便于标准化 API 与协议，支持多客户端。
3. 易于观察和审计。

### 缺点

1. 增加后端部署与运维成本。
2. 引入额外跳点，时延略高于直连。

## 不采用方案

1. 手机直连 PC：NAT/防火墙/安全暴露风险高，不利于通用化。
2. 纯远程桌面：实现快但不可编排，无法稳定结构化管理任务和审计。

## 后续影响

1. 必须实现 Agent 注册、心跳、重连与版本治理。
2. 必须实现命令幂等和审计事件模型。
3. 小程序阶段可复用同一控制后端，无需重做协议。
