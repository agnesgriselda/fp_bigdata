#!/bin/sh
# wait-for-minio.sh
# Skrip ini bekerja sama seperti wait-for-kafka.sh, tapi untuk MinIO.
# Ia akan mengecek koneksi ke host 'minio' di port 9000.

until nc -z minio 9000; do
  echo "Menunggu MinIO siap..."
  sleep 1
done

echo ">>> MinIO sudah siap! <<<"
exec "$@"