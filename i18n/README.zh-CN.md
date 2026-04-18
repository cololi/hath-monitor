<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-version-monitor/image?description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Auto" alt="hath-version-monitor" width="640" />
</p>

<h1 align="center">Hentai@Home 版本与状态监控器</h1>

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
  <strong>一款轻量级、零依赖的 Python 工具，用于监控 H@H 客户端更新及实时运行状态。</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | 简体中文 | <a href="README.zh-TW.md">繁體中文</a>
</p>

---

## 🚀 核心功能

*   **🔍 多源版本追踪**: 同时监控官方 Java 客户端 (`repo.e-hentai.org`)、`hath-rust` (GitHub Releases) 以及 E-Hentai 管理页面的版本更新。
*   **📡 实时状态监控**: 追踪所有 H@H 客户端的在线/离线状态、IP 变更、信任度、点击率及质量。
*   **📅 每日配额提醒**: 每日自动推送当前的免费存档配额 (Free Archive Quota)。
*   **🔔 丰富的通知渠道**: 支持 Discord (精美 Embeds)、Telegram、Slack、Bark、Gotify、Matrix 等 10 余种推送平台。
*   **🌍 多语言支持**: 推送内容完全支持 11 种语言。
*   **🛡️ 零依赖**: 严格使用 Python 3.11+ 标准库构建，无需 `pip install`。
*   **🐳 容器化部署**: 提供优化的 Docker 镜像，部署简单高效。

---

## ⚙️ 快速开始

### 🐳 使用 Docker (推荐)

复制并粘贴以下命令立即开始运行：

```bash
# 1. 下载配置模板
curl -L https://raw.githubusercontent.com/cololi/hath-version-monitor/main/config.toml.example -o config.toml

# 2. 使用你喜欢的编辑器 (vi, nano 或记事本) 修改 config.toml，配置 EH Cookies 和推送 Token
vi config.toml 

# 3. 启动监控容器
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 手动安装

如果你更喜欢直接使用 Python (3.11+) 运行：

```bash
# 1. 克隆仓库并进入目录
git clone https://github.com/cololi/hath-version-monitor.git && cd hath-version-monitor

# 2. 生成默认配置文件
python3 hath_monitor.py

# 3. 修改生成的 config.toml
vi config.toml

# 4. 以守护进程模式启动监控
python3 hath_monitor.py --daemon
```

---

## 🛠️ 配置说明

`config.toml` 文件主要分为三个部分：`[monitor]` (监控配置), `[notify]` (推送配置), 和 `[system]` (系统配置)。

### 推送渠道支持

| 渠道 | 必要参数 |
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

## ⌨️ 命令行选项

| 选项 | 描述 |
| :--- | :--- |
| `--daemon` | 在后台以守护进程模式运行。 |
| `--verbose` | 启用详细的调试日志输出。 |
| `--history` | 显示数据库中最近的 20 条监控历史记录。 |
| `--push-all` | 立即向所有启用的渠道推送一次完整的状态报告。 |
| `--config PATH` | 指定自定义配置文件路径。 |

---

## 📜 许可协议与鸣谢

*   **许可协议**: 本项目基于 [MIT License](LICENSE) 开源。
*   **致谢**: 特别感谢 Hentai@Home 社区以及本项目所支持的各个推送服务的开发者。
