<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-monitor/image?description=1&font=Source+Code+Pro&forks=1&issues=1&name=1&pattern=Plus&pulls=1&stargazers=1&theme=Auto" alt="hath-monitor" width="640" />
</p>

<h1 align="center">Hentai@Home バージョン＆ステータスモニター</h1>

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
  <strong>H@H クライアントの更新とリアルタイムステータスを監視するための、軽量で依存関係のない Python ツールです。</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a> | 日本語 | <a href="README.ko.md">한국어</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.ru.md">Русский</a> | <a href="README.de.md">Deutsch</a> | <a href="README.ar.md">العربية</a> | <a href="README.he.md">עברית</a>
</p>

---

## 🚀 主な機能

*   **🔍 マルチソース・バージョントラッキング**: 公式 Java クライアント (`repo.e-hentai.org`)、`hath-rust` (GitHub リリース)、および E-Hentai の H@H 管理ページのバージョン変更を監視します。
*   **📡 リアルタイム・ステータス監視**: すべての H@H クライアントのオンライン/オフライン状態、IP の変更、信頼度、ヒット率、品質を追跡します。
*   **📅 デイリー・クォータ・アラート**: 無料アーカイブクォータ (Free Archive Quota) に関する通知を毎日自動的に送信します。
*   **🔔 豊富な通知機能**: Discord (リッチ埋め込み)、Telegram、Slack、Bark、Gotify、Matrix など、10 以上のチャンネルをサポートしています。
*   **🌍 多言語サポート**: 11 言語に完全ローカライズされた通知。
*   **🛡️ ゼロ依存**: Python 3.11+ の標準ライブラリのみで構築されています。`pip install` は不要です。
*   **🐳 コンテナ対応**: 簡単にデプロイできるように最適化された Docker イメージ。

---

## ⚙️ クイックスタート

### 🐳 Docker を使用する (推奨)

以下のコマンドをコピーして貼り付けるだけで、すぐに開始できます：

```bash
# 1. 設定テンプレートをダウンロード
curl -L https://raw.githubusercontent.com/cololi/hath-monitor/main/.env.example -o .env

# 2. EH の Cookie と通知トークンを使用して .env を編集
# (使い慣れたエディタを使用してください: vi, nano, メモ帳など)
vi .env 

# 3. モニターコンテナを起動
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 手動インストール

Python (3.11+) で直接実行したい場合：

```bash
# 1. リポジトリをクローンしてディレクトリに移動
git clone https://github.com/cololi/hath-monitor.git && cd hath-monitor

# 2. 環境変数のテンプレートをコピー
cp .env.example .env

# 3. .env 設定ファイルを編集
vi .env

# 4. デーモンモードでモニターを起動
python3 hath_monitor.py --daemon
```

---

## 🛠️ 設定

完全な環境変数リストについては [.env.example](../.env.example) を参照してください。

### 通知チャンネル

| チャンネル | 必要なキー |
| :--- | :--- |
| **Bark** | `BARK_URL` |
| **Telegram** | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| **Discord** | `DISCORD_WEBHOOK` |
| **Slack** | `SLACK_WEBHOOK` |
| **Pushover** | `PUSHOVER_USER_KEY`, `PUSHOVER_API_TOKEN` |
| **Gotify** | `GOTIFY_URL`, `GOTIFY_TOKEN` |
| **Matrix** | `MATRIX_URL`, `MATRIX_TOKEN`, `MATRIX_ROOM_ID` |
| **PushPlus** | `PUSHPLUS_TOKEN` |
| **PushDeer** | `PUSHDEER_KEY` |
| **DingTalk** | `DINGTALK_ACCESS_TOKEN` |
| **Webhooks** | `WEBHOOKS` |

---

## ⌨️ CLI オプション

| フラグ | 説明 |
| :--- | :--- |
| `--daemon` | スクリプトをデーモンとしてバックグラウンドで実行します。 |
| `--verbose / -v` | 詳細なデバッグログを有効にします。 |
| `--push-all` | 有効なすべてのチャンネルに、フルステータスレポートを即座に送信します。 |

---

## 📜 ライセンスと謝辞

*   **ライセンス**: このプロジェクトは [MIT ライセンス](LICENSE) の下でライセンスされています。
*   **クレジット**: Hentai@Home コミュニティ、およびサポートされている様々な通知サービスの開発者に感謝します。
