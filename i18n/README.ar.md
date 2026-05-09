<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-monitor/image?description=1&font=Source+Code+Pro&forks=1&issues=1&name=1&pattern=Plus&pulls=1&stargazers=1&theme=Auto" alt="hath-monitor" width="640" />
</p>

<h1 align="center">مراقب إصدار وحالة Hentai@Home</h1>

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
  <strong>أداة بايثون خفيفة الوزن وبدون تبعيات لمراقبة تحديثات عميل H@H وحالته في الوقت الفعلي.</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.ko.md">한국어</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.ru.md">Русский</a> | <a href="README.de.md">Deutsch</a> | العربية | <a href="README.he.md">עברית</a>
</p>

---

## 🚀 الميزات الرئيسية

*   **🔍 تتبع الإصدارات من مصادر متعددة**: يراقب عميل جافا الرسمي (`repo.e-hentai.org`)، و `hath-rust` (إصدارات GitHub)، وصفحة إدارة H@H في E-Hentai لمعرفة تغييرات الإصدار.
*   **📡 مراقبة الحالة في الوقت الفعلي**: يتتبع حالة الاتصال/عدم الاتصال، وتغييرات IP، ومستويات الثقة، ومعدل الإصابة (hitrate)، والجودة لجميع عملاء H@H الخاصين بك.
*   **📅 تنبيهات الحصة اليومية**: إشعارات يومية تلقائية لحصة الأرشيف المجانية (Free Archive Quota).
*   **🔔 إشعارات غنية**: يدعم أكثر من 10 قنوات بما في ذلك Discord (Rich Embeds) و Telegram و Slack و Bark و Gotify و Matrix والمزيد.
*   **🌍 دعم لغات متعددة**: إشعارات معربة بالكامل بـ 11 لغة.
*   **🛡️ بدون تبعيات**: تم بناؤه بدقة باستخدام مكتبات بايثون 3.11+ القياسية. لا يتطلب `pip install`.
*   **🐳 جاهز للحاويات**: صور Docker محسنة لسهولة النشر.

---

## ⚙️ البدء السريع

### 🐳 باستخدام Docker (موصى به)

انسخ هذه الأوامر والصقها للبدء فوراً:

```bash
# 1. قم بتنزيل نموذج التكوين
curl -L https://raw.githubusercontent.com/cololi/hath-monitor/main/.env.example -o .env

# 2. قم بتحرير ملف .env باستخدام ملفات تعريف الارتباط EH ورموز الإشعارات الخاصة بك
# (استخدم محرر النصوص المفضل لديك: vi أو nano أو المفكرة)
vi .env 

# 3. ابدأ حاوية المراقب
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 التثبيت اليدوي

إذا كنت تفضل تشغيله مباشرة باستخدام بايثون (3.11+):

```bash
# 1. قم باستنساخ المستودع وادخل إلى الدليل
git clone https://github.com/cololi/hath-monitor.git && cd hath-monitor

# 2. قم بنسخ نموذج متغيرات البيئة
cp .env.example .env

# 3. قم بتحرير ملف التكوين .env
vi .env

# 4. ابدأ المراقب في وضع الخادم الخفي (daemon)
python3 hath_monitor.py --daemon
```

---

## 🛠️ التكوين

راجع [.env.example](../.env.example) للحصول على القائمة الكاملة لمتغيرات البيئة.

### قنوات الإشعارات

| القناة | المتطلبات الأساسية |
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

## ⌨️ خيارات واجهة السطر البرمجي (CLI)

| العلامة | الوصف |
| :--- | :--- |
| `--daemon` | تشغيل السكربت في الخلفية كخادم خفي. |
| `--verbose / -v` | تمكين تسجيل تصحيح الأخطاء التفصيلي. |
| `--push-all` | دفع تقرير حالة كامل فوراً إلى جميع القنوات المفعلة. |

---

## 📜 الترخيص والتقدير

*   **الترخيص**: هذا المشروع مرخص بموجب [رخصة MIT](LICENSE).
*   **التقدير**: شكر خاص لمجتمع Hentai@Home ومطوري خدمات الإشعارات المختلفة المدعومة.
