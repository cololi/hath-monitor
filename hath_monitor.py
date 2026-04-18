#!/usr/bin/env python3
import argparse, json, logging, re, sqlite3, sys, time, tomllib, ssl, html
import urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

APP_NAME, VERSION = "hath-monitor", "1.3.0"
BASE_DIR = Path(__file__).resolve().parent
DB_PATH, CONFIG_PATH = BASE_DIR / "hath_monitor.db", BASE_DIR / "config.toml"
UA = f"{APP_NAME}/{VERSION}"
logger = logging.getLogger(APP_NAME)

def request(url, cfg=None, data=None, headers=None, method=None, timeout=10):
    headers = {"User-Agent": UA, **(headers or {})}
    if data:
        data = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    
    ctx = ssl.create_default_context()
    ctx.check_hostname, ctx.verify_mode = False, ssl.CERT_NONE
    
    handlers = [urllib.request.HTTPSHandler(context=ctx)]
    if cfg and cfg.get("proxy"):
        handlers.append(urllib.request.ProxyHandler({"http": cfg["proxy"], "https": cfg["proxy"]}))
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.build_opener(*handlers).open(req, timeout=timeout) as r:
            return r.read() if method != "HEAD" else True
    except Exception as e:
        if method != "HEAD": logger.debug("请求 %s 失败: %s", url, e)
        return None if method != "HEAD" else False

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS v (id INTEGER PRIMARY KEY, src TEXT, ver TEXT, extra TEXT, ts TEXT)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sv ON v(src, ver)")

def check_official(cfg):
    logger.info("🔍 检查官方 Java 客户端版本...")
    base = "https://repo.e-hentai.org/hath/HentaiAtHome_{v}.zip"
    with sqlite3.connect(DB_PATH) as conn:
        last = conn.execute("SELECT ver FROM v WHERE src = 'official' ORDER BY id DESC LIMIT 1").fetchone()
    best = last[0] if last else "1.6.5"
    v_tuple = tuple(int(x) for x in best.split("."))
    
    for p in range(v_tuple[2], v_tuple[2] + 10):
        cand = f"{v_tuple[0]}.{v_tuple[1]}.{p}"
        if request(base.format(v=cand), cfg, method="HEAD"): best = cand
        else: break
    return best, base.format(v=best)

def check_rust(cfg):
    logger.info("🔍 检查 hath-rust 版本...")
    res = request("https://api.github.com/repos/james58899/hath-rust/releases/latest", cfg)
    if not res: return None
    data = json.loads(res)
    return data["tag_name"].lstrip("v"), data["html_url"], data.get("body", "")[:500]

def check_hath_page(cfg):
    if not cfg.get("eh_ipb_member_id"): return None
    logger.info("🔍 正在抓取 EH H@H 管理页面...")
    cookie = f"ipb_member_id={cfg['eh_ipb_member_id']}; ipb_pass_hash={cfg['eh_ipb_pass_hash']}"
    res = request("https://e-hentai.org/hentaiathome.php", cfg, headers={"Cookie": cookie})
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
                
                # 强化版翻译逻辑：不区分大小写，且支持包含关键词的模糊匹配
                status_lower = status_raw.lower()
                if "online" in status_lower:
                    status_cn = "在线"
                elif "offline" in status_lower:
                    status_cn = "离线"
                else:
                    status_cn = status_raw # 保留无法识别的状态原样
                
                clients.append({
                    "id": cid,
                    "name": name,
                    "status": status_cn,
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
    res = request("https://forums.e-hentai.org/index.php?showtopic=234458&view=getlastpost", cfg, headers={"Cookie": cookie})
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

def send_notify(ncfg, title, body, group="H@H"):
    logger.info("📢 发送通知: %s", title)
    if ncfg.get("bark_url"):
        request(ncfg.get("bark_url").rstrip("/"), data={"title": title, "body": body, "group": group, "sound": ncfg.get("bark_sound", "minuet")})
    if ncfg.get("telegram_bot_token"):
        tg_text = f"<b>{title}</b>\n\n{body}"
        request(f"https://api.telegram.org/bot{ncfg['telegram_bot_token']}/sendMessage", 
                data={"chat_id": ncfg["telegram_chat_id"], "text": tg_text, "parse_mode": "HTML"})
    for url in ncfg.get("webhooks", []):
        request(url, data={"title": title, "body": body})

def run_check(config, force_push=False):
    mcfg, ncfg = config.get("monitor", {}), config.get("notify", {})
    init_db()
    now_iso = datetime.now(timezone.utc).isoformat()
    
    with sqlite3.connect(DB_PATH) as conn:
        # 1. 软件版本检查
        for src, func, label in [("official", check_official, "官方 Java 版"), ("rust", check_rust, "hath-rust")]:
            if not mcfg.get(f"check_{src}"): continue
            res = func(mcfg)
            if not res: continue
            ver, *rest = res if isinstance(res, tuple) else (res,)
            last = conn.execute("SELECT ver FROM v WHERE src = ? ORDER BY id DESC LIMIT 1", (src,)).fetchone()
            
            if force_push or not last or last[0] != ver:
                extra = {"url": rest[0] if len(rest) > 0 else "", "changelog": rest[1] if len(rest) > 1 else ""}
                if not force_push:
                    conn.execute("INSERT INTO v (src, ver, extra, ts) VALUES (?, ?, ?, ?)", (src, ver, json.dumps(extra), now_iso))
                
                title = f"H@H {label} 新版本: v{ver}"
                body = f"状态: {'更新' if last else '新发现'}\n版本: {last[0] if last else '?' } -> {ver}"
                if extra.get("changelog"): body += f"\n\n更新日志:\n{extra['changelog']}"
                send_notify(ncfg, title, body)

        # 2. EH 管理页面检查
        if mcfg.get("check_ehpage"):
            data = check_hath_page(mcfg)
            if data:
                # 页面版本号
                if "version" in data:
                    ver = data["version"]
                    last = conn.execute("SELECT ver FROM v WHERE src = 'ehpage' ORDER BY id DESC LIMIT 1").fetchone()
                    if force_push or not last or last[0] != ver:
                        extra = {"changelog": get_changelog(ver, mcfg)}
                        if not force_push:
                            conn.execute("INSERT INTO v (src, ver, extra, ts) VALUES ('ehpage', ?, ?, ?)", (ver, json.dumps(extra), now_iso))
                        title = f"H@H 网页端新版本: v{ver}"
                        body = f"版本: {last[0] if last else '?' } -> {ver}"
                        send_notify(ncfg, title, body)
                
                # 免费配额 (每日推送)
                if mcfg.get("check_quota") and "quota" in data:
                    quota = data["quota"]
                    last_q = conn.execute("SELECT ts, ver FROM v WHERE src = 'quota' ORDER BY id DESC LIMIT 1").fetchone()
                    is_new_day = not last_q or datetime.fromisoformat(last_q[0]).date() < datetime.now(timezone.utc).date()
                    if force_push or is_new_day:
                        if not force_push:
                            conn.execute("INSERT INTO v (src, ver, extra, ts) VALUES ('quota', ?, '', ?)", (quota, now_iso))
                        send_notify(ncfg, "H@H 每日配额提醒", f"当前免费存档配额 (Free Archive Quota):\n{quota}")
                
                # 客户端状态检查 (详细信息推送)
                if mcfg.get("check_clients") and "clients" in data:
                    for client in data["clients"]:
                        cid, name, status = client["id"], client["name"], client["status"]
                        src_name = f"client_{cid}"
                        last_s = conn.execute("SELECT ver FROM v WHERE src = ? ORDER BY id DESC LIMIT 1", (src_name,)).fetchone()
                        
                        if force_push or not last_s or last_s[0] != status:
                            if not force_push:
                                conn.execute("INSERT INTO v (src, ver, extra, ts) VALUES (?, ?, ?, ?)", (src_name, status, name, now_iso))
                            
                            is_change = last_s and last_s[0] != status
                            title = f"H@H {'状态变更' if is_change else '状态报告'}: {name}"
                            
                            status_detail = f"{last_s[0]} ➔ {status}" if is_change else f"{status} (保持中)"
                            
                            body = (
                                f"当前状态: {status} (ID: {cid})\n"
                                f"详情: {status_detail}\n"
                                f"地区: {client.get('region')}\n"
                                f"地址: {client.get('ip')}:{client.get('port')}\n"
                                f"版本: {client.get('version')}\n"
                                f"带宽: {client.get('max_speed')}\n"
                                f"信任: {client.get('trust')}\n"
                                f"质量: {client.get('quality')}\n"
                                f"点击: {client.get('hitrate')}\n"
                                f"产率: {client.get('hathrate')}\n"
                                f"已传: {client.get('files_served')}\n"
                                f"最后: {client.get('last_seen')}"
                            )
                            send_notify(ncfg, title, body)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--daemon", action="store_true", help="以守护进程模式运行")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细调试信息")
    parser.add_argument("--history", action="store_true", help="查看最近监控记录")
    parser.add_argument("--push-all", action="store_true", help="强制全量推送当前状态")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="[%(asctime)s] %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    if not CONFIG_PATH.exists():
        logger.error("配置文件 config.toml 不存在")
        return

    with open(CONFIG_PATH, "rb") as f: config = tomllib.load(f)

    if args.history:
        with sqlite3.connect(DB_PATH) as conn:
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
