# Usa un'immagine Python ufficiale e leggera
FROM python:3.12-slim

# Evita che Python generi file .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Impedisce che stdout e stderr vengano bufferizzati
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installa le dipendenze di sistema necessarie (per pdfplumber / ghostscript se servono in futuro, ma solitamente slim va bene)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia l'applicazione
COPY . .

# Cloud Run espone nativamente la porta 8080 tramite la env var PORT
ENV PORT=8080
EXPOSE 8080

# Esegui l'app con Gunicorn (raccomandato per Flask in prod)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
