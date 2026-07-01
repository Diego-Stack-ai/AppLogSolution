import os
import glob
import re

frontend_dir = 'frontend'
html_files = glob.glob(os.path.join(frontend_dir, '*.html'))

old_version_pattern = r'\?v=\d+\.\d+'
new_version_string = '?v=5.02'

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(old_version_pattern, new_version_string, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"No changes for {filepath}")

print("Update complete.")
