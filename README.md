<div align="center">
<img src="https.raw.githubusercontent.com/majdiza/bot-telegram-music/main/assets/logo.png" alt="Logo" width="150">
<h1>Bot Telegram Music</h1>
<p><strong>Hidupkan suasana di grup Telegram Anda dengan musik!</strong></p>
<p>Bot ini memungkinkan Anda memutar lagu favorit langsung dari YouTube ke dalam Voice Chat grup atau channel. Mudah di-hosting, cepat, dan siap menghibur komunitas Anda.</p>
</div>
🎵 Fitur Unggulan
 * Putar dari YouTube: Cukup kirim link YouTube atau judul lagu.
 * Kualitas Audio Jernih: Ditenagai oleh ffmpeg untuk audio terbaik.
 * Antrean Lagu: Tambahkan beberapa lagu sekaligus dan biarkan bot memutarnya secara berurutan.
 * Kontrol Penuh: Perintah untuk skip, pause, resume, dan stop bagi admin.
 * Ringan & Cepat: Didesain untuk berjalan lancar di VPS dengan sumber daya minimal.
🚀 Instalasi Super Cepat
Hanya butuh beberapa menit untuk membuat bot Anda siap beraksi. Ikuti langkah-langkah di bawah ini untuk VPS (Linux) atau Termux.
A. Di VPS (Ubuntu/Debian)
Metode ini adalah yang paling direkomendasikan untuk menjaga bot Anda online 24/7 tanpa henti.
1. Persiapan Awal & Instalasi
Buka terminal SSH Anda dan jalankan skrip instalasi otomatis kami. Skrip ini akan mengurus semuanya, mulai dari update sistem hingga instalasi dependensi yang dibutuhkan.
sudo apt update && sudo apt upgrade -y
sudo apt install git -y
git clone https://github.com/majdiza/bot-telegram-music.git
cd bot-telegram-music
bash install.sh

2. Konfigurasi Bot Anda
Setelah instalasi selesai, saatnya menghubungkan bot dengan akun Telegram Anda. Edit file config.py menggunakan nano.
nano config.py

Di dalam file tersebut, Anda akan menemukan beberapa variabel. Anda hanya perlu mengisi BOT_TOKEN, API_ID, dan API_HASH.
# ===============================================================
# ISI BAGIAN INI DENGAN DATA ANDA
# ===============================================================

# Dapatkan dari @BotFather di Telegram
BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"

# Dapatkan dari my.telegram.org
API_ID = 12345678  # Ganti dengan API ID Anda
API_HASH = "ganti_dengan_api_hash_anda"

# ID Pengguna/Grup yang boleh menggunakan perintah admin
SUDO_USERS = [123456789] # Ganti dengan ID Anda

# ===============================================================

Simpan perubahan dengan menekan Ctrl+X, lalu Y, dan Enter.
3. Jalankan Bot!
Sekarang, hidupkan bot Anda dengan perintah sederhana:
python3 start.py

Bot Anda kini sudah online! Namun, untuk membuatnya tetap berjalan bahkan setelah Anda menutup terminal, sangat disarankan menggunakan screen atau tmux.
Menjalankan 24/7 dengan screen:
# Instal screen jika belum ada
sudo apt install screen -y

# Buat sesi baru
screen -S musikbot

# Jalankan bot di dalam sesi screen
python3 start.py

# Keluar dari sesi (detach) dengan menekan Ctrl+A lalu D.
# Bot akan tetap berjalan di latar belakang!

B. Di Termux (Android)
Metode ini cocok untuk uji coba cepat, tetapi tidak direkomendasikan untuk penggunaan jangka panjang.
pkg update && pkg upgrade -y
pkg install git python ffmpeg -y
git clone https://github.com/majdiza/bot-telegram-music.git
cd bot-telegram-music
pip install -r requirements.txt
cp config.py.example config.py
nano config.py # Isi token dan data lainnya
python3 start.py

🛠️ Perintah Bot
 * /play [judul lagu atau link YouTube]: Memutar lagu atau menambahkannya ke antrean.
 * /skip: Melewatkan lagu yang sedang diputar.
 * /pause: Menjeda pemutaran.
 * /resume: Melanjutkan pemutaran.
 * /stop: Menghentikan pemutaran dan membersihkan antrean.
<div align="center">
<p><strong>Dibuat dengan ❤️ untuk komunitas. Selamat menikmati musik!</strong></p>
</div>
