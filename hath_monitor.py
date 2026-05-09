#!/usr/bin/env python3
import argparse, json, logging, sys, time, ssl, os
import urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

# --- 1. CONFIGURATION ---
def load_config():
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    k, *v = line.strip().split("=", 1)
                    if v: os.environ[k] = v[0]
    return {
        "monitor": {
            "check_interval_minutes": int(os.getenv("CHECK_INTERVAL_MINUTES", 10)),
            "check_official": os.getenv("CHECK_OFFICIAL", "true").lower() == "true",
            "check_rust": os.getenv("CHECK_RUST", "true").lower() == "true",
            "check_ehpage": os.getenv("CHECK_EHPAGE", "true").lower() == "true",
            "check_quota": os.getenv("CHECK_QUOTA", "true").lower() == "true",
            "check_clients": os.getenv("CHECK_CLIENTS", "true").lower() == "true",
            "eh_ipb_member_id": os.getenv("EH_IPB_MEMBER_ID", ""),
            "eh_ipb_pass_hash": os.getenv("EH_IPB_PASS_HASH", ""),
            "github_token": os.getenv("GITHUB_TOKEN", ""),
            "proxy": os.getenv("PROXY", ""),
        },
        "notify": {
            "language": os.getenv("LANGUAGE", "zh"),
            "group": os.getenv("NOTIFY_GROUP", "H@H"),
            "bark_url": os.getenv("BARK_URL", ""),
            "bark_sound": os.getenv("BARK_SOUND", "minuet"),
            "telegram_bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
            "telegram_chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
            "pushplus_token": os.getenv("PUSHPLUS_TOKEN", ""),
            "pushdeer_key": os.getenv("PUSHDEER_KEY", ""),
            "dingtalk_access_token": os.getenv("DINGTALK_ACCESS_TOKEN", ""),
            "discord_webhook": os.getenv("DISCORD_WEBHOOK", ""),
            "slack_webhook": os.getenv("SLACK_WEBHOOK", ""),
            "gotify_url": os.getenv("GOTIFY_URL", ""),
            "gotify_token": os.getenv("GOTIFY_TOKEN", ""),
            "matrix_url": os.getenv("MATRIX_URL", ""),
            "matrix_token": os.getenv("MATRIX_TOKEN", ""),
            "matrix_room_id": os.getenv("MATRIX_ROOM_ID", ""),
            "pushover_user_key": os.getenv("PUSHOVER_USER_KEY", ""),
            "pushover_api_token": os.getenv("PUSHOVER_API_TOKEN", ""),
            "webhooks": os.getenv("WEBHOOKS", "").split(",") if os.getenv("WEBHOOKS") else [],
        },
        "system": {
            "db_path": os.getenv("DB_PATH", ""),
            "verify_ssl": os.getenv("VERIFY_SSL", "false").lower() == "true",
        }
    }

APP_NAME, VERSION = "hath-monitor", "1.6.0"
BASE_DIR = Path(__file__).resolve().parent

class Translator:
    def __init__(self, data, lang="zh"):
        self._d = data.get(lang, data.get("en", data.get("zh", {})))
        self.lang = lang
    def __call__(self, k, **kw):
        t = self._d.get(k, k)
        return t.format(**kw) if kw else t
    def __getattr__(self, k): return self._d.get(k, k)

_ = None # Global translator

DB_PATH_DEFAULT = BASE_DIR / "hath_monitor.db"
UA_DEFAULT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
logger = logging.getLogger(APP_NAME)

# --- 2. CORE UTILS ---
def request(url, cfg=None, headers=None, data=None, method="GET", timeout=30):
    import urllib.parse
    handlers = []
    p = (cfg.get("monitor", {}) if cfg else {}).get("proxy")
    if p: handlers.append(urllib.request.ProxyHandler({'http': p, 'https': p}))
    if not (cfg.get("system", {}) if cfg else {}).get("verify_ssl", False):
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname, ctx.verify_mode = False, ssl.CERT_NONE
        handlers.append(urllib.request.HTTPSHandler(context=ctx))
    if data and isinstance(data, dict):
        data = json.dumps(data).encode()
        headers = headers or {}
        if "Content-Type" not in headers: headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers or {"User-Agent": UA_DEFAULT}, method=method)
    try:
        with urllib.request.build_opener(*handlers).open(req, timeout=timeout) as r:
            return r.read() if method != "HEAD" else True
    except Exception as e:
        if method != "HEAD": logger.debug("Request failed: %s", e)
        return None if method != "HEAD" else False

# --- 3. CHECK MODULES ---
def check_official(cfg, db_path):
    import sqlite3
    logger.info("🔍 检查官方 Java 客户端...")
    u = "https://repo.e-hentai.org/hath/HentaiAtHome_{v}.zip"
    with sqlite3.connect(db_path) as conn:
        r = conn.execute("SELECT ver FROM v WHERE src='official' ORDER BY id DESC LIMIT 1").fetchone()
    v = r[0] if r else "1.6.5"
    vt = tuple(int(x) for x in v.split("."))
    for p in range(vt[2], vt[2]+5):
        c = f"{vt[0]}.{vt[1]}.{p}"
        if request(u.format(v=c), {"monitor": cfg}, method="HEAD"): v = c
        else: break
    return v, u.format(v=v)

def check_rust(cfg):
    logger.info("🔍 检查 hath-rust...")
    h = {"User-Agent": UA_DEFAULT}
    if cfg.get("github_token"): h["Authorization"] = f"token {cfg['github_token']}"
    res = request("https://api.github.com/repos/james58899/hath-rust/releases/latest", {"monitor": cfg}, headers=h)
    if not res: return None
    d = json.loads(res)
    return d["tag_name"].lstrip("v"), d["html_url"], d.get("body", "")[:500]

def check_hath_page(cfg):
    import re
    if not cfg.get("eh_ipb_member_id"): return None
    logger.info("🔍 抓取 EH H@H 页面...")
    ck = f"ipb_member_id={cfg['eh_ipb_member_id']}; ipb_pass_hash={cfg['eh_ipb_pass_hash']}"
    res = request("https://e-hentai.org/hentaiathome.php", {"monitor": cfg}, headers={"Cookie": ck, "User-Agent": UA_DEFAULT})
    if not res: return None
    t = res.decode(errors="ignore")
    data = {}
    m = re.search(r"Hentai(?:At|@)Home[\s_]+v?(\d+\.\d+\.\d+)", t)
    if m: data["version"] = m.group(1)
    m = re.search(r"Free Archive Quota:\s*<strong>(.*?)</strong>", t)
    if m: data["quota"] = m.group(1)
    hct = re.search(r'<table id="hct">.*?</table>', t, re.DOTALL)
    if hct:
        cls = []
        for r in re.findall(r'<tr>(.*?)</tr>', hct.group(0), re.DOTALL)[1:]:
            cs = re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL)
            if len(cs) >= 15:
                st = re.sub(r'<[^>]+>', '', cs[2]).strip().lower()
                cls.append({
                    "id": cs[1].strip(), "name": re.sub(r'<[^>]+>', '', cs[0]).strip(),
                    "status_key": "online" if "online" in st else ("offline" if "offline" in st else st),
                    "ip": cs[3].strip(), "port": cs[4].strip(), "version": cs[5].strip(),
                    "max_speed": cs[9].strip(), "trust": re.sub(r'<[^>]+>', '', cs[10]).strip(),
                    "quality": cs[11].strip(), "hitrate": cs[12].strip(), "hathrate": cs[13].strip(), "region": cs[14].strip()
                })
        data["clients"] = cls
    return data

def get_changelog(ver, cfg):
    import re, html
    logger.info("🔍 获取更新日志...")
    ck = f"ipb_member_id={cfg['eh_ipb_member_id']}; ipb_pass_hash={cfg['eh_ipb_pass_hash']}"
    u = "https://forums.e-hentai.org/index.php?showtopic=234458&view=getlastpost"
    res = request(u, {"monitor": cfg}, headers={"Cookie": ck, "User-Agent": UA_DEFAULT})
    if not res: return None
    t = html.unescape(re.sub(r'<[^>]+>', '', re.sub(r'<br\s*/?>|</div>', '\n', res.decode(errors="ignore"))))
    ls = [l.strip() for l in t.split('\n') if l.strip()]
    for i, l in enumerate(ls):
        if ver in l:
            cl = []
            for j in range(i+1, min(i+15, len(ls))):
                if any(x in ls[j] for x in ["Edited by", "Quote", "Hentai@Home"]): break
                cl.append(ls[j])
            return "\n".join(cl)
    return None

def send_notify(ncfg, title, body):
    import urllib.parse
    logger.info("📢 通知: %s", title)
    g = ncfg.get("group", "H@H")
    if ncfg.get("bark_url"): request(ncfg["bark_url"].rstrip("/"), data={"title": title, "body": body, "group": g, "sound": ncfg.get("bark_sound", "minuet")})
    if ncfg.get("telegram_bot_token"): request(f"https://api.telegram.org/bot{ncfg['telegram_bot_token']}/sendMessage", data={"chat_id": ncfg["telegram_chat_id"], "text": f"<b>{title}</b>\n\n{body}", "parse_mode": "HTML"})
    if ncfg.get("pushplus_token"): request("https://www.pushplus.plus/send", data={"token": ncfg["pushplus_token"], "title": title, "content": body.replace("\n", "<br/>"), "template": "html"})
    if ncfg.get("pushdeer_key"): request(f"https://api2.pushdeer.com/message/push?pushkey={ncfg['pushdeer_key']}&text={urllib.parse.quote(title)}&desp={urllib.parse.quote(body)}")
    if ncfg.get("discord_webhook"): request(ncfg["discord_webhook"], data={"embeds": [{"title": title, "description": body, "color": 3066993 if "在线" in body or "Online" in body else 3447003, "timestamp": datetime.now(timezone.utc).isoformat()}]})
    if ncfg.get("pushover_user_key"): request("https://api.pushover.net/1/messages.json", data=urllib.parse.urlencode({"token": ncfg["pushover_api_token"], "user": ncfg["pushover_user_key"], "title": title, "message": body}).encode())
    for u in ncfg.get("webhooks", []): request(u, data={"title": title, "body": body})

def run_check(config, force_push=False):
    import sqlite3
    mcfg, ncfg = config["monitor"], config["notify"]
    db = config["system"]["db_path"] or DB_PATH_DEFAULT
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS v (id INTEGER PRIMARY KEY, src TEXT, ver TEXT, ts TEXT)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sv ON v(src, ver)")
    now = datetime.now(timezone.utc).isoformat()
    try:
        with sqlite3.connect(db) as conn:
            for s, f, l in [("official", check_official, "official"), ("rust", check_rust, "rust")]:
                if not mcfg.get(f"check_{s}"): continue
                res = f(mcfg, db) if s == "official" else f(mcfg)
                if not res: continue
                v, *rest = res if isinstance(res, tuple) else (res,)
                last = conn.execute("SELECT ver FROM v WHERE src=? ORDER BY id DESC LIMIT 1", (s,)).fetchone()
                if force_push or not last or last[0] != v:
                    if not force_push: conn.execute("INSERT INTO v (src, ver, ts) VALUES (?, ?, ?)", (s, v, now))
                    body = _("version_info", type=_("update_type_update" if last else "update_type_new"), old=last[0] if last else "?", new=v)
                    if len(rest) > 1 and rest[1]: body += f"\n\n{_.changelog_label}:\n{rest[1]}"
                    send_notify(ncfg, _("new_version_found", label=getattr(_, l), ver=v), body)
            if mcfg.get("check_ehpage"):
                d = check_hath_page(mcfg)
                if d:
                    if "version" in d:
                        v = d["version"]
                        last = conn.execute("SELECT ver FROM v WHERE src='ehpage' ORDER BY id DESC LIMIT 1").fetchone()
                        if force_push or not last or last[0] != v:
                            if not force_push: conn.execute("INSERT INTO v (src, ver, ts) VALUES ('ehpage', ?, ?)", (v, now))
                            send_notify(ncfg, _("new_version_found", label=_.web, ver=v), _("version_info", type=_.update_type_update, old=last[0] if last else "?", new=v))
                    if mcfg.get("check_quota") and "quota" in d:
                        q = d["quota"]
                        lq = conn.execute("SELECT ts FROM v WHERE src='quota' ORDER BY id DESC LIMIT 1").fetchone()
                        if force_push or not lq or datetime.fromisoformat(lq[0]).date() < datetime.now(timezone.utc).date():
                            if not force_push: conn.execute("INSERT INTO v (src, ver, ts) VALUES ('quota', ?, ?)", (q, now))
                            send_notify(ncfg, _.quota_title, _("quota_body", quota=q))
                    if mcfg.get("check_clients") and "clients" in d:
                        for c in d["clients"]:
                            sn = f"client_{c['id']}"
                            ls = conn.execute("SELECT ver FROM v WHERE src=? ORDER BY id DESC LIMIT 1", (sn,)).fetchone()
                            if force_push or not ls or ls[0] != c['status_key']:
                                if not force_push: conn.execute("INSERT INTO v (src, ver, ts) VALUES (?, ?, ?)", (sn, c['status_key'], now))
                                st_n = getattr(_, c['status_key'])
                                body = f"{_.cur_status}: {st_n}\n{_.detail}: {getattr(_, ls[0]) if ls else '?'} ➔ {st_n}\n{_.region}: {c['region']}\n{_.address}: {c['ip']}:{c['port']}\n{_.version}: {c['version']}\n{_.speed}: {c['max_speed']}\n{_.trust}: {c['trust']}\n{_.quality}: {c['quality']}\n{_.hitrate}: {c['hitrate']}\n{_.hathrate}: {c['hathrate']}"
                                send_notify(ncfg, _("client_msg_title", type=_("status_change" if ls and ls[0] != c['status_key'] else "status_report"), name=c['name']), body)
    except Exception as e: logger.exception("Run error: %s", e)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--daemon", action="store_true")
    p.add_argument("--verbose", "-v", action="store_true")
    p.add_argument("--push-all", action="store_true")
    args = p.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
    cfg = load_config()
    global _
    _ = Translator(I18N, cfg["notify"]["language"])
    if args.push_all: run_check(cfg, True)
    elif args.daemon:
        logger.info("🚀 启动 (间隔: %d 分钟)", cfg['monitor']['check_interval_minutes'])
        while True:
            run_check(cfg)
            time.sleep(cfg['monitor']['check_interval_minutes'] * 60)
    else: run_check(cfg)

I18N = {
    "zh": {
        "official": "官方 Java 版", "rust": "hath-rust", "web": "H@H 网页端",
        "new_version_found": "H@H {label} 新版本: v{ver}", "update_type_new": "新发现", "update_type_update": "更新",
        "version_info": "状态: {type}\n版本: {old} -> {new}", "changelog_label": "更新日志",
        "quota_title": "H@H 每日配额提醒", "quota_body": "当前免费存档配额:\n{quota}",
        "status_change": "状态变更", "status_report": "状态报告", "client_msg_title": "H@H {type}: {name}",
        "online": "在线", "offline": "离线", "cur_status": "当前状态", "detail": "详情",
        "region": "地区", "address": "地址", "version": "版本", "speed": "带宽",
        "trust": "信任度", "quality": "质量", "hitrate": "点击率", "hathrate": "Hath 产率",
        "served": "已传", "last_seen": "最后"
    },
    "zh-hant": {
        "official": "官方 Java 版", "rust": "hath-rust", "web": "H@H 網頁端",
        "new_version_found": "H@H {label} 新版本: v{ver}", "update_type_new": "新發現", "update_type_update": "更新",
        "version_info": "狀態: {type}\n版本: {old} -> {new}", "changelog_label": "更新日誌",
        "quota_title": "H@H 每日配額提醒", "quota_body": "當前免費存檔配額:\n{quota}",
        "status_change": "狀態變更", "status_report": "狀態報告", "client_msg_title": "H@H {type}: {name}",
        "online": "在線", "offline": "離線", "cur_status": "當前狀態", "detail": "詳情",
        "region": "地區", "address": "地址", "version": "版本", "speed": "頻寬",
        "trust": "信任度", "quality": "質量", "hitrate": "點擊率", "hathrate": "Hath 產率",
        "served": "已傳", "last_seen": "最後"
    },
    "en": {
        "official": "Official Java", "rust": "hath-rust", "web": "H@H Web",
        "new_version_found": "H@H {label} New Version: v{ver}", "update_type_new": "New", "update_type_update": "Update",
        "version_info": "Status: {type}\nVersion: {old} -> {new}", "changelog_label": "Changelog",
        "quota_title": "H@H Daily Quota Reminder", "quota_body": "Current Free Archive Quota:\n{quota}",
        "status_change": "Status Change", "status_report": "Status Report", "client_msg_title": "H@H {type}: {name}",
        "online": "Online", "offline": "Offline", "cur_status": "Current Status", "detail": "Details",
        "region": "Region", "address": "Address", "version": "Version", "speed": "Speed",
        "trust": "Trust", "quality": "Quality", "hitrate": "Hitrate", "hathrate": "Hathrate",
        "served": "Served", "last_seen": "Last Seen"
    },
    "es": {
        "official": "Versión Oficial Java", "rust": "hath-rust", "web": "Web H@H",
        "new_version_found": "Nueva versión de H@H {label}: v{ver}", "update_type_new": "Nueva", "update_type_update": "Actualización",
        "version_info": "Estado: {type}\nVersión: {old} -> {new}", "changelog_label": "Registro de cambios",
        "quota_title": "Recordatorio de cuota diaria H@H", "quota_body": "Cuota de archivo gratuita actual:\n{quota}",
        "status_change": "Cambio de estado", "status_report": "Informe de estado", "client_msg_title": "H@H {type}: {name}",
        "online": "En línea", "offline": "Desconectado", "cur_status": "Estado actual", "detail": "Detalles",
        "region": "Región", "address": "Dirección", "version": "Versión", "speed": "Ancho de banda",
        "trust": "Confianza", "quality": "Calidad", "hitrate": "Tasa de aciertos", "hathrate": "Tasa Hath",
        "served": "Servido", "last_seen": "Última vez visto"
    },
    "fr": {
        "official": "Version Officielle Java", "rust": "hath-rust", "web": "Web H@H",
        "new_version_found": "Nouvelle version H@H {label} : v{ver}", "update_type_new": "Nouveau", "update_type_update": "Mise à jour",
        "version_info": "Statut : {type}\nVersion : {old} -> {new}", "changelog_label": "Journal des modifications",
        "quota_title": "Rappel de quota quotidien H@H", "quota_body": "Quota d'archive gratuit actuel :\n{quota}",
        "status_change": "Changement d'état", "status_report": "Rapport d'état", "client_msg_title": "H@H {type} : {name}",
        "online": "En ligne", "offline": "Hors ligne", "cur_status": "Statut actuel", "detail": "Détails",
        "region": "Région", "address": "Adresse", "version": "Version", "speed": "Bande passante",
        "trust": "Confiance", "quality": "Qualité", "hitrate": "Taux de réussite", "hathrate": "Taux Hath",
        "served": "Servi", "last_seen": "Dernière vue"
    },
    "ru": {
        "official": "Официальная Java версия", "rust": "hath-rust", "web": "H@H веб-интерфейс",
        "new_version_found": "Новая версия H@H {label}: v{ver}", "update_type_new": "Новое", "update_type_update": "Обновление",
        "version_info": "Статус: {type}\nВерсия: {old} -> {new}", "changelog_label": "Список изменений",
        "quota_title": "Ежедневная квота H@H", "quota_body": "Текущая бесплатная квота архива:\n{quota}",
        "status_change": "Изменение статуса", "status_report": "Отчет о статусе", "client_msg_title": "H@H {type}: {name}",
        "online": "В сети", "offline": "Вне сети", "cur_status": "Текущий статус", "detail": "Подробности",
        "region": "Регион", "address": "Адрес", "version": "Версия", "speed": "Скорость",
        "trust": "Доверие", "quality": "Качество", "hitrate": "Частота запросов", "hathrate": "Скорость Hath",
        "served": "Обслужено", "last_seen": "Последний раз в сети"
    },
    "de": {
        "official": "Offizielle Java-Version", "rust": "hath-rust", "web": "H@H Webseite",
        "new_version_found": "Neue H@H {label} Version: v{ver}", "update_type_new": "Neu", "update_type_update": "Update",
        "version_info": "Status: {type}\nVersion: {old} -> {new}", "changelog_label": "Änderungsprotokoll",
        "quota_title": "H@H Tägliche Quoten-Erinnerung", "quota_body": "Aktuelle kostenlose Archivquote:\n{quota}",
        "status_change": "Statusänderung", "status_report": "Statusbericht", "client_msg_title": "H@H {type}: {name}",
        "online": "Online", "offline": "Offline", "cur_status": "Aktueller Status", "detail": "Details",
        "region": "Region", "address": "Adresse", "version": "Version", "speed": "Bandbreite",
        "trust": "Vertrauen", "quality": "Qualité", "hitrate": "Trefferquote", "hathrate": "Hath-Rate",
        "served": "Bedient", "last_seen": "Zuletzt gesehen"
    },
    "ja": {
        "official": "公式 Java 版", "rust": "hath-rust", "web": "H@H ウェブ版",
        "new_version_found": "H@H {label} 新バージョン: v{ver}", "update_type_new": "新発見", "update_type_update": "更新",
        "version_info": "状态: {type}\n版本: {old} -> {new}", "changelog_label": "変更履歴",
        "quota_title": "H@H 毎日のクォータ通知", "quota_body": "現在の無料アーカイブクォータ:\n{quota}",
        "status_change": "ステータス変更", "status_report": "ステータスレポート", "client_msg_title": "H@H {type}: {name}",
        "online": "オンライン", "offline": "オフライン", "cur_status": "現在のステータス", "detail": "詳細",
        "region": "地域", "address": "アドレス", "version": "バージョン", "speed": "帯域幅",
        "trust": "信頼", "quality": "品質", "hitrate": "ヒット率", "hathrate": "Hathレート",
        "served": "転送済み", "last_seen": "最終確認"
    },
    "ko": {
        "official": "공식 Java 버전", "rust": "hath-rust", "web": "H@H 웹 버전",
        "new_version_found": "H@H {label} 새 버전: v{ver}", "update_type_new": "새 발견", "update_type_update": "업데이트",
        "version_info": "상태: {type}\n버전: {old} -> {new}", "changelog_label": "변경 로그",
        "quota_title": "H@H 일일 쿼터 알림", "quota_body": "현재 무료 아카이브 쿼터:\n{quota}",
        "status_change": "상태 변경", "status_report": "상태 보고", "client_msg_title": "H@H {type}: {name}",
        "online": "온라인", "offline": "오프라인", "cur_status": "현재 상태", "detail": "상세",
        "region": "지역", "address": "주소", "version": "버전", "speed": "대역폭",
        "trust": "신뢰", "quality": "품질", "hitrate": "히트레이트", "hathrate": "Hath레이트",
        "served": "전송됨", "last_seen": "마지막 확인"
    },
    "ar": {
        "official": "نسخة جافا الرسمية", "rust": "hath-rust", "web": "صفحة ويب H@H",
        "new_version_found": "إصدار جديد من H@H {label}: v{ver}", "update_type_new": "جديد", "update_type_update": "تحديث",
        "version_info": "الحالة: {type}\nالإصدار: {old} -> {new}", "changelog_label": "سجل التغييرات",
        "quota_title": "تذكיר بحصة H@H اليومية", "quota_body": "حصة الأرشيف المجانية الحالية:\n{quota}",
        "status_change": "تغيיר الحالة", "status_report": "تقرير الحالة", "client_msg_title": "H@H {type}: {name}",
        "online": "متصل", "offline": "غير متصل", "cur_status": "الحالة الحالية", "detail": "التفاصيل",
        "region": "المنطقة", "address": "العنوان", "version": "الإصدار", "speed": "عرض النطاق التردדי",
        "trust": "الثقة", "quality": "الجودة", "hitrate": "معدل الإصابة", "hathrate": "معدل Hath",
        "served": "تم تقديمه", "last_seen": "آخر ظهور"
    },
    "he": {
        "official": "גרסת ג'אווה רשמית", "rust": "hath-rust", "web": "דף אינטרנט H@H",
        "new_version_found": "גרסה חדשה של H@H {label}: v{ver}", "update_type_new": "חדש", "update_type_update": "עדכון",
        "version_info": "סטטוס: {type}\nגרסה: {old} -> {new}", "changelog_label": "יומן שינויים",
        "quota_title": "תזכורת מכסה יומית של H@H", "quota_body": "מכסת ארכיון חינמית נוכחית:\n{quota}",
        "status_change": "שינוי סטטוס", "status_report": "דיווח סטטוס", "client_msg_title": "H@H {type}: {name}",
        "online": "מחובר", "offline": "מנותק", "cur_status": "סטטוס נוכחי", "detail": "פרטים",
        "region": "אזור", "address": "כתובת", "version": "גרסה", "speed": "רוחב פס",
        "trust": "אמון", "quality": "איכות", "hitrate": "שיעור פגיעה", "hathrate": "שיעור Hath",
        "served": "הוגש", "last_seen": "נראה לאחרונה"
    }
}

if __name__ == "__main__": main()
