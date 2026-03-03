# CCOS Scripts

## ccosctl

统一入口：`/Users/zhuxiaowei/ccos/scripts/ccosctl`

常用命令：

```bash
# Hub
/Users/zhuxiaowei/ccos/scripts/ccosctl hub lint --hub-root /Users/zhuxiaowei/ccos
/Users/zhuxiaowei/ccos/scripts/ccosctl hub sync-index --hub-root /Users/zhuxiaowei/ccos

# Node
/Users/zhuxiaowei/ccos/scripts/ccosctl node validate --repo-root /Users/zhuxiaowei/apps/rpa-mobile --ccos-root CCOS
/Users/zhuxiaowei/ccos/scripts/ccosctl node sync --repo-root /Users/zhuxiaowei/apps/rpa-mobile --ccos-root CCOS

# Taskline
/Users/zhuxiaowei/ccos/scripts/ccosctl task start --task-id demo/task --title "demo" --project-id rpa-mobile --repo-root /Users/zhuxiaowei/apps/rpa-mobile --node-id outer
```

说明：

1. `ccosctl node validate/sync` 自动兼容不同仓库 `ccos_p0.py` 的参数风格（含 `--root` 差异）。
2. `ccosctl hub lint` 会校验 Node 协议是否锚定中枢协议文档 `ccos-unified-protocol.md`。
3. 在项目目录执行 `ccosctl hub ...` 时，若未传 `--hub-root`，会自动回退到 `~/ccos`。
