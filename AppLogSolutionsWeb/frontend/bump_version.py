import glob
for f in glob.glob('G:/Il mio Drive/App/AppLogSolutions/frontend/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = content.replace('?v=1.36', '?v=1.37')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
