<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-version-monitor/image?description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Auto" alt="hath-version-monitor" width="640" />
</p>

<h1 align="center">Hentai@Home Version & Status Monitor</h1>

<p align="center">
  <a href="https://github.com/cololi/hath-version-monitor/releases">
    <img src="https://img.shields.io/github/v/release/cololi/hath-version-monitor?style=flat-square&color=blue" alt="release">
  </a>
  <a href="https://github.com/cololi/hath-version-monitor/pkgs/container/hath-monitor">
    <img src="https://img.shields.io/badge/docker-ghcr.io-blue?style=flat-square&logo=docker" alt="docker">
  </a>
  <a href="https://github.com/cololi/hath-version-monitor/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/cololi/hath-version-monitor?style=flat-square&color=green" alt="license">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square&logo=python" alt="python">
  </a>
</p>

<p align="center">
  <a href="https://github.com/cololi/hath-version-monitor"><strong>[GitHub]</strong></a> |
  <a href="https://github.com/cololi/hath-version-monitor/releases"><strong>[Releases]</strong></a> |
  <a href="https://github.com/cololi/hath-version-monitor/pkgs/container/hath-monitor"><strong>[Docker Hub]</strong></a> |
  <a href="https://github.com/cololi/hath-version-monitor/blob/main/LICENSE"><strong>[License]</strong></a>
</p>

<p align="center">
  English | <a href="i18n/README.zh-CN.md">简体中文</a> | <a href="i18n/README.zh-TW.md">繁體中文</a> | <a href="i18n/README.ja.md">日本語</a> | <a href="i18n/README.ko.md">한국어</a> | <a href="i18n/README.es.md">Español</a> | <a href="i18n/README.fr.md">Français</a> | <a href="i18n/README.ru.md">Русский</a> | <a href="i18n/README.de.md">Deutsch</a> | <a href="i18n/README.ar.md">العربية</a> | <a href="i18n/README.he.md">עברית</a>
</p>

---

> **H@H Version & Status Monitor** is a lightweight, zero-dependency Python tool designed to keep you updated on your Hentai@Home clients. It tracks official updates, repository releases, and provides real-time status notifications across various channels.

---

## 🚀 Highlights

- **🔍 Multi-Source Tracking**: Simultaneously monitors Official Java client (`repo.e-hentai.org`), `hath-rust` (GitHub), and E-Hentai management pages.
- **📡 Real-time Monitoring**: Instant alerts for online/offline status, IP changes, trust levels, hitrate, and quality.
- **📅 Daily Quota Alerts**: Get automated daily summaries of your Free Archive Quota.
- **🌍 Global Support**: Fully localized notifications available in **11 languages**.
- **🔔 10+ Notify Channels**: Native support for Discord, Telegram, Slack, Bark, Gotify, Matrix, and more.
- **🛡️ Minimalist Build**: Written in pure Python 3.11+ standard library. Zero `pip install` required.

---

## ⚙️ Getting Started

### 🐳 Using Docker (Recommended)

Quickly deploy the monitor in a containerized environment:

1. **Get Config**: Download the template.
   ```bash
   curl -L https://raw.githubusercontent.com/cololi/hath-version-monitor/main/config.toml.example -o config.toml
   ```
2. **Configure**: Add your EH cookies and notification tokens to `config.toml`.
3. **Run**:
   ```bash
   docker run -d \
     --name hath-monitor \
     --restart unless-stopped \
     -v $(pwd)/config.toml:/app/config.toml \
     -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
     ghcr.io/cololi/hath-monitor:latest
   ```

### 🐍 Manual Setup

Run directly on your host machine:

1. **Clone**:
   ```bash
   git clone https://github.com/cololi/hath-version-monitor.git && cd hath-version-monitor
   ```
2. **Initialize**: Generate default configuration.
   ```bash
   python3 hath_monitor.py
   ```
3. **Start**:
   ```bash
   python3 hath_monitor.py --daemon
   ```

---

## 🛠️ Configuration & Commands

### CLI Options

| Flag | Description |
| :--- | :--- |
| `--daemon` | Run the script in the background as a persistent service. |
| `--verbose / -v` | Enable detailed debug logging for troubleshooting. |
| `--history` | View the last 20 events recorded in the local database. |
| `--push-all` | Trigger an immediate status report to all enabled channels. |
| `--config PATH` | Specify a custom path for the `config.toml` file. |

### Supported Channels

| Channel | Key Parameters |
| :--- | :--- |
| **Discord** | `discord_webhook` |
| **Telegram** | `telegram_bot_token`, `chat_id` |
| **Bark** | `bark_url` |
| **Slack** | `slack_webhook` |
| **Gotify** | `gotify_url`, `token` |
| **Pushover** | `user_key`, `api_token` |
| **Webhooks** | `webhooks = ["url1", "url2"]` |

---

## 📜 License & Acknowledgments

*   **License**: Distributed under the [MIT License](LICENSE).
*   **Acknowledgments**: Special thanks to the Hentai@Home community and all supported notification service providers.
