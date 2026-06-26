import os
import glob

directory = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend"
old_version = "v=2.170"
new_version = "v=2.171"

html_files = glob.glob(os.path.join(directory, "*.html"))

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    if old_version in content:
        content = content.replace(old_version, new_version)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Updated {file_path}")
    else:
        print(f"No match found in {file_path}")
