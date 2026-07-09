import sys
import re

filepath = r"G:\Il mio Drive\App\AppLogSolutionsWeb\functions\main.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace drag-handle inline style
target_handle = """<div class="drag-handle" style="color:#94a3b8; cursor:grab; display:flex; align-items:center; justify-content:center;" onclick="event.stopPropagation()">"""
injection_handle = """<div class="drag-handle" style="color:#94a3b8; cursor:grab; display:flex; align-items:center; justify-content:center; touch-action:none;" onclick="event.stopPropagation()">"""
content = content.replace(target_handle, injection_handle)

# Replace SortableJS init
target_sortable = """        new Sortable(list, {{
            handle: ".drag-handle",
            animation: 150,
            onEnd: function(evt) {{"""

injection_sortable = """        new Sortable(list, {{
            handle: ".drag-handle",
            animation: 150,
            delay: 150,
            delayOnTouchOnly: true,
            fallbackTolerance: 3,
            onEnd: function(evt) {{"""

content = content.replace(target_sortable, injection_sortable)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
