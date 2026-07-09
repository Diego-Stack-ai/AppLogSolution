import sys

filepath = r"G:\Il mio Drive\App\AppLogSolutionsWeb\functions\main.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Trova la parte da sostituire
target = """                if json_blob.exists():
                    import json
                    raw_json = json.loads(json_blob"""

replacement = """                if json_blob.exists():
                    raw_json = json.loads(json_blob"""

content = content.replace(target, replacement)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fix import json applied")
