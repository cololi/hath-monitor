<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-monitor/image?description=1&font=Source+Code+Pro&forks=1&issues=1&name=1&pattern=Plus&pulls=1&stargazers=1&theme=Auto" alt="hath-monitor" width="640" />
</p>

<h1 align="center">Hentai@Home Versions- & Statusmonitor</h1>

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
  <strong>Ein leichtgewichtiges, abhängigkeitsfreies Python-Tool zur Überwachung von H@H-Client-Updates und Echtzeit-Status.</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.ko.md">한국어</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.ru.md">Русский</a> | Deutsch | <a href="README.ar.md">العربية</a> | <a href="README.he.md">עברית</a>
</p>

---

## 🚀 Hauptmerkmale

*   **🔍 Versionsverfolgung aus mehreren Quellen**: Überwacht den offiziellen Java-Client (`repo.e-hentai.org`), `hath-rust` (GitHub Releases) und die E-Hentai H@H-Managementseite auf Versionsänderungen.
*   **📡 Echtzeit-Statusüberwachung**: Verfolgt Online-/Offline-Status, IP-Änderungen, Vertrauensstufen, Hitrate und Qualität für alle Ihre H@H-Clients.
*   **📅 Tägliche Quoten-Benachrichtigungen**: Automatische tägliche Benachrichtigungen für Ihre Free Archive Quota.
*   **🔔 Umfangreiche Benachrichtigungen**: Unterstützt mehr als 10 Kanäle, darunter Discord (Rich Embeds), Telegram, Slack, Bark, Gotify, Matrix und mehr.
*   **🌍 Mehrsprachige Unterstützung**: Vollständig lokalisierte Benachrichtigungen in 11 Sprachen.
*   **🛡️ Keine Abhängigkeiten**: Ausschließlich mit Python 3.11+ Standardbibliotheken erstellt. Kein `pip install` erforderlich.
*   **🐳 Container-bereit**: Optimierte Docker-Images für eine einfache Bereitstellung.

---

## ⚙️ Schnellstart

### 🐳 Mit Docker (Empfohlen)

Kopieren Sie diese Befehle und fügen Sie sie ein, um sofort zu beginnen:

```bash
# 1. Laden Sie die Konfigurationsvorlage herunter
curl -L https://raw.githubusercontent.com/cololi/hath-monitor/main/config.toml.example -o config.toml

# 2. Bearbeiten Sie die config.toml mit Ihren EH-Cookies und Benachrichtigungs-Token
# (Verwenden Sie Ihren bevorzugten Editor: vi, nano oder Notepad)
vi config.toml 

# 3. Starten Sie den Monitor-Container
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 Manuelle Installation

Wenn Sie es vorziehen, es direkt mit Python (3.11+) auszuführen:

```bash
# 1. Klonen Sie das Repository und wechseln Sie in das Verzeichnis
git clone https://github.com/cololi/hath-monitor.git && cd hath-monitor

# 2. Erstellen Sie die Standardkonfigurationsdatei
python3 hath_monitor.py

# 3. Bearbeiten Sie die generierte config.toml
vi config.toml

# 4. Starten Sie den Monitor im Daemon-Modus
python3 hath_monitor.py --daemon
```

---

## 🛠️ Konfiguration

Die Datei `config.toml` ist in drei Hauptabschnitte unterteilt: `[monitor]`, `[notify]` und `[system]`.

### Benachrichtigungskanäle

| Kanal | Erforderlicher Schlüssel |
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

## ⌨️ CLI-Optionen

| Flag | Beschreibung |
| :--- | :--- |
| `--daemon` | Führt das Skript im Hintergrund als Daemon aus. |
| `--verbose / -v` | Aktiviert detaillierte Debug-Protokollierung. |
| `--history` | Zeigt die letzten 20 Einträge aus dem Statusverlauf an. |
| `--push-all` | Sendet sofort einen vollständigen Statusbericht an alle aktivierten Kanäle. |
| `--config PATH` | Gibt einen benutzerdefinierten Pfad für die Konfigurationsdatei an. |

---

## 📜 Lizenz & Danksagungen

*   **Lizenz**: Dieses Projekt ist unter der [MIT-Lizenz](LICENSE) lizenziert.
*   **Credits**: Besonderer Dank geht an die Hentai@Home-Community und die Entwickler der verschiedenen unterstützten Benachrichtigungsdienste.
