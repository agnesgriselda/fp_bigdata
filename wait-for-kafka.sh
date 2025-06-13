#!/bin/sh
# wait-for-kafka.sh
# Skrip ini akan terus mencoba terhubung ke host 'kafka' di port 9092.
# Ini menggunakan 'netcat' (nc) dengan flag '-z' (zero-I/O mode) untuk hanya mengecek koneksi.

# Loop akan terus berjalan selama perintah 'nc' gagal (exit code bukan 0)
until nc -z kafka 9092; do
  echo "Menunggu Kafka siap..."
  # Tunggu 1 detik sebelum mencoba lagi
  sleep 1
done

echo ">>> Kafka sudah siap! <<<"
# 'exec "$@"' akan menjalankan perintah apa pun yang diberikan setelah skrip ini.
# Contoh: exec python my_script.py
exec "$@"