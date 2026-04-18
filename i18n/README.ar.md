<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-version-monitor/image?description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Auto" alt="hath-version-monitor" width="640" />
</p>

<h1 align="center">مراقب إصدار وحالة Hentai@Home</h1>

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
  <strong>أداة بايثون خفيفة الوزن وبدون تبعيات لمراقبة تحديثات عميل H@H وحالته في الوقت الفعلي.</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a>
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
curl -L https://raw.githubusercontent.com/cololi/hath-version-monitor/main/config.toml.example -o config.toml

# 2. قم بتحرير ملف config.toml باستخدام ملفات تعريف الارتباط EH ورموز الإشعارات الخاصة بك
# (استخدم محرر النصوص المفضل لديك: vi أو nano أو المفكرة)
vi config.toml 

# 3. ابدأ حاوية المراقب
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 التثبيت اليدوي

إذا كنت تفضل تشغيله مباشرة باستخدام بايثون (3.11+):

```bash
# 1. قم باستنساخ المستودع وادخل إلى الدليل
git clone https://github.com/cololi/hath-version-monitor.git && cd hath-version-monitor

# 2. قم بإنشاء ملف التكوين الافتراضي
python3 hath_monitor.py

# 3. قم بتحرير ملف config.toml الناتج
vi config.toml

# 4. ابدأ المراقب في وضع الخادم الخفي (daemon)
python3 hath_monitor.py --daemon
```

---

## 🛠️ التكوين

ينقسم ملف `config.toml` إلى ثلاثة أقسام رئيسية: `[monitor]` و `[notify]` و `[system]`.

### قنوات الإشعارات

| القناة | المتطلبات الأساسية |
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

## ⌨️ خيارات واجهة السطر البرمجي (CLI)

| العلامة | الوصف |
| :--- | :--- |
| `--daemon` | تشغيل السكربت في الخلفية كخادم خفي. |
| `--verbose` | تمكين تسجيل تصحيح الأخطاء التفصيلي. |
| `--history` | عرض آخر 20 إدخالاً من سجل الحالة. |
| `--push-all` | دفع تقرير حالة كامل فوراً إلى جميع القنوات المفعلة. |
| `--config PATH` | تحديد مسار مخصص لملف التكوين. |

---

## 📜 الترخيص والتقدير

*   **الترخيص**: هذا المشروع مرخص بموجب [رخصة MIT](LICENSE).
*   **التقدير**: شكر خاص لمجتمع Hentai@Home ومطوري خدمات الإشعارات المختلفة المدعومة.
