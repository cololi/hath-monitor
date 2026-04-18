# Hentai@Home Version & Status Monitor (hath-monitor)

[English](../README.md) | 简体中文 | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Русский](README.ru.md) | [Deutsch](README.de.md) | [العربية](README.ar.md) | [עברית](README.he.md)

---

一款轻量级的 Python 脚本，用于监控 Hentai@Home (H@H) 的版本更新、每日存档配额和所有客户端的在线/离线状态。

### 核心功能
- **🚀 实时监控**：每隔 5 分钟（可配置）检查一次状态变化。
- **📊 客户端状态**：检测所有活跃客户端的状态，并推送包含 IP、版本、信任度、产率等详细信息的通知。
- **📅 配额追踪**：每日定时推送当前的免费存档配额 (Free Archive Quota)。
- **🔄 版本追踪**：同时监控官方 Java 客户端、`hath-rust` (GitHub Releases) 以及管理页面的版本。
- **🔔 多渠道通知**：支持 Bark, Telegram, PushPlus, PushDeer, Pushover, Discord, Slack, Gotify, Matrix, 钉钉机器人及通用 Webhooks。
- **🌐 多语言支持**：支持 中文 (zh)、英文 (en)、日文 (ja)、韩文 (ko) 等 11 种语言的推送内容。
- **🐳 Docker 支持**：提供预构建镜像，支持自动化流水线。
- **🛡️ 纯净无依赖**：Python 3.11+ 标准库实现，无需安装第三方 pip 库。

### Docker 使用
你可以通过 Docker 轻松部署：
```bash
docker pull ghcr.io/cololi/hath-monitor:latest
docker run -d \
  --name hath-monitor \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```
*注意：请确保当前目录下已存在 `config.toml`。*

### 快速开始
1. 克隆仓库。
2. 运行 `python3 hath_monitor.py` 生成默认配置。
3. 修改 `config.toml`。
4. 运行 `python3 hath_monitor.py --daemon`。

---
[MIT License](../LICENSE)
