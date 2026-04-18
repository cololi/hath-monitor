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
  <strong>A lightweight, zero-dependency Python tool to monitor H@H client updates and real-time status.</strong>
</p>

<p align="center">
  English | <a href="i18n/README.zh-CN.md">简体中文</a> | <a href="i18n/README.zh-TW.md">繁體中文</a>
</p>

---

## 🚀 Key Features

*   **🔍 Multi-Source Version Tracking**: Monitors Official Java client (`repo.e-hentai.org`), `hath-rust` (GitHub Releases), and the E-Hentai H@H management page for version changes.
*   **📡 Real-time Status Monitoring**: Tracks online/offline status, IP changes, trust levels, hitrate, and quality for all your H@H clients.
*   **📅 Daily Quota Alerts**: Automatic daily notifications for your Free Archive Quota.
*   **🔔 Rich Notifications**: Supports 10+ channels including Discord (Rich Embeds), Telegram, Slack, Bark, Gotify, Matrix, and more.
*   **🌍 Multi-language Support**: Fully localized notifications in 11 languages.
*   **🛡️ Zero Dependencies**: Built strictly with Python 3.11+ standard libraries. No `pip install` required.
*   **🐳 Container Ready**: Optimized Docker images for easy deployment.

---

## ⚙️ Quick Start

### 🐳 Using Docker (Recommended)

Copy and paste these commands to get started immediately:

```bash
# 1. Download the configuration template
curl -L https://raw.githubusercontent.com/cololi/hath-version-monitor/main/config.toml.example -o config.toml

# 2. Edit the config.toml with your EH cookies and notification tokens
# (Use your favorite editor: vi, nano, or notepad)
vi config.toml 

# 3. Start the monitor container
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 Manual Installation

If you prefer running it directly with Python (3.11+):

```bash
# 1. Clone the repository and enter the directory
git clone https://github.com/cololi/hath-version-monitor.git && cd hath-version-monitor

# 2. Generate the default configuration file
python3 hath_monitor.py

# 3. Edit the generated config.toml
vi config.toml

# 4. Start the monitor in daemon mode
python3 hath_monitor.py --daemon
```

---

## 🛠️ Configuration

The `config.toml` file is divided into three main sections: `[monitor]`, `[notify]`, and `[system]`.

### Notification Channels

| Channel | Key Requirement |
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

## ⌨️ CLI Options

| Flag | Description |
| :--- | :--- |
| `--daemon` | Run the script in the background as a daemon. |
| `--verbose` | Enable detailed debug logging. |
| `--history` | Display the last 20 entries from the status history. |
| `--push-all` | Immediately push a full status report to all enabled channels. |
| `--config PATH` | Specify a custom path for the configuration file. |

---

## 📜 License & Acknowledgments

*   **License**: This project is licensed under the [MIT License](LICENSE).
*   **Credits**: Special thanks to the Hentai@Home community and the developers of the various notification services supported.

---

## 🤝 Acknowledgements

- This project was developed with the assistance of [Gemini AI](https://gemini.google.com/).
- Special thanks to the Hentai@Home community.

<p align="center">Made with ❤️ for the H@H Community</p>
