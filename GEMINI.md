# Gemini Context: H@H Version & Status Monitor

This project is a Python-based monitoring tool designed to track Hentai@Home (H@H) version updates and client statuses across multiple sources.

## Project Overview

-   **Purpose:** Monitors H@H official Java client, `hath-rust` (GitHub releases), and the E-Hentai H@H management page for version updates, daily archive quota, and real-time client status changes.
-   **Architecture:** A standalone Python script (`hath_monitor.py`) that uses standard libraries for networking, scraping, and database management.
-   **Core Technologies:**
    -   **Python 3.11+:** Utilizes the built-in `tomllib` for configuration.
    -   **SQLite:** Stores version history and client status state to track changes.
    -   **Regular Expressions:** Extracted data from E-Hentai's HTML management page.
    -   **Notification Channels:** Supports Bark (iOS), Telegram Bot, and custom Webhooks.
-   **Key Components:**
    -   `hath_monitor.py`: Main logic for scraping, checking updates, and sending notifications.
    -   `config.toml`: Configuration for monitor intervals, EH cookies, and notification endpoints.
    -   `hath_monitor.db`: SQLite database for state persistence.
    -   `hath-monitor.service`: Systemd service unit (runnable as `--user` or system-wide).

## Setup and Running

### Commands

-   **Run Once (Testing):** `python3 hath_monitor.py --verbose`
-   **Run as Daemon:** `python3 hath_monitor.py --daemon`
-   **Force Status Report:** `python3 hath_monitor.py --push-all` (Sends current quota and client statuses regardless of changes).
-   **Check History:** `python3 hath_monitor.py --history`
-   **Service Management (User-level):**
    -   Restart: `systemctl --user restart hath-monitor.service`
    -   Status: `systemctl --user status hath-monitor.service`
    -   Logs: `journalctl --user -u hath-monitor.service -f`

### Configuration

-   Ensure `eh_ipb_member_id` and `eh_ipb_pass_hash` are set in `config.toml` to monitor the EH management page.
-   `check_interval_minutes` determines the polling frequency in daemon mode (default is 5 minutes).

## Development Conventions

-   **Language:** Python 3 (Strictly avoid third-party dependencies where possible).
-   **Scraping:** Use `urllib.request` with custom headers (User-Agent) and SSL context handling for stability.
-   **State Management:** Always query the database to compare "last seen" status before sending a notification to avoid redundant alerts.
-   **Notifications:**
    -   Standardize on Chinese for user-facing push content.
    -   Format: Use `➔` for status transitions (e.g., `离线 ➔ 在线`).
    -   First line of the notification body should contain the most critical info (ID and current status).
-   **Error Handling:** Fail gracefully during network requests to prevent the daemon from crashing; log errors to `hath_monitor.log`.
-   **Versioning:** Follow Semantic Versioning for the script itself (current: 1.3.0).
