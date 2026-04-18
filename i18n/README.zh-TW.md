# Hentai@Home Version & Status Monitor (hath-monitor)

[English](../README.md) | [简体中文](README.zh-CN.md) | 繁體中文 | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Русский](README.ru.md) | [Deutsch](README.de.md) | [العربية](README.ar.md) | [עברית](README.he.md)

---

一款輕量級的 Python 腳本，用於監控 Hentai@Home (H@H) 的版本更新、每日存檔配額和所有用戶端的在線/離線狀態。

### 核心功能
- **🚀 即時監控**：每隔 5 分鐘（可配置）檢查一次狀態變化。
- **📊 用戶端狀態**：檢測所有活躍用戶端的狀態，並推送包含 IP、版本、信任度、產率等詳細信息的通知。
- **📅 配額追蹤**：每日定時推送當前的免費存檔配額 (Free Archive Quota)。
- **🔄 版本追蹤**：同時監控官方 Java 用户端、`hath-rust` (GitHub Releases) 以及管理頁面的版本。
- **🔔 多渠道通知**：支持 Bark, Telegram, PushPlus, PushDeer, Pushover, Discord, Slack, Gotify, Matrix, 釘釘機器人及通用 Webhooks。
- **🌐 多語言支持**：支持 中文 (zh)、英文 (en)、日文 (ja)、韓文 (ko) 等 11 種語言的推送內容。
- **🐳 Docker 支持**：提供預構建鏡像，支持自動化流水線。
- **🛡️ 零依賴**：Python 3.11+ 標準庫實現，無需安裝第三方 pip 庫。

### Docker 使用
您可以通過 Docker 輕鬆部署：
```bash
docker pull ghcr.io/cololi/hath-monitor:latest
docker run -d \
  --name hath-monitor \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```
*注意：請確保當前目錄下已存在 `config.toml`。*

---
[MIT License](../LICENSE)
