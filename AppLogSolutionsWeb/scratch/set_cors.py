from google.cloud import storage
import json

cred_path = r'g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'

client = storage.Client.from_service_account_json(cred_path)
bucket = client.get_bucket('log-solution-60007.firebasestorage.app')

cors = [
    {
        "origin": [
            "https://log-solution-60007.web.app",
            "https://log-solution-60007.firebaseapp.com",
            "http://localhost",
            "http://localhost:5000",
            "http://127.0.0.1:5000"
        ],
        "method": ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
        "responseHeader": [
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "x-goog-resumable"
        ],
        "maxAgeSeconds": 3600
    }
]

bucket.cors = cors
bucket.patch()
print("CORS aggiornato con successo sul bucket:", bucket.name)
print("Configurazione applicata:", json.dumps(bucket.cors, indent=2))
