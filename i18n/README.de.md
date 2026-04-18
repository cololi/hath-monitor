<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-version-monitor/image?description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Auto" alt="hath-version-monitor" width="640" />
</p>

<h1 align="center">Hentai@Home Versions- & Statusmonitor</h1>

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
  <strong>Ein leichtgewichtiges, abhängigkeitsfreies Python-Tool zur Überwachung von H@H-Client-Updates und Echtzeit-Status.</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a>
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
curl -L https://raw.githubusercontent.com/cololi/hath-version-monitor/main/config.toml.example -o config.toml

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
git clone https://github.com/cololi/hath-version-monitor.git && cd hath-version-monitor

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
| `--verbose` | Aktiviert detaillierte Debug-Protokollierung. |
| `--history` | Zeigt die letzten 20 Einträge aus dem Statusverlauf an. |
| `--push-all` | Sendet sofort einen vollständigen Statusbericht an alle aktivierten Kanäle. |
| `--config PATH` | Gibt einen benutzerdefinierten Pfad für die Konfigurationsdatei an. |

---

## 📜 Lizenz & Danksagungen

*   **Lizenz**: Dieses Projekt ist unter der [MIT-Lizenz](LICENSE) lizenziert.
*   **Credits**: Besonderer Dank geht an die Hentai@Home-Community und die Entwickler der verschiedenen unterstützten Benachrichtigungsdienste.

---

## 👥 Mitwirkende

<p align="center">
  <table align="center">
    <tr>
      <td align="center">
        <a href="https://github.com/cololi">
          <img src="https://github.com/cololi.png" width="100px;" alt="Cololi"/><br />
          <sub><b>Cololi</b></sub>
        </a><br />
        🚀 <b>Hauptentwickler</b>
      </td>
      <td align="center">
        <a href="https://gemini.google.com/">
          <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/google-gemini-icon.png" width="100px;" alt="Gemini AI"/><br />
          <sub><b>Gemini AI</b></sub>
        </a><br />
        🤖 <b>KI-Assistent</b>
      </td>
    </tr>
  </table>
</p>

<p align="center">Mit ❤️ für die H@H-Community gemacht</p>
