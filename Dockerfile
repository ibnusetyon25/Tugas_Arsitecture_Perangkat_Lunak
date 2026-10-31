# ==============================================================================
# STAGE 1: Build & Dependency Stage
# ==============================================================================
FROM python:3.11-alpine AS builder

# Set direktori kerja untuk proses build
WORKDIR /build

# Mencegah pembuatan file .pyc dan memastikan output log tidak dibuffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Salin hanya requirements.txt terlebih dahulu untuk memanfaatkan Docker Layer Caching
COPY requirements.txt .

# Instal dependensi ke direktori prefix /install agar mudah disalin ke stage berikutnya
# --no-cache-dir mencegah penyimpanan file installer wheel di cache pip
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ==============================================================================
# STAGE 2: Final / Production Runtime Stage
# ==============================================================================
FROM python:3.11-alpine AS runner

# Metadata image
LABEL maintainer="Ibnu Setyo Nugroho (NIM: 257110015)" \
      description="Flask Web App - Optimized Production Image"

# Variabel lingkungan runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Buat grup dan pengguna non-root demi alasan keamanan (Least Privilege)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set direktori kerja aplikasi
WORKDIR /app

# Salin hanya library python yang telah terpasang dari builder stage
COPY --from=builder /install /usr/local

# Salin kode sumber aplikasi dengan hak kepemilikan non-root user
COPY --chown=appuser:appgroup app.py .

# Expose port aplikasi
EXPOSE 5000

# Beralih dari user root ke user non-root
USER appuser

# Health check untuk memantau kondisi container secara otomatis
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -qO- http://127.0.0.1:5000/health || exit 1

# Jalankan aplikasi menggunakan Production WSGI Server (Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]

