<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-monitor/image?description=1&font=Source+Code+Pro&forks=1&issues=1&name=1&pattern=Plus&pulls=1&stargazers=1&theme=Auto" alt="hath-monitor" width="640" />
</p>

<h1 align="center">Hentai@Home 版本與狀態監控器</h1>

<p align="center">
  <a href="https://github.com/cololi/hath-monitor/releases">
    <img src="https://img.shields.io/github/v/release/cololi/hath-monitor?style=flat-square&color=blue" alt="release">
  </a>
  <a href="https://github.com/cololi/hath-monitor/pkgs/container/hath-monitor">
    <img src="https://img.shields.io/badge/docker-ghcr.io-blue?style=flat-square&logo=docker" alt="docker">
  </a>
  <a href="https://github.com/cololi/hath-monitor/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/cololi/hath-monitor?style=flat-square&color=green" alt="license">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square&logo=python" alt="python">
  </a>
</p>

<p align="center">
  <strong>一款輕量級、零依賴的 Python 工具，用於監控 H@H 用戶端更新及實時運行狀態。</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | 繁體中文 | <a href="README.ja.md">日本語</a> | <a href="README.ko.md">한국어</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.ru.md">Русский</a> | <a href="README.de.md">Deutsch</a> | <a href="README.ar.md">العربية</a> | <a href="README.he.md">עברית</a>
</p>

---

## 🚀 核心功能

*   **🔍 多源版本追踪**: 同時監控官方 Java 用戶端 (`repo.e-hentai.org`)、`hath-rust` (GitHub Releases) 以及 E-Hentai 管理頁面的版本更新。
*   **📡 實時狀態監控**: 追蹤所有 H@H 用戶端的在線/離線狀態、IP 變更、信任度、點擊率及質量。
*   **📅 每日配額提醒**: 每日自動推送當前的免費存檔配額 (Free Archive Quota)。
*   **🔔 豐富的通知渠道**: 支持 Discord (精美 Embeds)、Telegram、Slack、Bark、Gotify、Matrix 等 10 餘種推送平台。
*   **🌍 多語言支持**: 推送內容完全支持 11 種語言。
*   **🛡️ 零依賴**: 嚴格使用 Python 3.11+ 標準庫構建，無需 `pip install`。
*   **🐳 容器化部署**: 提供優化的 Docker 鏡像，部署簡單高效。

---

## ⚙️ 快速開始

### 🐳 使用 Docker (推薦)

複製並粘貼以下命令立即開始運行：

```bash
# 1. 下載配置模板
curl -L https://raw.githubusercontent.com/cololi/hath-monitor/main/config.toml.example -o config.toml

# 2. 使用您喜歡的編輯器 (vi, nano 或記事本) 修改 config.toml，配置 EH Cookies 和推送 Token
vi config.toml 

# 3. 啟動監控容器
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 手動安裝

如果您更喜歡直接使用 Python (3.11+) 運行：

```bash
# 1. 克隆倉庫並進入目錄
git clone https://github.com/cololi/hath-monitor.git && cd hath-monitor

# 2. 生成默認配置文件
python3 hath_monitor.py

# 3. 修改生成的 config.toml
vi config.toml

# 4. 以守護進程模式啟動監控
python3 hath_monitor.py --daemon
```

---

## 🛠️ 配置說明

`config.toml` 文件主要分為三個部分：`[monitor]` (監控配置), `[notify]` (推送配置), 和 `[system]` (系統配置)。

### 推送渠道支持

| 渠道 | 必要參數 |
| :--- | :--- |
| **Bark** | `bark_url` |
| **Telegram** | `telegram_bot_token`, `telegram_chat_id` |
| **Discord** | `discord_webhook` |
| **Slack** | `slack_webhook` |
| **Pushover** | `pushover_user_key`, `pushover_api_token` |
| **Gotify** | `gotify_url`, `gotify_token` |
| **Matrix** | `matrix_url`, `matrix_token`, `matrix_room_id` |
| **PushPlus** | `pushplus_token` |
| **PushDeer** | `pushdeer_key` |
| **DingTalk** | `dingtalk_access_token` |
| **Webhooks** | `webhooks = ["url1", "url2"]` |

---

## ⌨️ 命令行選項

| 選項 | 描述 |
| :--- | :--- |
| `--daemon` | 在後台以守護進程模式運行。 |
| `--verbose / -v` | 啟用詳細的調試日誌輸出。 |
| `--history` | 顯示資料庫中最近的 20 條監控歷史記錄。 |
| `--push-all` | 立即向所有啟用的渠道推送一次完整的狀態報告。 |
| `--config PATH` | 指定自定義配置文件路徑。 |

---

## 📜 許可協議與鳴謝

*   **許可協議**: 本項目基於 [MIT License](LICENSE) 開源。
*   **致謝**: 特別感謝 Hentai@Home 社區以及本项目所支持的各个推送服务的開發者。
