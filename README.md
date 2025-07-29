# Bot Telegram Music 🎵

Bot untuk download lagu dari Telegram dengan kualitas tinggi.

---

## ✅ Cara Install

Untuk pengguna **Linux**, **VPS**, atau **Termux Android**:

```bash
sudo apt update && sudo apt upgrade -y
git clone https://github.com/majdiza/bot-telegram-music.git
cd bot-telegram-music
bash install.sh
nano config.py  # Masukkan token bot Telegram Anda
python3 start.py
```

---

## 💬 Cara Menggunakan Bot

```bash
/music [judul lagu]
```

Contoh:

```bash
/music Noah separuh aku
```

Bot akan mencari dan mengirimkan lagu ke chat Telegram Anda dengan kualitas terbaik.

---

## 🔑 Cara Mendapatkan Token Telegram

1. Buka Telegram dan cari **@BotFather**
2. Kirim perintah:
   ```
   /start
   /newbot
   ```
3. Ikuti instruksi dan dapatkan token seperti ini:
   ```
   123456789:ABCDefGhIjklMnopQRstuVWXyz12345678
   ```
4. Masukkan token ke dalam file `config.py`:
   ```python
   API_TOKEN = "TOKEN_ANDA"
   ```

---

## ❌ Cara Menghapus atau Menonaktifkan Token

- Cabut token melalui @BotFather:
  ```
  /revoke
  ```
- Atau hapus manual dari `config.py`:
  ```python
  API_TOKEN = ""
  ```

---

## 🚪 Cara Menutup Terminal / Bash

Jika bot sedang berjalan:

```bash
CTRL + C
```

Lalu untuk menutup terminal sepenuhnya:

```bash
exit
```

Atau tekan `CTRL + D`

---

## 📄 Lisensi

© 2025 Bangjdi
