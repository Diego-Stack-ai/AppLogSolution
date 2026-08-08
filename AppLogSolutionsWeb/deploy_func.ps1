$env:PATH = "H:\Il mio Drive\App\AppLogSolutionsWeb\functions\venv\Scripts;" + $env:PATH
$env:GCLOUD_PROJECT = "log-solutions-cantiere"
$env:GOOGLE_CLOUD_PROJECT = "log-solutions-cantiere"
$env:GOOGLE_APPLICATION_CREDENTIALS = "H:\Il mio Drive\App\AppLogSolutionsWeb\cantiere_key.json"
$env:FIREBASE_FUNCTIONS_DISCOVERY_TIMEOUT = "30000"

& "firebase" deploy --project log-solutions-cantiere --only functions:elabora_centro_costi
