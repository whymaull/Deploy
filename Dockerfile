# Gunakan Python slim image
FROM python:3.10-slim

# Install dependencies OS untuk kompilasi pmdarima
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libatlas-base-dev \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Buat direktori kerja di dalam container
WORKDIR /app

# Salin semua file project ke dalam image
COPY . .

# Upgrade pip dan install semua dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Railway akan gunakan port dari ENV `PORT`, pastikan terbuka
EXPOSE 5000

# Jalankan aplikasinya
CMD ["python", "app.py"]
