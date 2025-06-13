# Gunakan image Python dasar yang ringan
FROM python:3.9-slim

# Install utilitas yang dibutuhkan: netcat (untuk wait-for) dan procps (untuk pkill)
RUN apt-get update && apt-get install -y netcat-openbsd procps && rm -rf /var/lib/apt/lists/*

# Tetapkan direktori kerja
WORKDIR /app

# Salin dan install library Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file proyek
COPY . .

# Berikan izin eksekusi pada skrip shell
RUN chmod +x /app/wait-for-kafka.sh /app/wait-for-minio.sh

# Perintah default (cadangan)
CMD ["python"]