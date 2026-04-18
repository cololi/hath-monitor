#!/usr/bin/env python3
import argparse, json, logging, re, sqlite3, sys, time, ssl, html, urllib.parse
import urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

# Try to import tomllib (Python 3.11+) or tomli
try:
    import tomllib
except ImportError:
    import tomli as tomllib

APP_NAME, VERSION = "hath-monitor", "1.4.0"
BASE_DIR = Path(__file__).resolve().parent
DB_PATH_DEFAULT, CONFIG_PATH = BASE_DIR / "hath_monitor.db", BASE_DIR / "config.toml"
UA_DEFAULT = f"{APP_NAME}/{VERSION}"
logger = logging.getLogger(APP_NAME)

I18N = {
    "zh": {
        "official": "官方 Java 版",
        "rust": "hath-rust",
        "web": "H@H 网页端",
        "new_version_found": "H@H {label} 新版本: v{ver}",
        "update_type_new": "新发现",
        "update_type_update": "更新",
        "version_info": "状态: {type}\n版本: {old} -> {new}",
        "changelog_label": "更新日志",
        "quota_title": "H@H 每日配额提醒",
        "quota_body": "当前免费存档配额 (Free Archive Quota):\n{quota}",
        "status_change": "状态变更",
        "status_report": "状态报告",
        "client_msg_title": "H@H {type}: {name}",
        "online": "在线",
        "offline": "离线",
        "cur_status": "当前状态",
        "detail": "详情",
        "region": "地区",
        "address": "地址",
        "version": "版本",
        "speed": "带宽",
        "trust": "信任度",
        "quality": "质量",
        "hitrate": "点击率",
        "hathrate": "Hath 产率",
        "served": "已传",
        "last_seen": "最后"
    },
    "zh-hant": {
        "official": "官方 Java 版",
        "rust": "hath-rust",
        "web": "H@H 網頁端",
        "new_version_found": "H@H {label} 新版本: v{ver}",
        "update_type_new": "新發現",
        "update_type_update": "更新",
        "version_info": "狀態: {type}\n版本: {old} -> {new}",
        "changelog_label": "更新日誌",
        "quota_title": "H@H 每日配額提醒",
        "quota_body": "當前免費存檔配額 (Free Archive Quota):\n{quota}",
        "status_change": "狀態變更",
        "status_report": "狀態報告",
        "client_msg_title": "H@H {type}: {name}",
        "online": "在線",
        "offline": "離線",
        "cur_status": "當前狀態",
        "detail": "詳情",
        "region": "地區",
        "address": "地址",
        "version": "版本",
        "speed": "頻寬",
        "trust": "信任度",
        "quality": "質量",
        "hitrate": "點擊率",
        "hathrate": "Hath 產率",
        "served": "已傳",
        "last_seen": "最後"
    },
    "en": {
        "official": "Official Java",
        "rust": "hath-rust",
        "web": "H@H Web",
        "new_version_found": "H@H {label} New Version: v{ver}",
        "update_type_new": "New",
        "update_type_update": "Update",
        "version_info": "Status: {type}\nVersion: {old} -> {new}",
        "changelog_label": "Changelog",
        "quota_title": "H@H Daily Quota Reminder",
        "quota_body": "Current Free Archive Quota:\n{quota}",
        "status_change": "Status Change",
        "status_report": "Status Report",
        "client_msg_title": "H@H {type}: {name}",
        "online": "Online",
        "offline": "Offline",
        "cur_status": "Current Status",
        "detail": "Details",
        "region": "Region",
        "address": "Address",
        "version": "Version",
        "speed": "Speed",
        "trust": "Trust",
        "quality": "Quality",
        "hitrate": "Hitrate",
        "hathrate": "Hathrate",
        "served": "Served",
        "last_seen": "Last Seen"
    },
    "es": {
        "official": "Versión Oficial Java",
        "rust": "hath-rust",
        "web": "Web H@H",
        "new_version_found": "Nueva versión de H@H {label}: v{ver}",
        "update_type_new": "Nueva",
        "update_type_update": "Actualización",
        "version_info": "Estado: {type}\nVersión: {old} -> {new}",
        "changelog_label": "Registro de cambios",
        "quota_title": "Recordatorio de cuota diaria H@H",
        "quota_body": "Cuota de archivo gratuita actual:\n{quota}",
        "status_change": "Cambio de estado",
        "status_report": "Informe de estado",
        "client_msg_title": "H@H {type}: {name}",
        "online": "En línea",
        "offline": "Desconectado",
        "cur_status": "Estado actual",
        "detail": "Detalles",
        "region": "Región",
        "address": "Dirección",
        "version": "Versión",
        "speed": "Ancho de banda",
        "trust": "Confianza",
        "quality": "Calidad",
        "hitrate": "Tasa de aciertos",
        "hathrate": "Tasa Hath",
        "served": "Servido",
        "last_seen": "Última vez visto"
    },
    "fr": {
        "official": "Version Officielle Java",
        "rust": "hath-rust",
        "web": "Web H@H",
        "new_version_found": "Nouvelle version H@H {label} : v{ver}",
        "update_type_new": "Nouveau",
        "update_type_update": "Mise à jour",
        "version_info": "Statut : {type}\nVersion : {old} -> {new}",
        "changelog_label": "Journal des modifications",
        "quota_title": "Rappel de quota quotidien H@H",
        "quota_body": "Quota d'archive gratuit actuel :\n{quota}",
        "status_change": "Changement d'état",
        "status_report": "Rapport d'état",
        "client_msg_title": "H@H {type} : {name}",
        "online": "En ligne",
        "offline": "Hors ligne",
        "cur_status": "Statut actuel",
        "detail": "Détails",
        "region": "Région",
        "address": "Adresse",
        "version": "Version",
        "speed": "Bande passante",
        "trust": "Confiance",
        "quality": "Qualité",
        "hitrate": "Taux de réussite",
        "hathrate": "Taux Hath",
        "served": "Servi",
        "last_seen": "Dernière vue"
    },
    "ru": {
        "official": "Официальная Java версия",
        "rust": "hath-rust",
        "web": "H@H веб-интерфейс",
        "new_version_found": "Новая версия H@H {label}: v{ver}",
        "update_type_new": "Новое",
        "update_type_update": "Обновление",
        "version_info": "Статус: {type}\nВерсия: {old} -> {new}",
        "changelog_label": "Список изменений",
        "quota_title": "Ежедневная квота H@H",
        "quota_body": "Текущая бесплатная квота архива:\n{quota}",
        "status_change": "Изменение статуса",
        "status_report": "Отчет о статусе",
        "client_msg_title": "H@H {type}: {name}",
        "online": "В сети",
        "offline": "Вне сети",
        "cur_status": "Текущий статус",
        "detail": "Подробности",
        "region": "Регион",
        "address": "Адрес",
        "version": "Версия",
        "speed": "Скорость",
        "trust": "Доверие",
        "quality": "Качество",
        "hitrate": "Частота запросов",
        "hathrate": "Скорость Hath",
        "served": "Обслужено",
        "last_seen": "Последний раз в сети"
    },
    "de": {
        "official": "Offizielle Java-Version",
        "rust": "hath-rust",
        "web": "H@H Webseite",
        "new_version_found": "Neue H@H {label} Version: v{ver}",
        "update_type_new": "Neu",
        "update_type_update": "Update",
        "version_info": "Status: {type}\nVersion: {old} -> {new}",
        "changelog_label": "Änderungsprotokoll",
        "quota_title": "H@H Tägliche Quoten-Erinnerung",
        "quota_body": "Aktuelle kostenlose Archivquote:\n{quota}",
        "status_change": "Statusänderung",
        "status_report": "Statusbericht",
        "client_msg_title": "H@H {type}: {name}",
        "online": "Online",
        "offline": "Offline",
        "cur_status": "Aktueller Status",
        "detail": "Details",
        "region": "Region",
        "address": "Adresse",
        "version": "Version",
        "speed": "Bandbreite",
        "trust": "Vertrauen",
        "quality": "Qualität",
        "hitrate": "Trefferquote",
        "hathrate": "Hath-Rate",
        "served": "Bedient",
        "last_seen": "Zuletzt gesehen"
    },
    "ja": {
        "official": "公式 Java 版",
        "rust": "hath-rust",
        "web": "H@H ウェブ版",
        "new_version_found": "H@H {label} 新バージョン: v{ver}",
        "update_type_new": "新発見",
        "update_type_update": "更新",
        "version_info": "状態: {type}\nバージョン: {old} -> {new}",
        "changelog_label": "変更履歴",
        "quota_title": "H@H 毎日のクォータ通知",
        "quota_body": "現在の無料アーカイブクォータ:\n{quota}",
        "status_change": "ステータス変更",
        "status_report": "ステータスレポート",
        "client_msg_title": "H@H {type}: {name}",
        "online": "オンライン",
        "offline": "オフライン",
        "cur_status": "現在のステータス",
        "detail": "詳細",
        "region": "地域",
        "address": "アドレス",
        "version": "バージョン",
        "speed": "帯域幅",
        "trust": "信頼",
        "quality": "品質",
        "hitrate": "ヒット率",
        "hathrate": "Hathレート",
        "served": "転送済み",
        "last_seen": "最終確認"
    },
    "ko": {
        "official": "공식 Java 버전",
        "rust": "hath-rust",
        "web": "H@H 웹 버전",
        "new_version_found": "H@H {label} 새 버전: v{ver}",
        "update_type_new": "새 발견",
        "update_type_update": "업데이트",
        "version_info": "상태: {type}\n버전: {old} -> {new}",
        "changelog_label": "변경 로그",
        "quota_title": "H@H 일일 쿼터 알림",
        "quota_body": "현재 무료 아카이브 쿼터:\n{quota}",
        "status_change": "상태 변경",
        "status_report": "상태 보고",
        "client_msg_title": "H@H {type}: {name}",
        "online": "온라인",
        "offline": "오프라인",
        "cur_status": "현재 상태",
        "detail": "상세",
        "region": "지역",
        "address": "주소",
        "version": "버전",
        "speed": "대역폭",
        "trust": "신뢰",
        "quality": "품질",
        "hitrate": "히트레이트",
        "hathrate": "Hath레이트",
        "served": "전송됨",
        "last_seen": "마지막 확인"
    },
    "ar": {
        "official": "نسخة جافا الرسمية",
        "rust": "hath-rust",
        "web": "صفحة ويب H@H",
        "new_version_found": "إصدار جديد من H@H {label}: v{ver}",
        "update_type_new": "جديد",
        "update_type_update": "تحديث",
        "version_info": "الحالة: {type}\nالإصدار: {old} -> {new}",
        "changelog_label": "سجل التغييرات",
        "quota_title": "تذكير بحصة H@H اليومية",
        "quota_body": "حصة الأرشيف المجانية الحالية:\n{quota}",
        "status_change": "تغيير الحالة",
        "status_report": "تقرير الحالة",
        "client_msg_title": "H@H {type}: {name}",
        "online": "متصل",
        "offline": "غير متصل",
        "cur_status": "الحالة الحالية",
        "detail": "التفاصيل",
        "region": "المنطقة",
        "address": "العنوان",
        "version": "الإصدار",
        "speed": "عرض النطاق الترددي",
        "trust": "الثقة",
        "quality": "الجودة",
        "hitrate": "معدل الإصابة",
        "hathrate": "معدل Hath",
        "served": "تم تقديمه",
        "last_seen": "آخر ظهور"
    },
    "he": {
        "official": "גרסת ג'אווה רשמית",
        "rust": "hath-rust",
        "web": "דף אינטרנט H@H",
        "new_version_found": "גרסה חדשה של H@H {label}: v{ver}",
        "update_type_new": "חדש",
        "update_type_update": "עדכון",
        "version_info": "סטטוס: {type}\nגרסה: {old} -> {new}",
        "changelog_label": "יומן שינויים",
        "quota_title": "תזכורת מכסה יומית של H@H",
        "quota_body": "מכסת ארכיון חינמית נוכחית:\n{quota}",
        "status_change": "שינוי סטטוס",
        "status_report": "דיווח סטטוס",
        "client_msg_title": "H@H {type}: {name}",
        "online": "מחובר",
        "offline": "מנותק",
        "cur_status": "סטטוס נוכחי",
        "detail": "פרטים",
        "region": "אזור",
        "address": "כתובת",
        "version": "גרסה",
        "speed": "רוחב פס",
        "trust": "אמון",
        "quality": "איכות",
        "hitrate": "שיעור פגיעה",
        "hathrate": "שיעור Hath",
        "served": "הוגש",
        "last_seen": "נראה לאחרונה"
    }
}

DEFAULT_CONFIG_TEXT = """# ==========================================================
# Hentai@Home 版本与状态监控器 配置文件
# ==========================================================

[monitor]
# 检查间隔（分钟），推荐 5-10 分钟
check_interval_minutes = 5

# 启用检查项
check_official = true        # 监控官方 Java 客户端 (repo.e-hentai.org)
check_rust = true            # 监控 hath-rust (GitHub Releases)
check_ehpage = true          # 监控 E-Hentai H@H 管理页面 (需 Cookies)
check_quota = true           # 每天推送一次免费配额数值
check_clients = true         # 监控所有 H@H 客户端的状态 (在线/离线)

# E-Hentai cookies (check_ehpage = true 时需要)
# 请在浏览器中登录后获取 ipb_member_id 和 ipb_pass_hash
eh_ipb_member_id = ""
eh_ipb_pass_hash = ""

# GitHub Token (可选，用于提高 API 调用限制)
github_token = ""

# 本地代理 (可选，支持 http://user:pass@host:port)
proxy = ""

[notify]
# 推送语言 (支持: zh, zh-hant, en, ja, ko, es, fr, ru, de, ar, he)
language = "zh"

# 推送分组名称 (默认: H@H)
group = "H@H"

# ---- Bark (iOS 推送) ----
bark_url = ""
bark_sound = "minuet"

# ---- Telegram Bot ----
telegram_bot_token = ""
telegram_chat_id = ""

# ---- PushPlus ----
pushplus_token = ""

# ---- PushDeer ----
pushdeer_key = ""

# ---- DingTalk (钉钉机器人) ----
dingtalk_access_token = ""

# ---- Discord (Webhook) ----
discord_webhook = ""

# ---- Slack (Webhook) ----
slack_webhook = ""

# ---- Gotify ----
gotify_url = ""
gotify_token = ""

# ---- Matrix ----
matrix_url = ""
matrix_token = ""
matrix_room_id = ""

# ---- Pushover ----
pushover_user_key = ""
pushover_api_token = ""

# ---- 通用 Webhooks (支持多个，POST JSON {"title": "...", "body": "..."}) ----
webhooks = []

[system]
# 数据库路径 (可选，默认为同目录下的 hath_monitor.db)
db_path = ""
# 用户代理 (User-Agent)
user_agent = ""
# 是否验证 SSL 证书 (默认 false，提高某些环境下的兼容性)
verify_ssl = false
"""

def get_t(lang, key, **kwargs):
    translations = I18N.get(lang, I18N["zh"])
    text = translations.get(key, I18N["zh"].get(key, key))
    return text.format(**kwargs) if kwargs else text

def request(url, cfg=None, data=None, headers=None, method=None, timeout=10):
    scfg = (cfg or {}).get("system", {})
    ua = scfg.get("user_agent") or UA_DEFAULT
    headers = {"User-Agent": ua, **(headers or {})}
    
    if data:
        if isinstance(data, dict):
            data = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
        elif isinstance(data, str):
            data = data.encode()
    
    ctx = ssl.create_default_context()
    if not scfg.get("verify_ssl", False):
        ctx.check_hostname, ctx.verify_mode = False, ssl.CERT_NONE
    
    handlers = [urllib.request.HTTPSHandler(context=ctx)]
    mcfg = (cfg or {}).get("monitor", {})
    if mcfg.get("proxy"):
        proxy_url = mcfg["proxy"]
        handlers.append(urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url}))
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.build_opener(*handlers).open(req, timeout=timeout) as r:
            return r.read() if method != "HEAD" else True
    except Exception as e:
        if method != "HEAD": logger.debug("请求 %s 失败: %s", url, e)
        return None if method != "HEAD" else False

def init_db(db_path):
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS v (id INTEGER PRIMARY KEY, src TEXT, ver TEXT, extra TEXT, ts TEXT)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sv ON v(src, ver)")

def check_official(cfg, db_path):
    logger.info("🔍 检查官方 Java 客户端版本...")
    base = "https://repo.e-hentai.org/hath/HentaiAtHome_{v}.zip"
    with sqlite3.connect(db_path) as conn:
        last = conn.execute("SELECT ver FROM v WHERE src = 'official' ORDER BY id DESC LIMIT 1").fetchone()
    best = last[0] if last else "1.6.5"
    v_tuple = tuple(int(x) for x in best.split("."))
    
    for p in range(v_tuple[2], v_tuple[2] + 10):
        cand = f"{v_tuple[0]}.{v_tuple[1]}.{p}"
        if request(base.format(v=cand), {"monitor": cfg}, method="HEAD"): best = cand
        else: break
    return best, base.format(v=best)

def check_rust(cfg):
    logger.info("🔍 检查 hath-rust 版本...")
    headers = {}
    if cfg.get("github_token"):
        headers["Authorization"] = f"token {cfg['github_token']}"
    res = request("https://api.github.com/repos/james58899/hath-rust/releases/latest", {"monitor": cfg}, headers=headers)
    if not res: return None
    data = json.loads(res)
    return data["tag_name"].lstrip("v"), data["html_url"], data.get("body", "")[:500]

def check_hath_page(cfg):
    if not cfg.get("eh_ipb_member_id"): return None
    logger.info("🔍 正在抓取 EH H@H 管理页面...")
    cookie = f"ipb_member_id={cfg['eh_ipb_member_id']}; ipb_pass_hash={cfg['eh_ipb_pass_hash']}"
    res = request("https://e-hentai.org/hentaiathome.php", {"monitor": cfg}, headers={"Cookie": cookie})
    if not res: return None
    text = res.decode(errors="ignore")
    
    data = {}
    # 版本号
    m = re.search(r"Hentai(?:At|@)Home[\s_]+v?(\d+\.\d+\.\d+)", text)
    if m: data["version"] = m.group(1)
    
    # 免费配额
    m = re.search(r"Free Archive Quota:\s*<strong>(.*?)</strong>", text)
    if m: data["quota"] = m.group(1)
    
    # 客户端列表
    clients = []
    hct_m = re.search(r'<table id="hct">.*?</table>', text, re.DOTALL)
    if hct_m:
        hct_html = hct_m.group(0)
        rows = re.findall(r'<tr>(.*?)</tr>', hct_html, re.DOTALL)[1:] # 跳过表头
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cells) >= 15:
                name = re.sub(r'<[^>]+>', '', cells[0]).strip()
                cid = cells[1].strip()
                status_raw = re.sub(r'<[^>]+>', '', cells[2]).strip()
                
                status_lower = status_raw.lower()
                if "online" in status_lower:
                    status_key = "online"
                elif "offline" in status_lower:
                    status_key = "offline"
                else:
                    status_key = status_raw
                
                clients.append({
                    "id": cid,
                    "name": name,
                    "status_key": status_key,
                    "created": cells[3].strip(),
                    "last_seen": cells[4].strip(),
                    "files_served": cells[5].strip(),
                    "ip": cells[6].strip(),
                    "port": cells[7].strip(),
                    "version": cells[8].strip(),
                    "max_speed": cells[9].strip(),
                    "trust": re.sub(r'<[^>]+>', '', cells[10]).strip(),
                    "quality": cells[11].strip(),
                    "hitrate": cells[12].strip(),
                    "hathrate": cells[13].strip(),
                    "region": cells[14].strip()
                })
    if clients: data["clients"] = clients
        
    return data

def get_changelog(ver, cfg):
    cookie = f"ipb_member_id={cfg.get('eh_ipb_member_id', '')}; ipb_pass_hash={cfg.get('eh_ipb_pass_hash', '')}"
    res = request("https://forums.e-hentai.org/index.php?showtopic=234458&view=getlastpost", {"monitor": cfg}, headers={"Cookie": cookie})
    if not res: return None
    text = html.unescape(re.sub(r'<[^>]+>', '', re.sub(r'<br\s*/?>|</p>|</div>', '\n', res.decode(errors="ignore"))))
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for i, l in enumerate(lines):
        if ver in l:
            cl = []
            for j in range(i + 1, min(i + 15, len(lines))):
                if any(x in lines[j] for x in ["Edited by", "Quote", "Hentai@Home"]): break
                cl.append(lines[j])
            return "\n".join(cl) if cl else None
    return None

def send_notify(ncfg, title, body):
    logger.info("📢 发送通知: %s", title)
    group = ncfg.get("group") or ncfg.get("bark_group") or "H@H"
    
    # Bark
    if ncfg.get("bark_url"):
        request(ncfg.get("bark_url").rstrip("/"), data={"title": title, "body": body, "group": group, "sound": ncfg.get("bark_sound", "minuet")})
    
    # Telegram
    if ncfg.get("telegram_bot_token"):
        tg_text = f"<b>{title}</b>\n\n{body}"
        request(f"https://api.telegram.org/bot{ncfg['telegram_bot_token']}/sendMessage", 
                data={"chat_id": ncfg["telegram_chat_id"], "text": tg_text, "parse_mode": "HTML"})
    
    # PushPlus
    if ncfg.get("pushplus_token"):
        request("https://www.pushplus.plus/send", data={"token": ncfg["pushplus_token"], "title": title, "content": body.replace("\n", "<br/>"), "template": "html"})

    # PushDeer
    if ncfg.get("pushdeer_key"):
        request(f"https://api2.pushdeer.com/message/push?pushkey={ncfg['pushdeer_key']}&text={urllib.parse.quote(title)}&desp={urllib.parse.quote(body)}")
        
    # DingTalk
    if ncfg.get("dingtalk_access_token"):
        request(f"https://oapi.dingtalk.com/robot/send?access_token={ncfg['dingtalk_access_token']}", 
                data={"msgtype": "text", "text": {"content": f"{title}\n\n{body}"}})
    
    # Discord
    if ncfg.get("discord_webhook"):
        color = 3066993 if any(s in body for s in ["在线", "Online", "En ligne", "В сети", "オンライン", "온라인", "متصل", "מחובר"]) else (15158332 if any(s in body for s in ["离线", "Offline", "Hors ligne", "Вне сети", "オフライン", "오프라인", "غير متصل", "מנותק"]) else 3447003)
        request(ncfg.get("discord_webhook"), data={
            "embeds": [{
                "title": title,
                "description": body,
                "color": color,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }]
        })

    # Slack
    if ncfg.get("slack_webhook"):
        request(ncfg.get("slack_webhook"), data={"text": f"*{title}*\n{body}"})

    # Gotify
    if ncfg.get("gotify_url") and ncfg.get("gotify_token"):
        url = f"{ncfg['gotify_url'].rstrip('/')}/message?token={ncfg['gotify_token']}"
        request(url, data={"title": title, "message": body, "priority": 5})

    # Matrix
    if ncfg.get("matrix_url") and ncfg.get("matrix_token") and ncfg.get("matrix_room_id"):
        url = f"{ncfg['matrix_url'].rstrip('/')}/_matrix/client/r0/rooms/{ncfg['matrix_room_id']}/send/m.room.message?access_token={ncfg['matrix_token']}"
        request(url, data={"msgtype": "m.text", "body": f"{title}\n\n{body}"})

    # Pushover
    if ncfg.get("pushover_user_key") and ncfg.get("pushover_api_token"):
        request("https://api.pushover.net/1/messages.json", data=urllib.parse.urlencode({
            "token": ncfg["pushover_api_token"],
            "user": ncfg["pushover_user_key"],
            "title": title,
            "message": body
        }).encode())
        
    # Generic Webhooks
    for url in ncfg.get("webhooks", []):
        request(url, data={"title": title, "body": body})

def run_check(config, force_push=False):
    mcfg, ncfg = config.get("monitor", {}), config.get("notify", {})
    scfg = config.get("system", {})
    db_path = scfg.get("db_path") or DB_PATH_DEFAULT
    lang = ncfg.get("language", "zh")
    
    init_db(db_path)
    now_iso = datetime.now(timezone.utc).isoformat()
    
    with sqlite3.connect(db_path) as conn:
        # 1. 软件版本检查
        for src, func, label_key in [("official", check_official, "official"), ("rust", check_rust, "rust")]:
            if not mcfg.get(f"check_{src}"): continue
            
            try:
                res = func(mcfg, db_path) if src == "official" else func(mcfg)
                if not res: continue
                ver, *rest = res if isinstance(res, tuple) else (res,)
                last = conn.execute("SELECT ver FROM v WHERE src = ? ORDER BY id DESC LIMIT 1", (src,)).fetchone()
                
                if force_push or not last or last[0] != ver:
                    extra = {"url": rest[0] if len(rest) > 0 else "", "changelog": rest[1] if len(rest) > 1 else ""}
                    if not force_push:
                        conn.execute("INSERT INTO v (src, ver, extra, ts) VALUES (?, ?, ?, ?)", (src, ver, json.dumps(extra), now_iso))
                    
                    label = get_t(lang, label_key)
                    title = get_t(lang, "new_version_found", label=label, ver=ver)
                    update_type = get_t(lang, "update_type_update" if last else "update_type_new")
                    body = get_t(lang, "version_info", type=update_type, old=last[0] if last else "?", new=ver)
                    
                    if extra.get("changelog"):
                        body += f"\n\n{get_t(lang, 'changelog_label')}:\n{extra['changelog']}"
                    send_notify(ncfg, title, body)
            except Exception as e:
                logger.error("检查 %s 异常: %s", src, e)

        # 2. EH 管理页面检查
        if mcfg.get("check_ehpage"):
            try:
                data = check_hath_page(mcfg)
            except Exception as e:
                logger.error("抓取 EH 管理页面异常: %s", e)
                data = None
            if data:
                # 页面版本号
                if "version" in data:
                    ver = data["version"]
                    last = conn.execute("SELECT ver FROM v WHERE src = 'ehpage' ORDER BY id DESC LIMIT 1").fetchone()
                    if force_push or not last or last[0] != ver:
                        extra = {"changelog": get_changelog(ver, mcfg)}
                        if not force_push:
                            conn.execute("INSERT INTO v (src, ver, extra, ts) VALUES ('ehpage', ?, ?, ?)", (ver, json.dumps(extra), now_iso))
                        
                        label = get_t(lang, "web")
                        title = get_t(lang, "new_version_found", label=label, ver=ver)
                        body = get_t(lang, "version_info", type=get_t(lang, "update_type_update"), old=last[0] if last else "?", new=ver)
                        send_notify(ncfg, title, body)
                
                # 免费配额 (每日推送)
                if mcfg.get("check_quota") and "quota" in data:
                    quota = data["quota"]
                    last_q = conn.execute("SELECT ts, ver FROM v WHERE src = 'quota' ORDER BY id DESC LIMIT 1").fetchone()
                    is_new_day = not last_q or datetime.fromisoformat(last_q[0]).date() < datetime.now(timezone.utc).date()
                    if force_push or is_new_day:
                        if not force_push:
                            conn.execute("INSERT INTO v (src, ver, extra, ts) VALUES ('quota', ?, '', ?)", (quota, now_iso))
                        title = get_t(lang, "quota_title")
                        body = get_t(lang, "quota_body", quota=quota)
                        send_notify(ncfg, title, body)
                
                # 客户端状态检查 (详细信息推送)
                if mcfg.get("check_clients") and "clients" in data:
                    for client in data["clients"]:
                        cid, name, status_key = client["id"], client["name"], client["status_key"]
                        src_name = f"client_{cid}"
                        last_s = conn.execute("SELECT ver FROM v WHERE src = ? ORDER BY id DESC LIMIT 1", (src_name,)).fetchone()
                        
                        if force_push or not last_s or last_s[0] != status_key:
                            if not force_push:
                                conn.execute("INSERT INTO v (src, ver, extra, ts) VALUES (?, ?, ?, ?)", (src_name, status_key, name, now_iso))
                            
                            is_change = last_s and last_s[0] != status_key
                            type_label = get_t(lang, "status_change" if is_change else "status_report")
                            title = get_t(lang, "client_msg_title", type=type_label, name=name)
                            
                            status_now = get_t(lang, status_key)
                            if is_change:
                                status_detail = f"{get_t(lang, last_s[0])} ➔ {status_now}"
                            else:
                                status_detail = f"{status_now}"
                            
                            body = (
                                f"{get_t(lang, 'cur_status')}: {status_now} (ID: {cid})\n"
                                f"{get_t(lang, 'detail')}: {status_detail}\n"
                                f"{get_t(lang, 'region')}: {client.get('region')}\n"
                                f"{get_t(lang, 'address')}: {client.get('ip')}:{client.get('port')}\n"
                                f"{get_t(lang, 'version')}: {client.get('version')}\n"
                                f"{get_t(lang, 'speed')}: {client.get('max_speed')}\n"
                                f"{get_t(lang, 'trust')}: {client.get('trust')}\n"
                                f"{get_t(lang, 'quality')}: {client.get('quality')}\n"
                                f"{get_t(lang, 'hitrate')}: {client.get('hitrate')}\n"
                                f"{get_t(lang, 'hathrate')}: {client.get('hathrate')}\n"
                                f"{get_t(lang, 'served')}: {client.get('files_served')}\n"
                                f"{get_t(lang, 'last_seen')}: {client.get('last_seen')}"
                            )
                            send_notify(ncfg, title, body)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--daemon", action="store_true", help="以守护进程模式运行")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细调试信息")
    parser.add_argument("--history", action="store_true", help="查看最近监控记录")
    parser.add_argument("--push-all", action="store_true", help="强制全量推送当前状态")
    parser.add_argument("--config", help="指定配置文件路径")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="[%(asctime)s] %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    cfg_path = Path(args.config) if args.config else CONFIG_PATH
    if not cfg_path.exists():
        logger.info("配置文件 %s 不存在，正在创建默认配置模板...", cfg_path)
        with open(cfg_path, "w", encoding="utf-8") as f:
            f.write(DEFAULT_CONFIG_TEXT)
        logger.info("已创建 %s，请编辑并配置相关参数。", cfg_path)
        return

    with open(cfg_path, "rb") as f: config = tomllib.load(f)

    scfg = config.get("system", {})
    db_path = scfg.get("db_path") or DB_PATH_DEFAULT

    if args.history:
        with sqlite3.connect(db_path) as conn:
            for r in conn.execute("SELECT src, ver, ts FROM v ORDER BY id DESC LIMIT 20"): print(r)
        return

    if args.push_all:
        logger.info("🚀 正在执行全量状态推送...")
        run_check(config, force_push=True)
        return

    if args.daemon:
        logger.info("🚀 守护进程启动，检查间隔: %d 分钟", config['monitor'].get('check_interval_minutes', 30))
        while True:
            try: run_check(config)
            except Exception: logger.exception("循环运行出错")
            time.sleep(config['monitor'].get('check_interval_minutes', 30) * 60)
    else:
        run_check(config)

if __name__ == "__main__":
    main()
