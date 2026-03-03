# 联邦索引同步流程（多项目 CCOS）

目标：保留各项目独立 `CCOS` 的前提下，在 CCOS 中枢生成统一检索索引。

本流程遵循统一协议：`meta/ccos-unified-protocol.md`（CCOS Node 与 CCOS Hub 必须协同使用）。

## 输入

- `machine/federation/project-registry.json`（项目与 CCOS 节点注册）。
- 各项目 `CCOS/.index.json`（由各项目自己维护）。

## 输出

- `machine/federation/ccos-index-federated.json`

## 执行命令

```bash
python3 machine/federation/scripts/aggregate_ccos_index.py --ccos-root .
```

## 使用原则

1. 不把项目业务文档复制到中枢。
2. 只聚合索引与状态，保留项目自治。
3. mono 仓可注册多个节点（外层/内层），按 `node_id` 区分。
