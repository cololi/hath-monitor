<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-monitor/image?description=1&font=Source+Code+Pro&forks=1&issues=1&name=1&pattern=Plus&pulls=1&stargazers=1&theme=Auto" alt="hath-monitor" width="640" />
</p>

<h1 align="center">Hentai@Home ניטור גרסה וסטטוס</h1>

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
  <strong>כלי Python קל משקל וללא תלות בספריות חיצוניות לניטור עדכוני לקוח H@H וסטטוס בזמן אמת.</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.ko.md">한국어</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.ru.md">Русский</a> | <a href="README.de.md">Deutsch</a> | <a href="README.ar.md">العربية</a> | עברית
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

1. **הכן את הסביבה**: צור קובץ `.env` המבוסס על ה-[תבנית](.env.example).
   ```bash
   curl -L https://raw.githubusercontent.com/cololi/hath-monitor/main/.env.example -o .env
   ```
2. **הגדר**: הוסף את עוגיות ה-EH ומפתחות ההתראה שלך לקובץ ה-`.env`.
3. **הפעל**:
   ```bash
   docker run -d \
     --name hath-monitor \
     --restart unless-stopped \
     --env-file .env \
     -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
     ghcr.io/cololi/hath-monitor:latest
   ```

### 🐍 התקנה ידנית

אם אתה מעדיף להריץ ישירות עם Python (3.11+):

1. **שכפל**:
   ```bash
   git clone https://github.com/cololi/hath-monitor.git && cd hath-monitor
   ```
2. **הגדר**: העתק את `.env.example` ל-`.env` וערוך אותו.
   ```bash
   cp .env.example .env && vi .env
   ```
3. **הפעל**:
   ```bash
   python3 hath_monitor.py --daemon
   ```

---

## 🛠️ הגדרות ופקודות

### אפשרויות CLI

| דגל | תיאור |
| :--- | :--- |
| `--daemon` | הרץ את הסקריפט ברקע כ-daemon. |
| `--verbose / -v` | אפשר רישום דיבאג מפורט. |
| `--push-all` | שלח מיד דוח סטטוס מלא לכל הערוצים המופעלים. |

### משתני סביבה

ראה [.env.example](.env.example) לרשימה המלאה של המשתנים הנתמכים.

---

## 📜 רישיון ותודות

*   **רישיון**: פרויקט זה מופץ תחת [רישיון MIT](LICENSE).
*   **תודות**: תודה מיוחדת לקהילת Hentai@Home ולמפתחי שירותי ההתראות השונים הנתמכים.
