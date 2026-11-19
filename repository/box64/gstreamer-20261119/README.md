# Box64 GStreamer 依赖回移（2026-11-19）

范围为 Native（glibc_box64）与 PRoot（rootfs_box64）的 0.2.8、0.3.8、0.4.4 六个当前候选。分别回移上游 [PR #4528](https://github.com/ptitSeb/box64/pull/4528)，将包装层的非必要 GTK 依赖改为 GLib/GObject/GModule；每个版本仅修改 wrappedgstreamer.c 的一行，不升级源码版本。

所有组件编译和归档制备均在现有编译机的 Debian13 SDK 执行。Native 保留 Termux GLIBC 解释器及 RUNPATH；PRoot 使用 /lib/ld-linux-aarch64.so.1，无 Native RUNPATH。原地更新现有标签和同名 tar.xz，仅替换 Box64 ELF，所有支持库、成员路径、权限及链接均逐项核对不变。程序版本、组件 ID、索引修订、默认选择和 URL 保持；索引更新大小、SHA256 及修复说明。

源码锁见 source-locks.json，原/新资产摘要及大小见 package-manifest.json，编译机 42 项实际结果见 verification-results.json。Android App 域36/36项通过，结果见 device-matrix-results.json；六项资产均已原地发布，原URL全量下载的大小/SHA256核对通过，见 publication-results.json。源码、补丁及构建/打包脚本位于 [termux-app 的分发目录](https://github.com/jiaxinchen-max/termux-app/tree/master-x11-submodule-tmp/distribution/termux-app-packages/box64-gstreamer)。

验证针对实际 GStreamer 核心流水线、GObject 类回调、WMV2 解码及 ELF/x86 冒烟。Android Native 媒体检查使用独立 SDK GStreamer 1.26.2 测试库和设备 GLIBC 2.44，PRoot 使用现有 Ubuntu26.04.1/GStreamer1.28.2；测试库不进入分发组件。此前原版 PRoot0.4.4 也能完成 PE64 WMV2 播放，不能把 GTK 报错认定为历史媒体故障根因；本次不声明全部游戏、格式或 Media Foundation 已验收。仓库缺少 Harness 严格脚本，实际返回127，严格门禁未通过。

已安装组件不自动升级。使用更新后的 App 后，手动重新安装对应 Box64 组件即可取得本次资产；无需更改默认版本或重建 Wine 前缀。

原始六份归档、历史构建及原索引均保留。编译机证据目录：/home/builder/proton-sud-dc26-20261108/debian13-buildroot/work/idap-box64-gstreamer-release-20261119/；baselines/ 为可回滚原包。组件仓库两个旧索引同时与 App 当前47项目录同步；除六项 Box64 外不替换其他二进制资产。
