<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-version-monitor/image?description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Auto" alt="hath-version-monitor" width="640" />
</p>

<h1 align="center">Hentai@Home 버전 및 상태 모니터</h1>

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
  <strong>H@H 클라이언트 업데이트 및 실시간 상태를 모니터링하기 위한 가볍고 의존성 없는 Python 도구입니다.</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a>
</p>

---

## 🚀 주요 기능

*   **🔍 멀티 소스 버전 추적**: 공식 Java 클라이언트 (`repo.e-hentai.org`), `hath-rust` (GitHub 릴리스) 및 E-Hentai H@H 관리 페이지의 버전 변경을 모니터링합니다.
*   **📡 실시간 상태 모니터링**: 모든 H@H 클라이언트의 온라인/오프라인 상태, IP 변경, 신뢰도, 히트율 및 품질을 추적합니다.
*   **📅 일일 할당량 알림**: 무료 아카이브 할당량 (Free Archive Quota)에 대한 일일 알림을 자동으로 전송합니다.
*   **🔔 풍부한 알림 지원**: Discord (리치 임베드), Telegram, Slack, Bark, Gotify, Matrix 등 10개 이상의 채널을 지원합니다.
*   **🌍 다국어 지원**: 11개 언어로 완벽하게 로컬라이즈된 알림을 제공합니다.
*   **🛡️ 제로 의존성**: Python 3.11+ 표준 라이브러리만으로 구축되었습니다. `pip install`이 필요하지 않습니다.
*   **🐳 컨테이너 준비**: 쉬운 배포를 위해 최적화된 Docker 이미지를 제공합니다.

---

## ⚙️ 빠른 시작

### 🐳 Docker 사용 (권장)

다음 명령어를 복사하여 붙여넣으면 즉시 시작할 수 있습니다:

```bash
# 1. 설정 템플릿 다운로드
curl -L https://raw.githubusercontent.com/cololi/hath-version-monitor/main/config.toml.example -o config.toml

# 2. EH 쿠키 및 알림 토큰으로 config.toml 수정
# (vi, nano 또는 메모장 등 선호하는 에디터 사용)
vi config.toml 

# 3. 모니터 컨테이너 시작
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 수동 설치

Python (3.11+)으로 직접 실행하려는 경우:

```bash
# 1. 저장소 클론 및 디렉토리 이동
git clone https://github.com/cololi/hath-version-monitor.git && cd hath-version-monitor

# 2. 기본 설정 파일 생성
python3 hath_monitor.py

# 3. 생성된 config.toml 수정
vi config.toml

# 4. 데몬 모드로 모니터 시작
python3 hath_monitor.py --daemon
```

---

## 🛠️ 설정

`config.toml` 파일은 `[monitor]`, `[notify]`, `[system]`의 세 가지 주요 섹션으로 나뉩니다.

### 알림 채널

| 채널 | 필수 키 |
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

## ⌨️ CLI 옵션

| 플래그 | 설명 |
| :--- | :--- |
| `--daemon` | 스크립트를 백그라운드에서 데몬으로 실행합니다. |
| `--verbose` | 상세 디버그 로깅을 활성화합니다. |
| `--history` | 상태 기록에서 마지막 20개 항목을 표시합니다. |
| `--push-all` | 활성화된 모든 채널에 즉시 전체 상태 보고서를 푸시합니다. |
| `--config PATH` | 설정 파일의 사용자 정의 경로를 지정합니다. |

---

## 📜 라이선스 및 크레딧

*   **라이선스**: 이 프로젝트는 [MIT 라이선스](LICENSE)에 따라 라이선스가 부여됩니다.
*   **크레딧**: Hentai@Home 커뮤니티와 지원되는 다양한 알림 서비스 개발자들에게 특별한 감사를 드립니다.

---

## 👥 기여자

<p align="center">
  <table align="center">
    <tr>
      <td align="center">
        <a href="https://github.com/cololi">
          <img src="https://github.com/cololi.png" width="100px;" alt="Cololi"/><br />
          <sub><b>Cololi</b></sub>
        </a><br />
        🚀 <b>리드 개발자</b>
      </td>
      <td align="center">
        <a href="https://gemini.google.com/">
          <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/google-gemini-icon.png" width="100px;" alt="Gemini AI"/><br />
          <sub><b>Gemini AI</b></sub>
        </a><br />
        🤖 <b>AI 어시스턴트</b>
      </td>
    </tr>
  </table>
</p>

<p align="center">H@H 커뮤니티를 위해 ❤️로 제작되었습니다.</p>
