import os
import glob
import re

frontend_dir = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend"
html_files = glob.glob(os.path.join(frontend_dir, "*.html"))

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(r'\?v=\d+\.\d+', '?v=4.77', content)

    if content != new_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(file_path)}")
