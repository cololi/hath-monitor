# Gemini Context: H@H Version & Status Monitor

This project is a Python-based monitoring tool designed to track Hentai@Home (H@H) version updates and client statuses across multiple sources.

## Project Overview

-   **Purpose:** Monitors H@H official Java client, `hath-rust` (GitHub releases), and the E-Hentai H@H management page for version updates, daily archive quota, and real-time client status changes.
-   **Architecture:** A standalone Python script (`hath_monitor.py`) that uses standard libraries for networking, scraping, and database management.
-   **Core Technologies:**
    -   **Python 3.11+:** Utilizes the built-in `tomllib` (or `tomli` as fallback) for configuration.
    -   **SQLite:** Stores version history and client status state to track changes.
    -   **Regular Expressions:** Extracted data from E-Hentai's HTML management page.
    -   **Notification Channels:** Supports 10+ channels including Bark, Telegram, Discord (Rich Embeds), Slack, Gotify, Matrix, PushPlus, PushDeer, Pushover, DingTalk, and generic Webhooks.
-   **Key Components:**
    -   `hath_monitor.py`: Main logic for scraping, checking updates, and sending notifications.
    -   `config.toml`: Configuration for monitor intervals, EH cookies, and notification endpoints.
    -   `hath_monitor.db`: SQLite database for state persistence.
    -   `hath-monitor.service`: Systemd service unit.
    -   `Dockerfile`: Containerization support.
    -   `.github/workflows/ci.yml`: Automated Docker builds and GitHub Releases.

## Setup and Running

### Commands

-   **Run Once (Testing):** `python3 hath_monitor.py --verbose`
-   **Run as Daemon:** `python3 hath_monitor.py --daemon`
-   **Force Status Report:** `python3 hath_monitor.py --push-all` (Sends current quota and client statuses regardless of changes).
-   **Check History:** `python3 hath_monitor.py --history`
-   **Docker:**
    -   `docker pull ghcr.io/<repo>:latest`
    -   `docker run -d -v $(pwd)/config.toml:/app/config.toml -v $(pwd)/hath_monitor.db:/app/hath_monitor.db ghcr.io/<repo>:latest`

## Development Conventions

-   **Language:** Python 3 (Minimize third-party dependencies).
-   **Multilingual Support:** All user-facing strings are localized in `I18N` (zh, zh-hant, en, ja, ko, es, fr, ru, de, ar, he).
-   **Scraping:** Use `urllib.request` with custom headers and SSL context handling for stability.
-   **State Management:** Query SQLite to avoid redundant notifications.
-   **Notifications:**
    -   Standardize on localized strings via `get_t(lang, key)`.
    -   Format: Use `➔` for status transitions.
-   **Error Handling:** Isolation via `try-except` blocks for each check module to ensure overall daemon stability.
-   **Versioning:** Current version 1.4.0.
