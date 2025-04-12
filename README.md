
# ACHERON AutoTap VapeLabs Bot

Bot otomatis untuk nge-tap dan upgrade fitur di game [The Vape Labs](https://app.thevapelabs.io/game). Dibuat agar auto earn kamu gak pernah berhenti selama baterai terisi.

## Fitur
- Auto-tap sampai baterai penuh
- Auto-upgrade `auto_earn` dan `battery` jika mist cukup
- Cek token JWT otomatis (kadaluarsa atau tidak)
- Tampilan banner hijau “DYOR” saat mulai
- Loop otomatis setiap 2 jam
- Baca token dari file `token.txt`

## Cara Instalasi & Menjalankan di Termux

### 1. Update & install Python + Git
```bash
pkg update && pkg upgrade -y
pkg install python git -y
```

### 2. Clone repository ini
```bash
git clone https://github.com/acheronyor/autotap-vapelabs.git
cd autotap-vapelabs
```

### 3. Install dependensi Python
```bash
pip install requests pyjwt rich
```

### 4. Buat file token.txt
```bash
nano token.txt
```
Isi dengan token JWT kamu (dari localStorage), tanpa kata "Bearer". Lalu tekan CTRL + X, Y, Enter untuk menyimpan.

### 5. Jalankan bot
```bash
python autotap.py
```

## Struktur File
- `autotap.py` → Script utama
- `token.txt` → Tempat simpan token kamu (tidak akan diupload ke GitHub)
- `.gitignore` → Untuk mengecualikan file pribadi seperti token.txt
- `README.md` → Penjelasan penggunaan script

## Keamanan
- Jangan pernah share isi `token.txt`
- File `token.txt` sudah otomatis di-ignore oleh `.gitignore`

---

Script ini dibuat oleh **ACHERON** sebagai project otomatisasi pribadi.  
Gunakan dengan bijak, dan DYOR (Do Your Own Research)!
```
