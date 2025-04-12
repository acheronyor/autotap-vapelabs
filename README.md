Berikut versi **Markdown asli (siap paste)** untuk `README.md`:

```markdown
# DYOR AutoTap VapeLabs Bot

Bot otomatis untuk nge-tap dan upgrade fitur di game [The Vape Labs](https://app.thevapelabs.io/game). Dibuat agar auto earn kamu gak pernah berhenti selama baterai terisi.

## Fitur
- Auto-tap sampai baterai penuh
- Auto-upgrade `auto_earn` dan `battery` jika mist cukup
- Cek token JWT otomatis (kadaluarsa atau tidak)
- Tampilan banner hijau “DYOR” saat mulai
- Loop otomatis setiap 2 jam
- Baca token dari file `token.txt`

## Cara Pakai
1. Install Python 3
2. Install dependensi:
   ```bash
   pip install requests pyjwt rich
   ```
3. Buat file `token.txt` (di folder yang sama), isi dengan token JWT kamu (tanpa kata "Bearer")
4. Jalankan:
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


