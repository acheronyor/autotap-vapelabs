from rich import print
import requests
import time
import jwt
from datetime import datetime

# === KONFIGURASI ===
TAP_LIMIT = 100
TAP_DELAY = 0.3
LOOP_DELAY = 2 * 60 * 60  # 2 jam dalam detik
UPGRADE_KINDS = {"auto_earn": 1, "battery": 2}

URL_INFO = "https://api.thevapelabs.net/v1.0/user/info"
URL_UPGRADE = "https://api.thevapelabs.net/v1.0/user/upgrade"

def show_banner():
    print("\n[bold green]========================================[/bold green]")
    print("[bold green]              D Y O R[/bold green]")
    print("[green] AutoTap The Vape Labs Bot By: ACHERON[/green]")
    print("[bold green]========================================[/bold green]\n")

# Ambil semua token dari file
def load_tokens():
    with open("token.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

# Cek token valid atau tidak
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

# Kirim tap untuk isi battery
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

# Ambil info upgrade
def get_upgrade_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(URL_UPGRADE, headers=headers)
    if resp.status_code == 200:
        return resp.json()["data"]
    print(f"[!] Gagal ambil info upgrade: {resp.status_code} {resp.text}")
    return None

# Eksekusi upgrade
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

# Jalankan satu siklus untuk satu akun
def run_for_token(token, index):
    valid, username, remaining = is_token_valid(token)
    label = f"[Akun {index+1}]"
    if not valid:
        print(f"{label} Token invalid atau expired.")
        return
    print(f"{label} Mulai sebagai '{username}' (expire dalam {remaining//60} menit)")

    for i in range(TAP_LIMIT):
        data = send_tap(i, token)
        if not data:
            return
        print(f"[TAP {i}] Battery: {data['battery']} | Earn Mist: {data['earn_mist']:.2f}")
        if data["battery"] >= 100:
            print("[✓] Battery FULL!")
            break
        time.sleep(TAP_DELAY)

    print("[⋆] Mengecek peluang upgrade...")
    upgrade_info = get_upgrade_info(token)
    if not upgrade_info:
        return
    user_points = upgrade_info["user_info"]["points"]

    for tipe in ["auto_earn", "battery"]:
        info = upgrade_info[tipe]
        required = info["point_to_next_level"]
        if user_points >= required:
            print(f"[→] Upgrade {tipe} ({required} / {user_points:.2f})")
            do_upgrade(token, UPGRADE_KINDS[tipe])
            time.sleep(1)
        else:
            print(f"[×] Mist kurang untuk upgrade {tipe}: butuh {required}, punya {user_points:.2f}")

# === MAIN LOOP ===
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
