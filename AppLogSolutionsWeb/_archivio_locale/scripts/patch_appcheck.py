import os
import glob
import re

frontend_dir = r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend"
site_key = "6Le8IjAtAAAAAIFW6c_ToaLJELGoygI27BW6d1jZ"

appcheck_import = 'import { initializeAppCheck, ReCaptchaV3Provider } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app-check.js";\n'

appcheck_init = f"""
try {{
    initializeAppCheck(app, {{
        provider: new ReCaptchaV3Provider('{site_key}'),
        isTokenAutoRefreshEnabled: true
    }});
}} catch (e) {{ console.warn("AppCheck init:", e); }}
"""

files_to_patch = []
for root, _, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith('.html') or f.endswith('.js'):
            files_to_patch.append(os.path.join(root, f))

patched_count = 0

for file_path in files_to_patch:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'firebase-app-check.js' in content:
            continue # Already patched or has it
            
        if 'initializeApp(firebaseConfig)' not in content:
            continue # Doesn't initialize app
            
        # We need to insert the import right after the firebase-app.js import
        import_pattern = r'(import\s*\{.*?\}.*?firebase-app\.js["\'];?)'
        
        # We need to insert the init right after the app initialization
        app_init_pattern = r'(const\s+app\s*=\s*(?:getApps\(\)\.length.*?:\s*)?initializeApp\(firebaseConfig\)(?:,\s*"[^"]+")?;?)'
        
        if re.search(import_pattern, content) and re.search(app_init_pattern, content):
            # Do replacement
            new_content = re.sub(import_pattern, r'\1\n' + appcheck_import, content, count=1)
            new_content = re.sub(app_init_pattern, r'\1\n' + appcheck_init, new_content, count=1)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            print(f"Patched: {os.path.relpath(file_path, frontend_dir)}")
            patched_count += 1
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

print(f"\nTotal files patched: {patched_count}")
