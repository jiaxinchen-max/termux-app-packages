# Android API 配套运行时资产

Android API 的 Java/IPC 宿主继续位于主 APK。CLI、公共脚本/回调、termux-api.deb 和 ARM64 UPower deb 由资产库提供，APK 仅包含 runtime-api-components.json 的可信目录和安装器。

当前发布 embedded-termux-api-0.60.0-r2 为四种 ABI 提供独立确定性 ZIP；每个 ZIP 的 termux-api.deb 与 r1 已公开同架构 deb 字节完全一致。它们仍在 Linux 下用 App 相同 NDK 和固定源码随 App 构建，输出目录不作为 Android assets 输入。CLI/脚本面向主 APK 的 embedded-v1 协议，不依赖另装 com.termux.api。源与许可见源覆盖包 tools/embedded-termux-api 及 distribution/embedded-termux-api。

初始化/修复只下载当前进程 ABI 的固定版本，通过大小、归档 SHA 和每文件白名单/摘要验证后持锁安装。断网、错误 ABI、摘要不符或中断不写完整成功状态，保留旧文件，恢复未完成事务后可重试；完整已安装内容和有效缓存可离线复用。ZIP 中的链接、越界、重复与超限项被拒绝。

基础终端与 API 组件状态分别记录。API 下载失败后终端保留，提示重试或继续使用终端；依赖 API 的运行时安装任务必须等配套组件完整才继续。普通桌面启动不新增联网步骤。

目录 runtime-api-components.json 固定 ABI、embedded-v1 契约、URL、大小、SHA 及每文件身份；source-lock.json 固定源码和基础提交（App 适配尚未提交）。源覆盖包中的 SOURCE-OVERLAY.json 含移除旧 APK 资产的清单。

发布：https://github.com/jiaxinchen-max/termux-app-packages/releases/tag/embedded-termux-api-0.60.0-r2

运行 python3 tools/verify-runtime-api-components.py --assets /path/to/downloads 核验四 ABI ZIP、目录和固定 r1 deb。历史 r1 原始 deb/资料保持不变。validation.json 和 Release verification-evidence.tar.gz 记录自动化结果；真实硬件、权限、USB 和 Android 图形/输入仍待设备验收，不使用历史 r8 设备结果冒充本次验证。

回滚可恢复旧 APK/完整旧组件；保留用户 prefix 和缓存。Hyprland/KWin 等原生生态包仍使用指定远程编译机，不在本次本地构建中重编。
