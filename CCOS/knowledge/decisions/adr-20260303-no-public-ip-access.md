---
CCOS-Index:
  id: adr-remote-control-no-public-ip-access-20260303
  domain: decisions
  tags: [adr, network, tailscale, remote-control]
  related:
    - ../../protocol/p0-rules.md
    - ../architecture/remote-codex-control-mvp.md
  created: 2026-03-03
  updated: 2026-03-03
---

# ADR-20260303：无公网 IP 下的外网接入策略

## 状态

`accepted`

## 背景

本地 PC 无公网 IP，需要支持手机在异网环境远程访问控制网关。候选方式：

1. 路由器端口映射 + 动态域名
2. Tailscale 私网组网
3. 云中转入口（本机主动外连）

## 决策

优先采用 `Tailscale` 作为接入方案；在需要小程序公网标准入口时，增加“云中转入口”作为扩展。

## 决策理由

1. 无需公网 IP，无需端口映射，落地快。
2. 连接模型符合“本机主动外连”，安全边界更可控。
3. 与“任务级远程控制”数据量匹配，网络开销小于远程桌面。
4. 后续若接小程序，可平滑扩展到云入口模式。

## 权衡

### 优点

1. 部署与运维复杂度低。
2. 跨网络稳定性较好。
3. 不必暴露家庭网络服务。

### 限制

1. 依赖 tailnet 账号体系和客户端安装。
2. 对纯公网浏览器访问不友好（需云入口补齐）。

## 后续影响

1. 首版 PoC 以 Tailscale 联通验证为准入门槛。
2. 网关监听策略默认“仅内网/隧道可达”，禁止直接公网开放。
3. 预留云中转接入层接口，避免后续小程序改造重构。
