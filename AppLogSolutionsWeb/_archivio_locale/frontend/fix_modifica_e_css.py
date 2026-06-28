import re

file_path = r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix CSS classes
content = content.replace('.modal-overlay {', '.presenze-modal-overlay {')
content = content.replace('class="modal-overlay"', 'class="presenze-modal-overlay"')
content = content.replace('.modal-box {', '.presenze-modal-box {')
content = content.replace('class="modal-box"', 'class="presenze-modal-box"')

# Fix toggleRowEdit
old_toggle = r"""            if (btn.innerText.includes('Modifica')) {"""
new_toggle = r"""            if (btn.innerText.includes('Mod')) {"""
content = content.replace(old_toggle, new_toggle)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Applied fixes for Modifica and Modal CSS conflict!")
