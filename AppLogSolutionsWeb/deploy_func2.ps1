$env:PATH = "H:\Il mio Drive\App\AppLogSolutionsWeb\functions\venv\Scripts;" + $env:PATH
$env:GCLOUD_PROJECT = "log-solutions-cantiere"
$env:GOOGLE_CLOUD_PROJECT = "log-solutions-cantiere"
$env:GOOGLE_APPLICATION_CREDENTIALS = "H:\Il mio Drive\App\AppLogSolutionsWeb\cantiere_key.json"

$env:FUNCTIONS_DISCOVERY_TIMEOUT = "60000"
$env:FIREBASE_FUNCTIONS_DISCOVERY_TIMEOUT = "60000"

& "C:\Users\39349\AppData\Local\npm-cache\_npx\7750544ccf494d8b\node_modules\.bin\firebase.cmd" deploy --project log-solutions-cantiere --only functions:elabora_centro_costi --force


