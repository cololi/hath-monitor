<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-version-monitor/image?description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Auto" alt="hath-version-monitor" width="640" />
</p>

<h1 align="center">Монитор версий и статуса Hentai@Home</h1>

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
  <strong>Легкий инструмент на Python без зависимостей для мониторинга обновлений и статуса клиента H@H в реальном времени.</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a>
</p>

---

## 🚀 Основные возможности

*   **🔍 Отслеживание версий из нескольких источников**: Мониторинг официального Java-клиента (`repo.e-hentai.org`), `hath-rust` (GitHub Releases) и страницы управления H@H на E-Hentai.
*   **📡 Мониторинг статуса в реальном времени**: Отслеживание онлайн/оффлайн статуса, изменений IP, уровней доверия, хитрэйта и качества всех ваших клиентов H@H.
*   **📅 Уведомления о дневной квоте**: Автоматические ежедневные уведомления о вашей бесплатной архивной квоте (Free Archive Quota).
*   **🔔 Разнообразные уведомления**: Поддержка более 10 каналов, включая Discord (Rich Embeds), Telegram, Slack, Bark, Gotify, Matrix и другие.
*   **🌍 Многоязычная поддержка**: Полная локализация уведомлений на 11 языках.
*   **🛡️ Без зависимостей**: Создано исключительно с использованием стандартных библиотек Python 3.11+. Не требуется `pip install`.
*   **🐳 Готов к Docker**: Оптимизированные Docker-образы для легкого развертывания.

---

## ⚙️ Быстрый старт

### 🐳 Использование Docker (рекомендуется)

Скопируйте и вставьте эти команды для быстрого запуска:

```bash
# 1. Скачайте шаблон конфигурации
curl -L https://raw.githubusercontent.com/cololi/hath-version-monitor/main/config.toml.example -o config.toml

# 2. Отредактируйте config.toml, указав ваши куки EH и токены уведомлений
# (Используйте ваш любимый редактор: vi, nano или блокнот)
vi config.toml 

# 3. Запустите контейнер монитора
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 Ручная установка

Если вы предпочитаете запускать напрямую через Python (3.11+):

```bash
# 1. Клонируйте репозиторий и перейдите в директорию
git clone https://github.com/cololi/hath-version-monitor.git && cd hath-version-monitor

# 2. Создайте файл конфигурации по умолчанию
python3 hath_monitor.py

# 3. Отредактируйте созданный config.toml
vi config.toml

# 4. Запустите монитор в режиме демона
python3 hath_monitor.py --daemon
```

---

## 🛠️ Конфигурация

Файл `config.toml` разделен на три основных раздела: `[monitor]`, `[notify]` и `[system]`.

### Каналы уведомлений

| Канал | Необходимые данные |
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

## ⌨️ Параметры CLI

| Флаг | Описание |
| :--- | :--- |
| `--daemon` | Запустить скрипт в фоновом режиме как демон. |
| `--verbose` | Включить подробное логирование отладки. |
| `--history` | Показать последние 20 записей из истории статусов. |
| `--push-all` | Немедленно отправить полный отчет о статусе во все включенные каналы. |
| `--config PATH` | Указать пользовательский путь к файлу конфигурации. |

---

## 📜 Лицензия и благодарности

*   **Лицензия**: Этот проект лицензирован под [MIT License](LICENSE).
*   **Благодарности**: Особая благодарность сообществу Hentai@Home и разработчикам различных поддерживаемых сервисов уведомлений.
