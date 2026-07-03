import re

with open('frontend/firebase-auth-sync.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the tenant selector code block
content = re.sub(r'// --- GESTIONE TENANT \(SELETTORE LOCALE\) ---.*?(?=\n// --- GESTIONE EMERGENZA)', '', content, flags=re.DOTALL)
content = re.sub(r'// --- GESTIONE TENANT \(SELETTORE GLOBALE\) ---.*?(?=\n// --- GESTIONE EMERGENZA)', '', content, flags=re.DOTALL)

with open('frontend/firebase-auth-sync.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
