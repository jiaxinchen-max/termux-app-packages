GNOME 50 / Ubuntu Resolute 集成组件

- Mutter 50.1-4、GNOME Shell 50.1-2、GJS 1.88.0、SpiderMonkey 140.17.0-1，使用原 Linux 编译链构建。
- 复用已发布的 libandroid-stub、libepoxy、termux-render；增加 Resolute glibc GIO 与 Glycin 适配。
- Mutter 修复 DING 重启窗口队列崩溃与 keymap 同步重入；Shell 适配 Android 无 logind/亮度管理的环境。
- 组件、源码、来源锁、校验清单独立下载，不加入 APK。
- 保存／安装阶段完成初始化；启动执行保存结果，失败退出。

已通过隔离 PRoot 实际桌面、四扩展、输入、文件管理器、8 次 DING 重启及进程清理。801 项 Java 测试和定向脚本回归通过。

这是公开的集成验证版组件。Native 完整 GUI、四类全新安装、真实 USB／高通 GPU／Discover 仍待验证；未发布新 APK，未完成整体验收。详见 validation.json。
