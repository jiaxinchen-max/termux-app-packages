# Hyprland 独立组件目录

此目录将原生窗口合成器与主题分别固定版本。它独立于根目录 Wine `catalog-v1.json`，没有修改通用 Wine 目录或历史 r7/r8 资产。

| 原生合成器 | 主题 | 交付修订 | 主要依赖 |
| --- | --- | --- | --- |
| `0.57.0-r7` | `classic-r7` | r7 | XFCE panel、genmon、swaybg |
| `0.57.0-r7` | `m3ww-v1` | r8 | EWW、Foot、Fish、Starship、字体 |

r8 是 App/主题交付修订，复用 r7 原生合成器，没有单独的 r8 runtime。本次不重编或复制 r7 合成器。

- `components.json` 与 App 内置 `hyprland-components.json` 完全相同，声明兼容组合、独立版本、依赖、下载 URL、大小、归档和 manifest 的 SHA-256。
- 两个主题只包含静态配置、图片、字体及许可；App Python 安装逻辑与可执行依赖不在主题包内。App 从 APK 内置的同一主题归档安装，公网 URL 用于公开分发及核验。
- `source-lock.json` 固定原生包、主题、源码覆盖包、App 基础提交及所有覆盖文件的摘要。App 改动尚未提交，不能把基础提交当作已包含适配的提交。
- Release 的 `hyprland-components-source-overlay.tar.gz` 按 App 仓库相对路径保存适配源文件和主题资源。在对应基础提交上覆盖后运行 `python3 tools/build-hyprland-themes.py` 可复现主题、目录、Java 和 shell 定义。它是源码覆盖包，不含整个 App 或 Android SDK。
- 资源许可随各主题携带；m3ww 字体有单独许可。Release `SHA256SUMS` 覆盖本次发布文件。

Linux 下 `termux-api.deb` 随 App 构建。Hyprland、KWin 等 termux-packages 原生包在指定远程编译机使用 `/workspace/termux-packages/build-package.sh` 构建。静态主题归档不需要 deb 构建。

本次为候选发布：自动化验证见 `validation.json`，实际 Android 图形、输入和原生/PRoot 场景仍待验收。历史 r8 的截图和设备证据不代表本次 App 适配已通过实机测试。APK 由 App 侧交付，名称保持 `termux-app_apt-android-7-debug_arm64-v8a.apk`。

发布地址：https://github.com/jiaxinchen-max/termux-app-packages/releases/tag/hyprland-components-20261113-r1

验证下载的目录和主题：

```sh
python3 tools/verify-hyprland-components.py --assets /path/to/release-assets
```

回退可恢复 App 旧配置/旧 APK；新组件目录不改写旧 Release 和旧目录。删除候选项前应先停止 App 对它的引用。
