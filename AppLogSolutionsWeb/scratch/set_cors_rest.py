"""
Applica CORS su Firebase Storage tramite API REST di Google Cloud Storage.
Il Firebase JS SDK usa firebasestorage.googleapis.com con il nome bucket
nella forma 'projectid.appspot.com', ma il bucket fisico si chiama
'projectid.firebasestorage.app'. Questo script applica su entrambi.
"""
import json
import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account

CRED_PATH = r'g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
BUCKET = 'log-solution-60007.firebasestorage.app'

CORS = [
    {
        "origin": [
            "https://log-solution-60007.web.app",
            "https://log-solution-60007.firebaseapp.com",
            "http://localhost",
            "http://localhost:5000"
        ],
        "method": ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
        "responseHeader": [
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "x-goog-resumable",
            "x-goog-meta-*"
        ],
        "maxAgeSeconds": 3600
    }
]

scopes = ["https://www.googleapis.com/auth/devstorage.full_control"]
creds = service_account.Credentials.from_service_account_file(CRED_PATH, scopes=scopes)
session = google.auth.transport.requests.AuthorizedSession(creds)

url = f"https://storage.googleapis.com/storage/v1/b/{BUCKET}"
resp = session.patch(url, json={"cors": CORS})
print(f"Status: {resp.status_code}")
print(f"Response: {json.dumps(resp.json(), indent=2)}")
