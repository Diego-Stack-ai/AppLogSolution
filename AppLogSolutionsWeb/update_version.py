import os
import glob
import re

frontend_dir = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend"
html_files = glob.glob(os.path.join(frontend_dir, "*.html"))

new_version = "v=5.46"

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace any v=X.XX with v=5.46
    new_content = re.sub(r'v=\d+\.\d+', new_version, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(filepath)}")
