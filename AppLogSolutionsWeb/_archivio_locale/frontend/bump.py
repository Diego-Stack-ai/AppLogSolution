import os
import re

files = [os.path.join(r, f) for r, d, files in os.walk('.') for f in files if f.endswith('.html')]
for file in files:
    with open(file, 'r', encoding='utf-8') as f: content = f.read()
    content = re.sub(r'\?v=\d+\.\d+', '?v=2.172', content)
    with open(file, 'w', encoding='utf-8') as f: f.write(content)

with open('script.js', 'r', encoding='utf-8') as f: c=f.read()
c = re.sub(r'const APP_VERSION = \".*?\";', 'const APP_VERSION = "2.172";', c)
with open('script.js', 'w', encoding='utf-8') as f: f.write(c)

with open('sw.js', 'r', encoding='utf-8') as f: c=f.read()
c = re.sub(r'const CACHE_NAME = \'.*?\';', "const CACHE_NAME = 'log-solution-v2.172';", c)
with open('sw.js', 'w', encoding='utf-8') as f: f.write(c)
