import glob

for f in glob.glob('frontend/*.html'):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        content = content.replace('?v=5.60', '?v=5.61')
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error processing {f}: {e}")
