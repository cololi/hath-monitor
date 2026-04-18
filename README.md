# Hentai@Home 版本与状态监控器 (hath-monitor)

一个轻量级的 Python 脚本，用于监控 Hentai@Home (H@H) 的版本更新、每日存档配额和所有客户端的在线/离线状态。

## 核心功能

- **🚀 实时监控**：每隔 5 分钟（可配置）检查一次状态变化。
- **📊 客户端状态**：检测所有活跃客户端的状态，并推送包含 IP、版本、信任度、产率等详细信息的通知。
- **📅 配额追踪**：每日定时推送当前的免费存档配额 (Free Archive Quota)。
- **🔄 版本追踪**：同时监控官方 Java 客户端、`hath-rust` (GitHub Releases) 以及管理页面的版本。
- **🔔 多渠道通知**：支持 Bark (iOS)、Telegram Bot、通用 Webhooks。
- **🗃️ 历史记录**：所有变更均保存在本地 SQLite 数据库中。
- **🌐 全中文支持**：推送内容专为中文环境优化，简洁明了。

## 快速安装

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/hath-monitor.git
cd hath-monitor

# 2. 准备配置文件
cp config.toml.example config.toml
# 修改 config.toml 填入你的 cookies 和通知 Token
vim config.toml

# 3. 手动运行测试
python3 hath_monitor.py --verbose

# 4. 强制全量推送当前所有状态
python3 hath_monitor.py --push-all
```

## 部署

### Systemd (推荐)
提供 `hath-monitor.service` 模板，支持作为用户级服务运行：

```bash
mkdir -p ~/.config/systemd/user/
cp hath-monitor.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now hath-monitor.service
```

## 通知示例

**标题**：`H@H 状态报告: Home`
**内容**：
```text
当前状态: 在线 (ID: 32864)
详情: 在线 (保持中)
地区: Chinese Dominion
地址: 1.2.3.4:6633
版本: 1.6.5 Stable
带宽: 6400 KB/s
信任: +1000
质量: 10000
点击: 615.1 / min
产率: 113.2 / day
已传: 1,526,624,199
最后: Today, 12:54
```

## 依赖
- Python 3.11+ (无需安装任何第三方 pip 库)
- 低于 3.11 的 Python 需要安装 `tomli`

## 开源协议
[MIT License](LICENSE)
