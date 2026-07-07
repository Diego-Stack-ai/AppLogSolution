import os
import re

root = 'frontend'
v_new = '5.70'

# 1. sw.js
with open(os.path.join(root, 'sw.js'), 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'log-solution-v[\d\.]+', f'log-solution-v{v_new}', c)
with open(os.path.join(root, 'sw.js'), 'w', encoding='utf-8') as f:
    f.write(c)

# 2. script.js
with open(os.path.join(root, 'script.js'), 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'APP_VERSION\s*=\s*"[\d\.]+"', f'APP_VERSION = "{v_new}"', c)
with open(os.path.join(root, 'script.js'), 'w', encoding='utf-8') as f:
    f.write(c)

# 3. HTML files
htmls = [f for f in os.listdir(root) if f.endswith('.html')]
for h in htmls:
    p = os.path.join(root, h)
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'\?v=[\d\.]+', f'?v={v_new}', c)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

print(f"Versione bumpata a {v_new}")
