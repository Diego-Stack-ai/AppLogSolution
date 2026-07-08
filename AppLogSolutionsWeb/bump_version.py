import os
import re

root = 'frontend'

with open(os.path.join(root, 'script.js'), 'r', encoding='utf-8') as f:
    c_script = f.read()

match = re.search(r'APP_VERSION\s*=\s*"([\d\.]+)"', c_script)
if match:
    v_old = float(match.group(1))
    if v_old < 5.85:
        v_new = '5.86'
    else:
        v_new = str(round(v_old + 0.01, 2))
else:
    v_new = '5.86'

print(f"Nuova versione calcolata: {v_new}")

with open(os.path.join(root, 'sw.js'), 'r', encoding='utf-8') as f:
    c_sw = f.read()
c_sw = re.sub(r'log-solution-v[\d\.]+', f'log-solution-v{v_new}', c_sw)
with open(os.path.join(root, 'sw.js'), 'w', encoding='utf-8') as f:
    f.write(c_sw)

c_script = re.sub(r'APP_VERSION\s*=\s*"[\d\.]+"', f'APP_VERSION = "{v_new}"', c_script)
with open(os.path.join(root, 'script.js'), 'w', encoding='utf-8') as f:
    f.write(c_script)

htmls = [f for f in os.listdir(root) if f.endswith('.html')]
for h in htmls:
    p = os.path.join(root, h)
    with open(p, 'r', encoding='utf-8') as f:
        c_h = f.read()
    c_h = re.sub(r'\?v=[\d\.]+', f'?v={v_new}', c_h)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c_h)

# 7. Aggiorna eventuali riferimenti ?v= negli altri script JS
js_files = [f for f in os.listdir(root) if f.endswith('.js') and f not in ['script.js', 'sw.js']]
for js_file in js_files:
    p = os.path.join(root, js_file)
    with open(p, 'r', encoding='utf-8') as f:
        c_js = f.read()
    c_js = re.sub(r'\?v=[\d\.]+', f'?v={v_new}', c_js)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c_js)

print(f"Versione bumpata a {v_new}")
