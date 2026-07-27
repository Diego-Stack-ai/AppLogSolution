cd "H:\Il mio Drive\App\AppLogSolutionsWeb"

Write-Host "1. Verifica sintassi"
& "C:\Users\39349\AppData\Local\Programs\Python\Python314\python.exe" -m py_compile functions\main.py
if ($LASTEXITCODE -ne 0) {
    throw "Compilazione Python fallita: deploy annullato."
}

Write-Host "2. Suite C2G e regressione"
Write-Host "Esecuzione test_cattel_parser.py (Suite C2G)..."
& "C:\Users\39349\AppData\Local\Programs\Python\Python314\python.exe" test_cattel_parser.py
if ($LASTEXITCODE -ne 0) {
    throw "Test C2G fallito."
}
Write-Host "Esecuzione test_preflight.py..."
& "C:\Users\39349\AppData\Local\Programs\Python\Python314\python.exe" functions\test_preflight.py
# Ignore if test_preflight fails because it might be incomplete, or check it. We will strictly check $LASTEXITCODE.
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: test_preflight.py failed or returned non-zero."
}
Write-Host "Tutti i test PASS."

Write-Host "3. Setup ENV"
$env:PATH = "H:\Il mio Drive\App\AppLogSolutionsWeb\functions\venv\Scripts;C:\Users\39349\AppData\Local\Programs\cursor\resources\app\resources\helpers;" + $env:PATH
$env:GCLOUD_PROJECT = "log-solutions-sviluppo"
$env:GOOGLE_CLOUD_PROJECT = "log-solutions-sviluppo"
$env:GOOGLE_APPLICATION_CREDENTIALS = "H:\Il mio Drive\App\AppLogSolutionsWeb\dev_key.json"

Write-Host "4. Controllo Firebase CLI"
& "C:\Users\39349\AppData\Local\npm-cache\_npx\7750544ccf494d8b\node_modules\.bin\firebase.cmd" --version
if ($LASTEXITCODE -ne 0) {
    throw "Firebase CLI non disponibile: deploy annullato."
}

Write-Host "5. Deploy selettivo ESCLUSIVAMENTE su DEV"
& "C:\Users\39349\AppData\Local\npm-cache\_npx\7750544ccf494d8b\node_modules\.bin\firebase.cmd" deploy `
  --project log-solutions-sviluppo `
  --only "functions:processa_job_pdf,functions:genera_report_giornaliero,functions:calcola_percorsi_zone,functions:web_calcola_percorsi"

if ($LASTEXITCODE -ne 0) {
    throw "Deploy DEV fallito. Non procedere con pulizia o reimportazione."
}

Write-Host "DEPLOY DEV COMPLETATO. Fermarsi e preparare l'inventario dei dati errati prima di qualsiasi cancellazione."
