import os
import re

FRONTEND_DIR = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend"

def bump_version():
    # Leggi versione da script.js
    script_path = os.path.join(FRONTEND_DIR, "script.js")
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r'const APP_VERSION = "(\d+\.\d+)";', content)
    if not match:
        print("Version not found in script.js!")
        return
        
    old_version = match.group(1)
    new_version = f"{float(old_version) + 0.01:.2f}"
    print(f"Bumping version: {old_version} -> {new_version}")

    # Update script.js
    new_content = content.replace(f'const APP_VERSION = "{old_version}";', f'const APP_VERSION = "{new_version}";')
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    # Update sw.js
    sw_path = os.path.join(FRONTEND_DIR, "sw.js")
    with open(sw_path, "r", encoding="utf-8") as f:
        sw_content = f.read()
    sw_content = sw_content.replace(f"const CACHE_NAME = 'log-solution-v{old_version}';", f"const CACHE_NAME = 'log-solution-v{new_version}';")
    with open(sw_path, "w", encoding="utf-8") as f:
        f.write(sw_content)

    # Update HTML files
    for file in os.listdir(FRONTEND_DIR):
        if file.endswith(".html"):
            file_path = os.path.join(FRONTEND_DIR, file)
            with open(file_path, "r", encoding="utf-8") as f:
                html = f.read()
            html = html.replace(f"?v={old_version}", f"?v={new_version}")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
    
    # Update js files
    for file in os.listdir(FRONTEND_DIR):
        if file.endswith(".js") and file not in ["script.js", "sw.js"]:
            file_path = os.path.join(FRONTEND_DIR, file)
            with open(file_path, "r", encoding="utf-8") as f:
                js_content = f.read()
            js_content = js_content.replace(f"?v={old_version}", f"?v={new_version}")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(js_content)
                
    print("Bump completed successfully.")

if __name__ == "__main__":
    bump_version()
