# Federation（多项目联邦索引）

本目录用于把多个项目的 `CCOS` 节点接入 CCOS 中枢，实现“分散存储 + 集中索引”。

`CCOS Node` 与 `CCOS Hub` 是分层协同关系，不是二选一；见统一协议：
`~/ccos/meta/ccos-unified-protocol.md`。

## 文件说明

- `project-registry.json`：项目与 CCOS 节点注册表（支持 mono 仓多层节点）。
- `ccos-index-federated.json`：聚合后的联邦索引快照。
- `scripts/aggregate_ccos_index.py`：读取注册表并聚合各节点 `.index.json`。

## 使用方式

```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl hub sync-index --hub-root /Users/zhuxiaowei/ccos
/Users/zhuxiaowei/ccos/scripts/ccosctl hub lint --hub-root /Users/zhuxiaowei/ccos
```

聚合输出可被联邦日报、任务路由与自动化脚本直接复用。

当前也可供联邦自进化扫描复用，输出多项目的规则 / 技能 / workflow 候选报告。
