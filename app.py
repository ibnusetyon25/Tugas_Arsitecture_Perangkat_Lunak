import os
import socket
from datetime import datetime
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Konfigurasi Redis jika tersedia (opsional via docker-compose)
REDIS_HOST = os.environ.get("REDIS_HOST", None)
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

redis_client = None
if REDIS_HOST:
    try:
        import redis
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, socket_timeout=2)
        redis_client.ping()
    except Exception:
        redis_client = None

# Fallback counter lokal jika Redis tidak aktif
local_counter = 0

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tugas Arsitektur Perangkat Lunak - Containerization</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 16px;
            max-width: 600px;
            width: 100%;
            padding: 32px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }
        .badge {
            display: inline-block;
            background: #0284c7;
            color: #fff;
            font-size: 12px;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 12px;
        }
        h1 {
            font-size: 24px;
            font-weight: 700;
            color: #38bdf8;
            margin-bottom: 8px;
        }
        p.subtitle {
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 24px;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 24px;
        }
        .info-box {
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 16px;
        }
        .info-label {
            font-size: 12px;
            color: #64748b;
            margin-bottom: 4px;
            text-transform: uppercase;
        }
        .info-value {
            font-size: 16px;
            font-weight: 600;
            color: #f1f5f9;
            word-break: break-all;
        }
        .counter-box {
            background: linear-gradient(135deg, #1e3a8a 0%, #0369a1 100%);
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            margin-bottom: 24px;
        }
        .counter-num {
            font-size: 42px;
            font-weight: 800;
            color: #ffffff;
        }
        .counter-desc {
            font-size: 13px;
            color: #bae6fd;
        }
        .footer {
            border-top: 1px solid #334155;
            padding-top: 16px;
            text-align: center;
            font-size: 12px;
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">Dockerized Flask App</span>
        <h1>Aplikasi Web Sederhana</h1>
        <p class="subtitle">Tugas Arsitektur Perangkat Lunak: Containerization & Orchestration</p>

        <div class="counter-box">
            <div class="counter-num">{{ count }}</div>
            <div class="counter-desc">Total Kunjungan Halaman (Storage: {{ storage_type }})</div>
        </div>

        <div class="grid">
            <div class="info-box">
                <div class="info-label">Hostname / Pod ID</div>
                <div class="info-value">{{ hostname }}</div>
            </div>
            <div class="info-box">
                <div class="info-label">Status Server</div>
                <div class="info-value" style="color: #4ade80;">Active / Healthy</div>
            </div>
            <div class="info-box">
                <div class="info-label">Waktu Akses</div>
                <div class="info-value">{{ current_time }}</div>
            </div>
            <div class="info-box">
                <div class="info-label">Redis Status</div>
                <div class="info-value" style="color: {{ '#4ade80' if redis_status else '#f87171' }}">
                    {{ 'Terhubung' if redis_status else 'Tidak Terhubung' }}
                </div>
            </div>
        </div>

        <div class="footer">
            Ibnu Setyo Nugroho (NIM: 257110015) | Multi-Stage Build | Non-Root User | Alpine Linux
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    global local_counter
    storage_type = "In-Memory (Local)"
    redis_active = False

    if redis_client:
        try:
            visits = redis_client.incr("page_views")
            storage_type = "Redis Cache"
            redis_active = True
        except Exception:
            local_counter += 1
            visits = local_counter
    else:
        local_counter += 1
        visits = local_counter

    hostname = socket.gethostname()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_template_string(
        HTML_TEMPLATE,
        count=visits,
        storage_type=storage_type,
        hostname=hostname,
        current_time=current_time,
        redis_status=redis_active
    )

@app.route("/health")
def health():
    """Health check endpoint untuk Kubernetes livenessProbe & readinessProbe"""
    return jsonify({
        "status": "UP",
        "hostname": socket.gethostname(),
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == "__main__":
    # Digunakan hanya untuk pengetesan lokal langsung
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

