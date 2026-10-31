# Tugas Arsitektur Perangkat Lunak - Containerization & Orchestration

Repositori ini berisi implementasi kontainerisasi aplikasi web sederhana berbasis **Python Flask** dengan menerapkan *best practices* Docker (Multi-stage build, non-root user, Alpine Linux) serta konfigurasi multi-kontainer menggunakan Docker Compose dan orkestrasi Kubernetes.

---

## 📁 Struktur Direktori

```text
├── app.py                     # Kode utama aplikasi Flask
├── requirements.txt           # Daftar dependensi Python (Flask, Gunicorn, Redis)
├── Dockerfile                 # Dockerfile teroptimasi (Multi-stage, Alpine, Non-root)
├── Dockerfile.unoptimized     # Dockerfile standar tanpa optimasi (baseline pembanding)
├── docker-compose.yml         # Konfigurasi multi-container (Flask + Redis Cache)
├── .dockerignore              # Mencegah file sampah masuk ke dalam build context
├── .gitignore                 # File pengabaian Git
├── k8s/
│   ├── deployment.yaml        # Manifest Kubernetes Deployment (3 replika, resource limits, probe)
│   └── service.yaml           # Manifest Kubernetes Service (LoadBalancer / Port Forwarding)
├── LAPORAN.md                 # Laporan lengkap analisis (600–800 kata)
├── laporan.html               # Format HTML laporan siap cetak / export ke PDF
└── generate_pdf.ps1           # Script PowerShell otomatis untuk generate PDF via headless browser
```

---

## 🚀 Panduan Menjalankan Aplikasi

### 1. Build & Run Single Container (Docker Standalone)

Pastikan Docker Desktop aktif di komputer Anda.

**Build Image Teroptimasi:**
```bash
docker build -t flask-app:latest .
```

**Jalankan Kontainer:**
```bash
docker run -d -p 5000:5000 --name web-flask flask-app:latest
```

Buka browser dan akses: `http://localhost:5000`  
Cek endpoint health check: `http://localhost:5000/health`

**Hentikan Kontainer:**
```bash
docker stop web-flask
docker rm web-flask
```

---

### 2. Menjalankan Multi-Container (Flask + Redis Cache) via Docker Compose

Untuk menjalankan aplikasi web bersama cache Redis:

```bash
# Menjalankan seluruh service di latar belakang (detached mode)
docker compose up -d --build

# Melihat status kontainer yang sedang berjalan
docker compose ps

# Melihat log aplikasi
docker compose logs -f web

# Menghentikan seluruh service
docker compose down
```

---

### 3. Deploy ke Kubernetes (K8s)

Pastikan klaster Kubernetes lokal (seperti Minikube, Kind, atau fitur Kubernetes di Docker Desktop) telah aktif.

**Terapkan Manifest:**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

**Verifikasi Status Pod dan Service:**
```bash
kubectl get pods -l app=flask-web
kubectl get svc flask-app-service
```

---

## 📊 Perbandingan Ukuran Image

Untuk menguji perbandingan ukuran image antara versi unoptimized dan versi teroptimasi:

```bash
# Build versi tanpa optimasi (Debian full)
docker build -f Dockerfile.unoptimized -t flask-app:unoptimized .

# Cek daftar ukuran image
docker images
```

Hasil perbandingan:
| Image | Base Image | Ukuran Image | Status Keamanan |
| :--- | :--- | :--- | :--- |
| `flask-app:unoptimized` | `python:3.11` (Debian) | ~1.02 GB | Root user, attack surface besar |
| `flask-app:latest` | `python:3.11-alpine` | ~58 MB | Non-root user, multi-stage, aman |

---

## 🌐 Tautan Repositori GitHub
- **URL Repositori:** [https://github.com/ibnusetyon25/Tugas_Arsitecture_Perangkat_Lunak](https://github.com/ibnusetyon25/Tugas_Arsitecture_Perangkat_Lunak)

---

## 📄 Laporan PDF
Dokumentasi tertulis lengkap (analisis instruksi Dockerfile, perbandingan optimasi, dan manifest Kubernetes) tersedia pada file `LAPORAN.pdf`.

