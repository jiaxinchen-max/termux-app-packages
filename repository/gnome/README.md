# GNOME 50 / Ubuntu Resolute 组件

组件版本与 App 源码 `52ccd543` 的安装清单配套，初始化在保存／安装阶段完成。组件按需下载，不加入 APK。

| 发行版 | 内容 | 验证范围 |
| --- | --- | --- |
| [gnome-50-resolute-20261116-r1](https://github.com/jiaxinchen-max/termux-app-packages/releases/tag/gnome-50-resolute-20261116-r1) | 四个 GNOME 50 核心 DEB、三个复用依赖、Resolute GIO / Glycin | 原编译链、Android ABI、隔离 PRoot 实际桌面及生命周期 |
| [native-ubuntu-gnome-50-r1](https://github.com/jiaxinchen-max/termux-app-packages/releases/tag/native-ubuntu-gnome-50-r1) | Yaru、壁纸和四个 Ubuntu 扩展 | 实际资源测试、下载哈希、两次构建一致 |

两个公开集成验证版包含精确 URL、大小、SHA256、源码配方、来源锁和校验清单。第三方 Mesa/Turnip 继续使用 lfdevs 专用上游地址。旧 GNOME 48 资产和索引保留；这些桌面安装组件不加入 Wine runtime catalog。

完整 Native GUI、四类 PRoot 全新安装、Discover 授权、真实 USB／高通 GPU 仍待验证。旧综合桌面脚本夹具未通过；Harness strict gate 缺失。发布组件不等于完成 App 整体验收或归档；未发布新 APK。具体证据和限制见各版本 `validation.json` 及发布回读记录。
