# CCOS 中枢全量迁移与文档同步

- taskline_id: `ccos/default/unification-migration-20260303`
- project_id: `ccos`
- repo_root: `/Users/zhuxiaowei/ccos`
- ccos_node: `default`
- status: `done`
- updated_at: `2026-03-03 17:35 +08:00`

## 完成事项

1. 中枢目录与入口迁移：
   - `~/pcos` -> `~/ccos`
   - `apps/pcos` -> `apps/ccos`（软链）
2. 协议与脚本统一：
   - `kcos_p0.py` -> `ccos_p0.py`
   - `aggregate_kcos_index.py` -> `aggregate_ccos_index.py`
   - `kcos-index-federated.json` -> `ccos-index-federated.json`
3. 联邦纳管结果：
   - `rpa-mobile/wanling-tower/myth-td-prototype/game_service` 共 4 项目纳入。
4. 文档同步：
   - 新增 `USAGE.md`
   - 更新 `CCOS/context` 与 `capture/tasklines` 双层任务路由。
5. 控制平面落地：
   - 新增 `scripts/ccosctl.py` 与 `scripts/ccosctl` 入口
   - 新增 `scripts/README.md`
6. 协议继承治理：
   - 4 个项目节点协议新增 Node -> Hub 元协议锚点
   - `ccosctl hub lint` 新增锚点强校验，当前结果 `errors=0 warnings=0`

## 回溯

迁移前备份目录：`/Users/zhuxiaowei/ccos_migration_backups/20260303_161540`
