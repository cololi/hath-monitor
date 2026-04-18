# Hentai@Home Version & Status Monitor (hath-monitor)

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文) | [日本語](#日本語) | [한국어](#한국어) | [Español](#español) | [Français](#français) | [Русский](#русский) | [Deutsch](#deutsch) | [العربية](#العربية) | [עברית](#עברית)

---

## English

A lightweight Python script to monitor Hentai@Home (H@H) version updates, daily archive quota, and the online/offline status of all your clients.

### Features
- **🚀 Real-time Monitoring**: Checks for changes every 5 minutes (configurable).
- **📊 Client Status**: Detailed status reports including IP, version, trust, hitrate, etc.
- **📅 Quota Tracking**: Daily notifications for your Free Archive Quota.
- **🔄 Version Tracking**: Monitors Official Java, `hath-rust`, and EH Web version changes.
- **🔔 Multi-channel**: Support for Bark, Telegram, PushPlus, PushDeer, Pushover, Discord, Slack, Gotify, Matrix, DingTalk, and generic Webhooks.
- **🌐 Multilingual**: Notification support for English, Chinese (S/T), Japanese, Korean, Spanish, French, Russian, German, Arabic, and Hebrew.
- **🐳 Docker Support**: Pre-built images available on GitHub Container Registry (GHCR).
- **🛡️ Zero Dependency**: Built with Python 3.11+ standard library only.

### Docker Usage
You can run this monitor using Docker for easy deployment:
```bash
docker pull ghcr.io/${{ github.repository }}:latest
docker run -d \
  --name hath-monitor \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/${{ github.repository }}:latest
```
*Note: Make sure your `config.toml` exists in the current directory.*

### Quick Start


## 简体中文

一款轻量级的 Python 脚本，用于监控 Hentai@Home (H@H) 的版本更新、每日存档配额和所有客户端的在线/离线状态。

### 核心功能
- **🚀 实时监控**：每隔 5 分钟检查一次状态变化。
- **📊 客户端状态**：检测所有活跃客户端的状态，并推送包含 IP、版本、信任度等详细信息的通知。
- **📅 配额追踪**：每日定时推送当前的免费存档配额。
- **🔔 多渠道通知**：支持 Bark, Telegram, PushPlus, PushDeer, Pushover, Discord, 钉钉。
- **🌐 多语言支持**：支持英文、中文（简/繁）、西班牙语、法语、俄语、德语、阿拉伯语和希伯来语。

---

## Русский

Легкий скрипт на Python для мониторинга обновлений версии Hentai@Home (H@H), ежедневной квоты архива и статуса онлайн/офлайн всех ваших клиентов.

### Функции
- **🚀 Мониторинг в реальном времени**: Проверка изменений каждые 5 минут.
- **📊 Статус клиента**: Подробные отчеты, включая IP, версию, доверие и т. д.
- **🔔 Мультиканальность**: Поддержка Telegram, Discord, Pushover и других.

---

## Deutsch

Ein leichtgewichtiges Python-Skript zur Überwachung von Hentai@Home (H@H) Versions-Updates, der täglichen Archivquote und dem Online/Offline-Status all Ihrer Clients.

### Funktionen
- **🚀 Echtzeit-Überwachung**: Überprüft alle 5 Minuten auf Änderungen.
- **📊 Client-Status**: Detaillierte Statusberichte einschließlich IP, Version, Vertrauen usw.
- **🔔 Multi-Channel**: Unterstützung für Telegram, Discord, Pushover und mehr.

---

## Español

Un script ligero de Python para monitorear las actualizaciones de versión de Hentai@Home (H@H), la cuota de archivo diaria y el estado en línea/desconectado de todos sus clientes.

---

## Français

Un script Python léger pour surveiller les mises à jour de version de Hentai@Home (H@H), le quota d'archive quotidien et le statut en ligne/hors ligne de tous vos clients.

---

## العربية

سكربت بايثون خفيف لمراقبة تحديثات إصدار Hentai@Home (H@H)، وحصة الأرشيف اليومية، وحالة الاتصال لجميع عملائك.

---

## עברית

סקריפט פייתון קל משקל לניטור עדכוני גרסה של Hentai@Home (H@H), מכסת ארכיון יומית וסטטוס מחובר/מנותק של כל הלקוחות שלך.

---

## License
[MIT License](LICENSE)
