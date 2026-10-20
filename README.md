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

## 私有付费条目

`distribution=private` 的 `listings/*.json` 是人工审阅的展示元数据，由生成器合并进目录的 `privateListings` 扩展数组，原 `plugins` 只保留免费包，让旧版 Aide 仍能刷新原目录。`distribution=private` 的条目不得包含 `package/sha256/bytes` 等公开包字段，也不得在本仓库 `packages/<id>/` 存包；验证器拒绝这些情况。Pages 只复制公开包，并在重建前清理生成目录里的旧包副本。PjPlan 目前仅展示“付费筹备中”，没有价格、购买入口或真实签发密钥。

私有条目使用 `commerce.status=coming_soon|available`、`model=perpetual-major`、`priceLabel`、可选 HTTPS `purchaseURL` 和发布者 Ed25519 `publicKeys`（key ID → 标准 Base64 的 32 字节公钥）。开放授权安装至少需要一把公钥。Aide 通过 `private-plugin-v1` 能力识别，旧宿主不会尝试当免费包下载安装。不要把私钥、订单、客户许可证或私有存储永久链接写进公开目录。

目前交付路径是：购买者给出 Aide 安装授权码 → 发布者在私有环境确认权益、签发许可证 → 私下交付 ZIP 和许可证 → Aide 详情中核验安装。官网只展示商品或跳转购买，不接收客户安装包，不处理支付或自动发货。在线授权服务与短效下载地址是后续接口，不是已上线能力。

现有免费包的 MIT 许可不自动适用于其他条目；历史已公开内容和第三方权利不被新商业条款追溯改变。

## 独立公开插件

独立仓库的公开插件以 `listings/<id>.json` 登记，使用 `distribution=public`，包含与内置包相同的 package/sha256/bytes 及详情字段。生成器会将它们合并进 plugins；验证器校验包路径、ZIP、清单身份、版本、字节数和摘要。私有条目的分发限制保持不变。

Skill Library 1.1.0 独立分发于 `skyelan1999/aide-pkg-skill`，保留已有市场安装包的版本、字节内容与 SHA-256。插件需要包含 `skill_library` 原生执行器的 Aide 构建；公开 Skill 的准备和只读引用登记仍遵守管理权限、用户确认与引用锁，不自动执行下载的脚本。

Goal 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-goal`，保留已有市场安装包的版本、字节内容与 SHA-256。它是目标能力预设，仅声明 `goal-create`、`goal-status`、服务名和面板槽位；当前没有目标管理 handler、存储或独立界面。独立收录不会给已安装的同版本插件强制提供升级。

Plan 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-plan`，保留已有市场安装包的版本、字节内容与 SHA-256。它仅声明 `plan-make`、`plan-review`、服务名和面板槽位，没有可执行的计划生成、审查或独立界面实现。

Todo 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-todo`，保留已有市场安装包的版本、字节内容与 SHA-256。它仅声明 `todo-list`、`todo-update`、服务名和面板槽位，没有可执行的任务查询、状态更新或独立界面实现。Release 说明提供仓库固定提交的安装 ZIP 与摘要下载链接。

Feedback 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-feedback`，保留已有市场安装包的版本、字节内容与 SHA-256。它仅声明 `feedback-capture`、`feedback-summary`、服务名和面板槽位，没有可执行的反馈采集、汇总或独立界面实现。Release 说明提供仓库固定提交的安装 ZIP 与摘要下载链接。

Subagent 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-subagent`，保留已有市场安装包的版本、字节内容与 SHA-256。它仅声明 `subagent-spawn`、`subagent-report`、服务名和面板槽位，没有可执行的子代理调度、结果回收或独立界面实现。Release 说明提供仓库固定提交的安装 ZIP 与摘要下载链接。

Terminal 1.2.0 预发布收录于 `skyelan1999/aide-pkg-terminal`，市场ZIP与Release固定提交归档逐字节一致（SHA-256 `38a4cf3a964b6e5b8a44a04c3ebfee3045f6c46742c9c40c54ba6137693315f1`）。提供本地/SSH工作区Shell、常驻设备SSH、密码/加密私钥认证、引用私钥选择、会话管理和轮转日志；Linux实测，Windows原生PTY未实现。条目要求 `terminal-workbench-v1` 和 `terminal-ssh-workspace-v1` 能力，旧宿主会显示不兼容；需要 [Aide main](https://github.com/skyelan1999/aide/tree/main) 的桥接续期与后台分离；main 已移除插件新标签页入口，单独升级插件不会替换宿主界面，公开0.1.17.3 RC1仍不能完整使用。旧1.0.0包保留；更新插件会结束现有连接，工作区日志保留。

Workflow 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-workflow`，保留已有市场安装包的版本、字节内容与 SHA-256。它仅声明 `workflow-start`、`workflow-status`、服务名和面板槽位，没有可执行的工作流编排、进度查询或独立界面实现。Release 说明提供仓库固定提交的安装文件链接。

EnvGuide 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-EnvGuide`，插件 ID 保持 `environment-guide`，保留已有安装包字节与摘要。环境摘要由 Aide 原生上下文构造器按插件启用状态注入；独立 ZIP 不包含 Go 实现。原生回归验证了启停、请求注入、预算记账，以及正文、隐藏文件和来源凭据排除。Release 提供固定提交的安装文件链接。

SQLite 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-sqlite`，保留已有安装包、测试和摘要。需要 Node 的 `node:sqlite`，验证环境为 Node 24。查询默认只读，但事务、脚本默认可写，导出会写文件，不是仅生成提案。既有回归 33/33 通过，实际 ZIP 经 Aide 宿主验证了六个数据库工具和事务回滚；仅使用新建样本库。Release 提供固定提交安装文件链接。

StarLink 当前版本是纯 AI 常驻查询插件，没有独立界面；检索复用增量快照。市场分发包与 StarLink GitHub Release 安装包为同一份字节内容。插件仓库当前未声明开源许可证，因此目录展示 UNLICENSED，不将市场网站的 MIT 许可证套用到该插件。

```sh
python3 scripts/test_private_catalog.py
python3 scripts/test_public_catalog.py
python3 scripts/verify_catalog.py
```
