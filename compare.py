import filecmp
import os
import sys

def print_diff(dc, path=''):
    output = []
    has_content = False
    
    if dc.left_only:
        output.append(f"Soltanto in AppLogSolution: {', '.join(dc.left_only)}")
        has_content = True
    if dc.right_only:
        output.append(f"Soltanto in AppLogSolutions: {', '.join(dc.right_only)}")
        has_content = True
    if dc.diff_files:
        output.append(f"File modificati tra le due: {', '.join(dc.diff_files)}")
        has_content = True
        
    if has_content:
        print(f"\n--- {path or 'ROOT'} ---")
        for line in output:
            print(line)
            
    for sub in dc.subdirs:
        print_diff(dc.subdirs[sub], os.path.join(path, sub))

d1 = r'g:\Il mio Drive\App\AppLogSolution'
d2 = r'g:\Il mio Drive\App\AppLogSolutions'
dc = filecmp.dircmp(d1, d2, ignore=['.git', '.vscode', '__pycache__', 'node_modules', 'CONSEGNE', '.vercel', 'out', '.next'])
print_diff(dc)
