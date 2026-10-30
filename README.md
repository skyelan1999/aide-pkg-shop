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

Terminal 1.3.1 预发布收录于 `skyelan1999/aide-pkg-terminal`，市场ZIP与Release固定提交归档一致（SHA-256 `36118a15e9f253823f9640e3b216a6066f91e5fd453bb3f2a9abe6f8e475d9fe`）。统一 Shell/SSH/TCP/UDP/串口工作台，合并35项通信工具（总49项），支持SFTP/隧道/模拟/代理/回放、显式UTF-8/HEX发送与TX/RX日志。安装包内含固定版ssh2/serialport及运行依赖。需要配套Aide main的 `terminal-communications-v1` 等能力，旧宿主会显示不兼容；单独升级插件不会补齐宿主上下文。Linux及原生串口虚拟PTY已验证，真实硬件与Windows/macOS未实测；旧包保留，升级会结束现有连接。

Workflow 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-workflow`，保留已有市场安装包的版本、字节内容与 SHA-256。它仅声明 `workflow-start`、`workflow-status`、服务名和面板槽位，没有可执行的工作流编排、进度查询或独立界面实现。Release 说明提供仓库固定提交的安装文件链接。

EnvGuide 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-EnvGuide`，插件 ID 保持 `environment-guide`，保留已有安装包字节与摘要。环境摘要由 Aide 原生上下文构造器按插件启用状态注入；独立 ZIP 不包含 Go 实现。原生回归验证了启停、请求注入、预算记账，以及正文、隐藏文件和来源凭据排除。Release 提供固定提交的安装文件链接。

SQLite 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-sqlite`，保留已有安装包、测试和摘要。需要 Node 的 `node:sqlite`，验证环境为 Node 24。查询默认只读，但事务、脚本默认可写，导出会写文件，不是仅生成提案。既有回归 33/33 通过，实际 ZIP 经 Aide 宿主验证了六个数据库工具和事务回滚；仅使用新建样本库。Release 提供固定提交安装文件链接。

Current Time 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-CurrentTime`，保留既有安装 ZIP 和摘要（SHA-256 `8ccc60d7464971c4ab1ca5c22c1e8ac912e4bfe2f3fb765241aadc5820d4f1ad`）。`get_current_datetime`、`get_week_number` 均可执行，支持 IANA 时区与 ISO-8601 周历；只读 Aide 插件运行环境时钟，即使使用 SSH 工作区也不读取设备时钟。原始行为、真实宿主调用及 Aide/小秘权限回归通过；Linux 实测，Windows/macOS 未实测。Release 提供固定提交的安装 ZIP 与摘要链接。

LunarCalendar 1.0.0 的独立仓库为 `skyelan1999/aide-pkg-LunarCalendar`，保留既有安装 ZIP 和摘要（SHA-256 `38e7fd998add27495c7c9d0bbd5d48ca53ed212af6032edad5e3f33b2a18c5a4`）。`get_lunar_date` 可执行，离线查询农历日期、闰月、干支年和生肖，默认按 Asia/Shanghai 确定今天，依赖 Node Intl/ICU 中国农历数据。原始测试、8次真实宿主调用及 Aide/小秘回归通过；Linux 实测，Windows/macOS 未实测。Release 提供固定提交安装包和摘要链接。

StarLink 当前版本是纯 AI 常驻查询插件，没有独立界面；检索复用增量快照。市场分发包与 StarLink GitHub Release 安装包为同一份字节内容。插件仓库当前未声明开源许可证，因此目录展示 UNLICENSED，不将市场网站的 MIT 许可证套用到该插件。

```sh
python3 scripts/test_private_catalog.py
python3 scripts/test_public_catalog.py
python3 scripts/verify_catalog.py
```

PluginAuthoring（插件工坊）1.0.0 已通过[独立仓库](https://github.com/skyelan1999/aide-pkg-PluginAuthoring)分发；保留原安装包与 `plugin-authoring-v1` 兼容要求，管理操作需要 Aide 原生执行器和人工确认。

Browser Control 1.1.0 已通过[独立仓库](https://github.com/skyelan1999/aide-pkg-BrowserControl)分发，保留原市场安装包；需要宿主浏览器桥接、允许域名配置及操作确认，PDF 另需系统 Python 依赖。

Computer Control 1.1.0 已通过[独立仓库](https://github.com/skyelan1999/aide-pkg-ComputerControl)分发，保留原安装包。桌面桥接支持 macOS，需系统屏幕录制/辅助功能授权；本次实机操作未验证。

Markdown History 1.0.0 已通过[独立仓库](https://github.com/skyelan1999/aide-pkg-MarkdownHistory)分发，保留原市场包；依赖 Aide 原生历史执行器，历史数据仍保存在服务数据目录。

Archive Tools 1.0.0 已通过[独立仓库](https://github.com/skyelan1999/aide-pkg-ArchiveTools)分发，原市场 ZIP 保持一致；依赖 Aide 原生归档执行器，部分格式需要 Python 标准库。

Office 1.1.0 已通过[独立仓库](https://github.com/skyelan1999/aide-pkg-office)分发。Propeller Aero 已按维护者要求从公开目录下架。

串口、SSH、TCP、UDP 的35项通信工具已整合到 Terminal 1.3.1。旧条目 `comm-serial`、`comm-ssh`、`comm-tcp`、`comm-udp` 已从市场下架，新安装请使用 Terminal。

## 插件能力路由

每次构建目录会为所有上架插件生成 `routing` 元数据及独立 `routing.json`，包含关键词、扩展名和精简能力摘要。上架可在 listing 中显式提供 `routing:{keywords:[...],extensions:[...],summary:"..."}`；没有提供时由 ID、名称及已有场景映射生成。修改 listing 后重新运行 `build_catalog.py` 构建目录和索引；`python3 scripts/routing.py` 可为现有目录补齐索引。`verify_catalog.py` 拒绝过期索引，Pages 同时发布索引。信息仅是匹配数据，不携带脚本或执行授权。

支持插件路由接口的新 Aide 会默认下载验证后的目录，在本地匹配需求，只将相关插件工具交给模型。缺少插件时 `route_plugins` 可推荐；宿主用户开启自动安装后，才允许安装匹配且尚未安装的官方公开兼容插件。不购买私有包、不升级或启用用户停用的插件，也不改变工具执行权限。旧宿主可照常浏览安装，不能仅更新商店获得宿主路由功能。

## 截图地址兼容性

市场截图使用本仓库的固定 commit 原始文件地址，以兼容已发布 Aide 的截图域与仓库限制。公开插件截图的未修改副本保存在 `screenshots/<plugin-id>/`，来源 commit、原始地址、SHA-256 和许可证见 `screenshots/provenance.json` 与各目录的 `LICENSE`。更新截图时先提交图片，再以该 commit 更新 listing；随后重建目录并运行 `python3 scripts/test_public_catalog.py`、`python3 scripts/verify_catalog.py`。商业插件仍仅展示筹备元数据，不上传安装包。


DeepSeekSupporter 0.1.0 已独立登记，MIT 许可。Release 与市场使用同一份通用 ZIP；离线价格快照为 2026-10-22，宿主保管凭证。仅声明官方 HTTPS 端点、四个精确模型名／别名、峰谷计价与只读余额协议，不注册生成工具，也未执行真实账户或付费调用。

Codex Bridge 0.3.0 预发布：插件与三端宿主管理器使用同一版本，一次性连接码完成配对；插件工作台支持宿主维护和只读账户额度百分比/重置时间。未知数据不伪造为100%，额度截图为合成数据；真实账户接口可用性与三端CI分开记录。升级时插件和宿主管理器需同时更新，详见[Release](https://github.com/skyelan1999/aide-pkg-CodexBridge/releases/tag/v0.3.0)。

OpenAISupporter 0.1.0 已通过[公开仓库](https://github.com/skyelan1999/aide-pkg-OpenAISupporter)独立分发，MIT 许可。已发布 Aide RC1 不支持 USD，市场兼容门槛暂设为尚未发行的 0.1.17.6 RC2；目前需包含 40b6e96 的 main 源码构建手动导入。四个旗舰模型使用 2026-10-30 Standard 美元价格，包含缓存命中和长上下文阶梯，不提供余额接口。Release 与市场使用同一份通用 ZIP，实际安装包已通过宿主安装、启停、USD/CNY 分开汇总和 race 检查；未调用真实账户或付费模型。
