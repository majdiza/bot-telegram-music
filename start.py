# start.py

import logging
import os
import asyncio
import sqlite3
import psutil
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, JobQueue

# --- Impor untuk Keep-Alive ---
from flask import Flask
import threading
# -----------------------------

# Impor konfigurasi
from config import TOKEN, ADMIN_IDS, MAX_FILE_SIZE_MB

# --- Konfigurasi Awal ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Inisialisasi Database & Antrian ---
DATABASE_FILE = "users.db"
BUSY_QUEUE = asyncio.Queue()

def initialize_database():
    """Membuat database SQLite dan tabel users."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
        conn.commit()
    logger.info("Database berhasil diinisialisasi.")

# --- FUNGSI-FUNGSI UTAMA & PEMBANTU ---

def is_server_busy():
    """Mengecek jika penggunaan CPU atau RAM melebihi 80%."""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    if cpu > 80 or ram > 80:
        logger.warning(f"Server sibuk! CPU: {cpu}%, RAM: {ram}%")
        return True
    return False

def download_music_sync(query: str):
    """Fungsi download sinkron yang akan dijalankan di thread terpisah."""
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
        if not info.get('entries'):
            raise ValueError("Lagu tidak ditemukan.")
        
        video_info = info['entries'][0]
        # Proses download file sebenarnya
        ydl.download([video_info['webpage_url']])
        # Siapkan path file hasil download
        downloaded_file_path = ydl.prepare_filename(video_info).rsplit('.', 1)[0] + '.mp3'
        return downloaded_file_path, video_info.get('title', 'audio')


async def run_download_and_send(context: ContextTypes.DEFAULT_TYPE, chat_id: int, original_message_id: int, query: str):
    """Proses lengkap dari mencari, mengunduh, hingga mengirim audio."""
    status_message = await context.bot.send_message(chat_id, "🔎 Mencari lagu...", reply_to_message_id=original_message_id)
    downloaded_file = None
    
    try:
        # Jalankan fungsi download yang berat di thread terpisah agar tidak memblokir bot
        downloaded_file, title = await asyncio.to_thread(download_music_sync, query)

        await context.bot.edit_message_text(f"✅ Lagu ditemukan: *{title}*\n\n📥 Mengunduh & mengirim...", chat_id, status_message.message_id, parse_mode='Markdown')
        
        file_size_mb = os.path.getsize(downloaded_file) / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            await context.bot.edit_message_text(f"❌ Gagal. Ukuran file {file_size_mb:.2f} MB melebihi batas {MAX_FILE_SIZE_MB} MB.", chat_id, status_message.message_id)
            return

        with open(downloaded_file, 'rb') as audio_file:
            await context.bot.send_audio(
                chat_id=chat_id,
                audio=audio_file,
                caption=f"🎧 {os.path.basename(downloaded_file)}",
                reply_to_message_id=original_message_id
            )
        await context.bot.delete_message(chat_id, status_message.message_id)

    except Exception as e:
        logger.error(f"Error pada proses download untuk chat {chat_id}: {e}", exc_info=True)
        await context.bot.edit_message_text(f"❌ Maaf, terjadi kesalahan: `{str(e)}`", chat_id, status_message.message_id, parse_mode='Markdown')
    
    finally:
        if downloaded_file and os.path.exists(downloaded_file):
            os.remove(downloaded_file)

# --- COMMAND HANDLERS ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user.id,))
        conn.commit()
    
    await update.message.reply_html(
        f"👋 Halo, {user.mention_html()}!\n\n"
        "Kirim perintah `/music` diikuti judul lagu, dan saya akan bekerja untukmu."
    )

async def music_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Gunakan format: /music [Judul Lagu]")
        return

    request_info = {
        'chat_id': update.effective_chat.id,
        'original_message_id': update.message.message_id,
        'query': query
    }

    if is_server_busy():
        await BUSY_QUEUE.put(request_info)
        await update.message.reply_text(f"🚧 Server sibuk. Permintaan Anda masuk antrian ke-{BUSY_QUEUE.qsize()}.")
    else:
        # Jalankan langsung jika server tidak sibuk
        asyncio.create_task(run_download_and_send(context, **request_info))

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    message = " ".join(context.args)
    if not message:
        await update.message.reply_text("Gunakan: /broadcast [Pesan]")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        users = conn.cursor().execute("SELECT user_id FROM users").fetchall()

    await update.message.reply_text(f"📣 Memulai broadcast ke {len(users)} pengguna...")
    count = 0
    for user in users:
        try:
            await context.bot.send_message(chat_id=user[0], text=message)
            count += 1
            await asyncio.sleep(0.1) # Jeda anti-spam
        except Exception:
            logger.warning(f"Gagal kirim ke {user[0]}")
    await update.message.reply_text(f"✅ Broadcast selesai. Terkirim ke {count} pengguna.")

# --- BACKGROUND WORKER ---

async def queue_worker(context: ContextTypes.DEFAULT_TYPE):
    logger.info("Worker antrian dimulai.")
    while True:
        if not is_server_busy() and not BUSY_QUEUE.empty():
            request = await BUSY_QUEUE.get()
            await context.bot.send_message(request['chat_id'], "✅ Giliran Anda dari antrian sedang diproses...")
            asyncio.create_task(run_download_and_send(context, **request))
            BUSY_QUEUE.task_done()
        await asyncio.sleep(5) # Cek antrian setiap 5 detik


# --- KODE WEB SERVER UNTUK KEEP-ALIVE ---
app = Flask(__name__)

@app.route('/')
def index():
    """Halaman simpel untuk menunjukkan bot aktif."""
    return "Bot is alive and running!"

def run_web_server():
    """Menjalankan Flask server."""
    app.run(host='0.0.0.0', port=8080)
# ----------------------------------------


# --- FUNGSI UTAMA ---

def main():
    initialize_database()

    # Menjalankan web server di thread terpisah agar bot tidak terblokir
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    logger.info("Keep-alive web server started.")
    
    # Buat instance JobQueue
    job_queue = JobQueue()
    
    # Pasang job_queue saat membangun aplikasi
    application = Application.builder().token(TOKEN).job_queue(job_queue).build()

    # Daftarkan background worker
    if application.job_queue:
        application.job_queue.run_once(queue_worker, 0)

    # Daftarkan command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("music", music_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))

    logger.info("✅ Bot telah berhasil dimulai!")
    application.run_polling()


if __name__ == "__main__":
    main()
