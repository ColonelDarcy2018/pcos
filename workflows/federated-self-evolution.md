# 联邦自进化扫描流程

目标：通过联邦注册表扫描多个项目的 CCOS 持久资产，输出一份可复核的“规则 / 技能 / workflow / automation”升级候选报告。

## 输入

1. `machine/federation/project-registry.json`
2. 各项目 `CCOS/context/*.md`
3. 各项目 `CCOS/knowledge/patterns/requirement-pool-v1.md`
4. 各项目 `CCOS/knowledge/architecture/**/*.md`

## 输出

1. `capture/self-evolution/federated-self-evolution-latest.md`

## 执行命令

```bash
python3 /Users/zhuxiaowei/apps/void/tools/ai_dev_harness/self_evolution/scripts/scan_federated_context.py \
  --hub-root /Users/zhuxiaowei/ccos \
  --mode federated \
  --output /Users/zhuxiaowei/ccos/capture/self-evolution/federated-self-evolution-latest.md
```

## 原则

1. 只聚合 durable assets，不宣称读取所有原始聊天记录。
2. 联邦中心只做聚合与路由，不复制项目业务正文。
3. 扫描结果默认进入人类复核，不自动升级顶层规则。
