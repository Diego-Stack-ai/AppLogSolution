import os
import glob
import re
import sys

NEW_VERSION = "6.250"

frontend_dir = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend"
html_files = glob.glob(os.path.join(frontend_dir, "*.html"))

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = re.sub(r'\?v=\d+\.\d+', f'?v={NEW_VERSION}', content)
    if content != new_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(file_path)}")

# Update script.js
script_path = os.path.join(frontend_dir, "script.js")
with open(script_path, "r", encoding="utf-8") as f:
    content = f.read()
new_content = re.sub(r'const APP_VERSION = ".*?";', f'const APP_VERSION = "{NEW_VERSION}";', content)
if content != new_content:
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated script.js")

# Update sw.js
sw_path = os.path.join(frontend_dir, "sw.js")
with open(sw_path, "r", encoding="utf-8") as f:
    content = f.read()
new_content = re.sub(r"const CACHE_NAME = 'log-solution-v.*?';", f"const CACHE_NAME = 'log-solution-v{NEW_VERSION}';", content)
if content != new_content:
    with open(sw_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated sw.js")
