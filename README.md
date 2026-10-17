# Aide 官方插件市场

Aide 官方目录、可直接下载的插件 ZIP 和静态市场网站。市场与 Aide 内置入口共用 `catalog.json`。

## 第一版

- 按名称、描述和 ID 搜索，按工作空间、创作、通信、规划、工具分类。
- 详情提供版本、适用平台、最低宿主版本、权限说明、许可证、源码和 SHA-256。
- 网站下载后在浏览器中核对字节数与 SHA-256，通过后才保存 ZIP；不会请求 Aide 访问令牌。
- 支持市场的 Aide 可直接下载、校验并安装；更新保留原有启用、设置和数据，复用宿主备份恢复流程。
- 无账号、评论、评分或自动收录第三方仓库。暂无实测截图的插件不生成虚假截图。

## 目录与包

`schemaVersion: 1`；每个 `plugins[]` 条目含 `id/kind/name/version/category/package/bytes/sha256/minAideVersion/features/platforms/permissions/source/license/readme/changelog`。

`package` 为本仓库内相对路径。Aide 先解析本仓库 `main` 的提交，再从该固定提交下载目录及 ZIP，不拼接用户提供的下载主机。新版本使用新的包文件名；已发布的旧包保留。首批 ZIP 总量约120 KiB，暂由仓库与 GitHub Pages 直接分发，不伪造尚不存在的 Releases 附件。规模增大后可在新目录版本中引入 Releases/CDN 包源。

`platforms` 表示支持的 Aide 宿主平台，不代表每种外接设备、凭据、系统权限或额外依赖都已实机验收。Node 插件在宿主执行，不是权限沙箱。官方目录和摘要核对不代替安全审阅，也不解除用户授权锁。

目前依赖 GitHub HTTPS 与受控仓库权限建立官方信任，尚未实现独立发布签名。后续可增加签名目录、撤回清单与密钥轮换；不能把 SHA-256 描述成发布方签名。

## 维护与验证

```sh
python3 scripts/build_catalog.py --aide ../aide --ref <明确审阅过的Aide提交>
python3 scripts/verify_catalog.py
node --check market.js
python3 -m http.server 8765 --directory public
```

生成器只读取指定 Git 提交中的受控插件文件并执行 Aide 的独立入口校验，不读取本地 `registry.json`、设置、凭据或缓存。包使用固定排序与时间戳，可重复生成。功能级测试由 Aide 仓库负责；打包通过不等于真实模型或外设验收。

GitHub Pages workflow 仅发布 `public/`，其中只含静态网站、目录及被目录引用的包。首次发布需仓库开启 Pages 的 GitHub Actions 构建。

## 回退

回退目录提交即可停止推荐新版本；客户端不会自动卸载已安装插件。已安装插件按 Aide 的升级备份和恢复说明处理。不要原地覆盖已发版 ZIP。
