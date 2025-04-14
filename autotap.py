from rich import print
import requests
import time
import jwt
import threading
from datetime import datetime

# === KONFIGURASI ===
TAP_LIMIT = 100
TAP_DELAY = 0.3
LOOP_DELAY = 2 * 60 * 60  # 2 jam dalam detik
UPGRADE_INTERVAL = 30 * 60  # 30 menit dalam detik
UPGRADE_KINDS = {"auto_earn": 1, "battery": 2}

URL_INFO = "https://api.thevapelabs.net/v1.0/user/info"
URL_UPGRADE = "https://api.thevapelabs.net/v1.0/user/upgrade"
URL_DAILY = "https://api.thevapelabs.net/v1.0/missions/completed"

def show_banner():
    print("\n[bold green]========================================[/bold green]")
    print("[bold green]              D Y O R[/bold green]")
    print("[green] AutoTap The Vape Labs Bot By: ACHERON[/green]")
    print("[bold green]========================================[/bold green]\n")

def load_tokens():
    with open("token.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def is_token_valid(token):
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp = payload.get("exp", 0)
        remaining = exp - int(time.time())
        if remaining > 0:
            return True, payload.get("username", "?"), remaining
        return False, None, 0
    except Exception:
        return False, None, 0

def send_tap(tab_number, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"init_data": "", "tab_number": tab_number}
    resp = requests.post(URL_INFO, headers=headers, json=payload)
    if resp.status_code == 200:
        return resp.json()["data"]
    print(f"[!] TAP Gagal: {resp.status_code} {resp.text}")
    return None

def get_upgrade_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(URL_UPGRADE, headers=headers)
    if resp.status_code == 200:
        return resp.json()["data"]
    print(f"[!] Gagal ambil info upgrade: {resp.status_code} {resp.text}")
    return None

def do_upgrade(token, kind):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"kind": kind}
    resp = requests.post(URL_UPGRADE, headers=headers, json=payload)
    if resp.status_code == 200:
        res = resp.json()
        if res.get("code") == 200:
            print(f"[UPGRADE] Berhasil upgrade kind={kind}")
            return True
        elif res.get("code") == 10:
            print(f"[UPGRADE] Gagal (mist tidak cukup) kind={kind}")
            return False
    print(f"[UPGRADE] Error: {resp.status_code} {resp.text}")
    return False

def auto_upgrade_loop(token, label):
    while True:
        print(f"\n{label} [UPGRADE] Cek otomatis tiap 30 menit...")
        upgrade_info = get_upgrade_info(token)
        if not upgrade_info:
            time.sleep(UPGRADE_INTERVAL)
            continue
        user_points = upgrade_info["user_info"]["points"]
        for tipe in ["auto_earn", "battery"]:
            info = upgrade_info[tipe]
            required = info["point_to_next_level"]
            if user_points >= required:
                print(f"{label} [→] Upgrade {tipe} ({required} / {user_points:.2f})")
                do_upgrade(token, UPGRADE_KINDS[tipe])
                time.sleep(1)
            else:
                print(f"{label} [×] Mist kurang untuk upgrade {tipe}: butuh {required}, punya {user_points:.2f}")
        time.sleep(UPGRADE_INTERVAL)

def daily_checkin(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"task_id": 247, "link": ""}
    resp = requests.post(URL_DAILY, headers=headers, json=payload)
    if resp.status_code == 200 and resp.json().get("code") == 200:
        print("[CHECK-IN] Berhasil klaim daily reward!")
    else:
        print(f"[CHECK-IN] Gagal: {resp.status_code} {resp.text}")

def run_for_token(token, index):
    valid, username, remaining = is_token_valid(token)
    label = f"[Akun {index+1}]"
    if not valid:
        print(f"{label} Token invalid atau expired.")
        return
    print(f"{label} Mulai sebagai '{username}' (expire dalam {remaining//60} menit)")

    # Jalankan upgrade di thread terpisah
    threading.Thread(target=auto_upgrade_loop, args=(token, label), daemon=True).start()

    daily_checkin(token)

    for i in range(TAP_LIMIT):
        data = send_tap(i, token)
        if not data:
            return
        print(f"[TAP {i}] Battery: {data['battery']} | Earn Mist: {data['earn_mist']:.2f}")
        if data["battery"] >= 100:
            print("[✓] Battery FULL!")
            break
        time.sleep(TAP_DELAY)

if __name__ == "__main__":
    show_banner()
    while True:
        tokens = load_tokens()
        for idx, token in enumerate(tokens):
            print(f"\n================ Akun {idx+1} ================")
            run_for_token(token, idx)
            print("========================================\n")
        print(f"[⏳] Menunggu {LOOP_DELAY // 3600} jam sebelum siklus berikutnya...")
        time.sleep(LOOP_DELAY)
