#!/bin/bash
# Skrip untuk menginstall semua kebutuhan bot

# Hentikan skrip jika ada perintah yang gagal
set -e

echo ">>> [Langkah 1 dari 2] Mengupdate sistem & menginstall alat..."
apt-get update && apt-get install -y python3 python3-pip git ffmpeg screen

echo ">>> [Langkah 2 dari 2] Menginstall semua pustaka Python dari requirements.txt..."
pip install -r requirements.txt

echo ""
echo "✅ Instalasi Selesai!"
echo "Semua program dan pustaka yang dibutuhkan telah terpasang."
echo "Sekarang Anda bisa menjalankan bot utama."
