import re

filepath = r"G:\Il mio Drive\App\AppLogSolutionsWeb\functions\main.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Rimuovo manual CORS da autista_aggiorna_sequenza
content = re.sub(
    r"    if req.method == 'OPTIONS':\s+headers = \{\s+'Access-Control-Allow-Origin': '\*',\s+'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',\s+'Access-Control-Allow-Headers': 'Content-Type',\s+'Access-Control-Max-Age': '3600'\s+\}\s+return https_fn.Response\('', status=204, headers=headers\)\s+",
    "",
    content
)

# Rimuovo headers={'Access-Control-Allow-Origin': '*'}
content = content.replace(", headers={'Access-Control-Allow-Origin': '*'}", "")
content = content.replace(", headers={'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}", ", headers={'Content-Type': 'application/json'}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("CORS duplicato rimosso")
