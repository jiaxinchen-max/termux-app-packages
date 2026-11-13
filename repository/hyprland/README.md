# Hyprland 合成器与主题资产

| 合成器 | 主题 | 交付修订 |
| --- | --- | --- |
| 0.57.0-r7 | classic-r7 | r7 |
| 0.57.0-r7 | m3ww-v1 | r8 |

r8 复用现有 r7 原生合成器。两套静态主题已发布在 hyprland-components-20261113-r1；本次 r2 更新的是按需下载目录、配套源材料和验证状态，主题字节与 SHA 不变。它独立于通用 Wine catalog-v1.json。

components.json 与 App 内置目录逐字节一致，source=release。APK 仅包含可信目录和安装器，不含主题、字体或重复归档。安装/修复或停止桌面后的切换按固定 URL、大小和 SHA 获取所选主题；已安装包和验证缓存可离线复用。下载、解包或激活失败不改变原选择。普通桌面启动不联网获取组件。

主题归档只含静态配置、图像、字体、manifest 和许可，原生依赖另行安装。API CLI/deb 也采用资产库分发，见 ../android-api/README.md；Android API 宿主保留 APK。Linux 下 API 随 App 构建，但输出不打入 APK；Hyprland/KWin 原生包仍在指定远程编译机编译。

source-lock.json 固定 App 基础提交、未提交的源码覆盖、删除文件清单与每项 SHA。Release 的 runtime-assets-source-overlay.tar.gz 为 App 基础提交上的覆盖包，SOURCE-OVERLAY.json 说明需要移除的旧 APK 资产输入。按覆盖包中的构建说明可复现主题和 API 配套资源。资源许可随源码和主题保留。

本次候选发布：https://github.com/jiaxinchen-max/termux-app-packages/releases/tag/hyprland-components-20261113-r2

主题地址在 components.json，可从其 r1 链接直接下载；没有覆盖旧 Release。运行 tools/verify-hyprland-components.py --assets /path/to/downloads 可核验目录、源材料和两套主题。

validation.json 记录 APK 体积、签名和自动化证据。真实 Android 图形、输入、API 硬件和原生/PRoot 场景仍待验收，Harness strict-run 因仓库脚本缺失不可用；历史 r8 证据不能作为本次实机结果。APK 名称保持 termux-app_apt-android-7-debug_arm64-v8a.apk，由 App 侧交付。

回滚恢复旧 APK 和原有效组件，不清空用户 prefix 或配置；删除当前引用的组件前必须先停止对应 App 目录引用。
