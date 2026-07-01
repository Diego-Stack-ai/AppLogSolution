import os
import re

frontend_dir = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend"
old_version = "4.92"
new_version = "4.93"

pattern = re.compile(rf"\?v={re.escape(old_version)}")
replacement = f"?v={new_version}"

count = 0
for filename in os.listdir(frontend_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(frontend_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content, num_subs = re.subn(pattern, replacement, content)
        
        if num_subs > 0:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {filename}: {num_subs} replacements.")
            count += 1

print(f"Total HTML files updated: {count}")
