<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-version-monitor/image?description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Auto" alt="hath-version-monitor" width="640" />
</p>

<h1 align="center">Hentai@Home ניטור גרסה וסטטוס</h1>

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
  <strong>כלי Python קל משקל וללא תלות בספריות חיצוניות לניטור עדכוני לקוח H@H וסטטוס בזמן אמת.</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a>
</p>

---

## 🚀 תכונות עיקריות

*   **🔍 מעקב גרסאות מרובה מקורות**: מנטר את לקוח ה-Java הרשמי (`repo.e-hentai.org`), את `hath-rust` (שחרורים ב-GitHub), ואת דף ניהול ה-H@H של E-Hentai לשינויי גרסה.
*   **📡 ניטור סטטוס בזמן אמת**: עוקב אחר מצב מקוון/לא מקוון, שינויי IP, רמות אמון, hitrate ואיכות עבור כל לקוחות ה-H@H שלך.
*   **📅 התראות מכסה יומית**: התראות יומיות אוטומטיות עבור מכסת הארכיון החינמית שלך (Free Archive Quota).
*   **🔔 התראות עשירות**: תומך בלמעלה מ-10 ערוצים כולל Discord (Rich Embeds), Telegram, Slack, Bark, Gotify, Matrix ועוד.
*   **🌍 תמיכה ברב-לשוניות**: התראות מתורגמות במלואן ל-11 שפות.
*   **🛡️ אפס תלות**: בנוי אך ורק עם הספריות הסטנדרטיות של Python 3.11+. אין צורך ב-`pip install`.
*   **🐳 מוכן ל-Docker**: אימג'ים של Docker ממוטבים לפריסה קלה.

---

## ⚙️ התחלה מהירה

### 🐳 שימוש ב-Docker (מומלץ)

העתק והדבק פקודות אלו כדי להתחיל מיד:

```bash
# 1. הורד את תבנית ההגדרה
curl -L https://raw.githubusercontent.com/cololi/hath-version-monitor/main/config.toml.example -o config.toml

# 2. ערוך את ה-config.toml עם עוגיות ה-EH ומפתחות ההתראה שלך
# (השתמש בעורך המועדף עליך: vi, nano או notepad)
vi config.toml 

# 3. הפעל את קונטיינר הניטור
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 התקנה ידנית

אם אתה מעדיף להריץ ישירות עם Python (3.11+):

```bash
# 1. שכפל את המאגר והיכנס לספרייה
git clone https://github.com/cololi/hath-version-monitor.git && cd hath-version-monitor

# 2. צור את קובץ ההגדרה המחדלי
python3 hath_monitor.py

# 3. ערוך את ה-config.toml שנוצר
vi config.toml

# 4. הפעל את הניטור במצב daemon
python3 hath_monitor.py --daemon
```

---

## 🛠️ הגדרות

קובץ ה-`config.toml` מחולק לשלושה סעיפים עיקריים: `[monitor]`, `[notify]`, ו-`[system]`.

### ערוצי התראות

| ערוץ | דרישת מפתח |
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

## ⌨️ אפשרויות CLI

| דגל | תיאור |
| :--- | :--- |
| `--daemon` | הרץ את הסקריפט ברקע כ-daemon. |
| `--verbose` | אפשר רישום דיבאג מפורט. |
| `--history` | הצג את 20 הרשומות האחרונות מהיסטוריית הסטטוס. |
| `--push-all` | שלח מיד דוח סטטוס מלא לכל הערוצים המופעלים. |
| `--config PATH` | ציין נתיב מותאם אישית לקובץ ההגדרה. |

---

## 📜 רישיון ותודות

*   **רישיון**: פרויקט זה מופץ תחת [רישיון MIT](LICENSE).
*   **קרדיטים**: תודה מיוחדת לקהילת Hentai@Home ולמפתחי שירותי ההתראות השונים הנתמכים.

---

## 👥 תורמים

<p align="center">
  <table align="center">
    <tr>
      <td align="center">
        <a href="https://github.com/cololi">
          <img src="https://github.com/cololi.png" width="100px;" alt="Cololi"/><br />
          <sub><b>Cololi</b></sub>
        </a><br />
        🚀 <b>מפתח ראשי</b>
      </td>
      <td align="center">
        <a href="https://gemini.google.com/">
          <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/google-gemini-icon.png" width="100px;" alt="Gemini AI"/><br />
          <sub><b>Gemini AI</b></sub>
        </a><br />
        🤖 <b>עוזר בינה מלאכותית</b>
      </td>
    </tr>
  </table>
</p>

<p align="center">נעשה ב-❤️ עבור קהילת H@H</p>
