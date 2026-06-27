import os, re, glob
v_old = ''
script_path = r'G:\Il mio Drive\App\AppLogSolutionsWeb\frontend\script.js'
with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()
    m = re.search(r'APP_VERSION\s*=\s*[\"\']([\d\.]+)[\"\']', content)
    v_old = m.group(1)

v_new = f'{float(v_old)+0.01:.2f}'
print(f'{v_old} -> {v_new}')

# Update script.js
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content.replace(f'\"{v_old}\"', f'\"{v_new}\"'))

# Update sw.js
sw_path = r'G:\Il mio Drive\App\AppLogSolutionsWeb\frontend\sw.js'
with open(sw_path, 'r', encoding='utf-8') as f:
    content = f.read()
with open(sw_path, 'w', encoding='utf-8') as f:
    f.write(re.sub(r'log-solution-v[\d\.]+', f'log-solution-v{v_new}', content))

# Update HTML files
for file in glob.glob(r'G:\Il mio Drive\App\AppLogSolutionsWeb\frontend\*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    html = re.sub(rf'\?v={v_old}', f'?v={v_new}', html)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)
