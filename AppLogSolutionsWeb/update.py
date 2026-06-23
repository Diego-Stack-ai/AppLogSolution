import os, re
for root, _, files in os.walk('frontend'):
    for file in files:
        if file.endswith('.html') or file.endswith('.js'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f: content = f.read()
                content = re.sub(r'v=\d+\.\d+', 'v=2.83', content)
                content = re.sub(r'log-solution-v\d+\.\d+', 'log-solution-v2.83', content)
                content = re.sub(r'APP_VERSION = \"\d+\.\d+\"', 'APP_VERSION = \"2.83\"', content)
                with open(path, 'w', encoding='utf-8') as f: f.write(content)
            except Exception as e: print(e)
