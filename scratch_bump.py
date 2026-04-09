import os
import glob
import re

dir_path = r"g:\Il mio Drive\AppLogSolutions\frontend"

# Read version from script.js
script_path = os.path.join(dir_path, "script.js")
with open(script_path, "r", encoding="utf-8") as f:
    script_content = f.read()

match = re.search(r'APP_VERSION\s*=\s*"(\d+)\.(\d+)"', script_content)
if not match:
    print("Cannot find version")
    exit(1)

major = int(match.group(1))
minor = int(match.group(2))
old_v = f"{major}.{minor}"
new_v = f"{major}.{minor + 1}"

# sw.js
sw_file = os.path.join(dir_path, "sw.js")
with open(sw_file, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace(f"log-solution-v{old_v}", f"log-solution-v{new_v}")
with open(sw_file, "w", encoding="utf-8") as f:
    f.write(c)

html_files = glob.glob(os.path.join(dir_path, "*.html"))
js_files = [f for f in glob.glob(os.path.join(dir_path, "*.js")) if not f.endswith("sw.js")]

for path in html_files + js_files:
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace(f"v={old_v}", f"v={new_v}")
    
    if "script.js" in path:
        c = c.replace(f'APP_VERSION = "{old_v}"', f'APP_VERSION = "{new_v}"')
        c = c.replace(f'// script.js - v{old_v}', f'// script.js - v{new_v}')
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
        
print(f"Bumped version from {old_v} to {new_v}")
