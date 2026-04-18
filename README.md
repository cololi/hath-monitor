# Hentai@Home Version & Status Monitor (hath-monitor)

English | [简体中文](i18n/README.zh-CN.md) | [繁體中文](i18n/README.zh-TW.md) | [日本語](i18n/README.ja.md) | [한국어](i18n/README.ko.md) | [Español](i18n/README.es.md) | [Français](i18n/README.fr.md) | [Русский](i18n/README.ru.md) | [Deutsch](i18n/README.de.md) | [العربية](i18n/README.ar.md) | [עברית](i18n/README.he.md)

---

A lightweight Python script to monitor Hentai@Home (H@H) version updates, daily archive quota, and the online/offline status of all your clients.

### Features
- **🚀 Real-time Monitoring**: Checks for changes every 5 minutes (configurable).
- **📊 Client Status**: Detailed status reports including IP, version, trust, hitrate, etc.
- **📅 Quota Tracking**: Daily notifications for your Free Archive Quota.
- **🔄 Version Tracking**: Monitors Official Java, `hath-rust`, and EH Web version changes.
- **🔔 Multi-channel**: Support for Bark, Telegram, PushPlus, PushDeer, Pushover, Discord, Slack, Gotify, Matrix, DingTalk, and generic Webhooks.
- **🌐 Multilingual**: Notification support for English, Chinese (S/T), Japanese, Korean, Spanish, French, Russian, German, Arabic, and Hebrew (11 languages).
- **🐳 Docker Support**: Pre-built images available on GitHub Container Registry (GHCR).
- **🛡️ Zero Dependency**: Built with Python 3.11+ standard library only.

### Docker Usage
You can run this monitor using Docker for easy deployment:
```bash
docker pull ghcr.io/cololi/hath-monitor:latest
docker run -d \
  --name hath-monitor \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```
*Note: Make sure your `config.toml` exists in the current directory.*

### Quick Start
1. Clone the repository.
2. Run `python3 hath_monitor.py` to generate the default `config.toml`.
3. Edit `config.toml` with your credentials and notification tokens.
4. Run `python3 hath_monitor.py --daemon` to start the monitor.

### CLI Options
- `--daemon`: Run as a daemon process.
- `--verbose`: Show detailed debug logs.
- `--history`: View recent monitoring records.
- `--push-all`: Force an immediate full status report.

---
## License
[MIT License](LICENSE)
