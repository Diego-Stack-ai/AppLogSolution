import re

with open('functions/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

collections = re.findall(r'collection\([\'"]([^\'"]+)[\'"]\)', text)
documents = re.findall(r'document\([\'"]([^\'"]+)[\'"]\)', text)
buckets = re.findall(r'bucket\.blob\([\'"]([^\'"]+)[\'"]\)', text)
prefixes = re.findall(r'prefix=[\'"]([^\'"]+)[\'"]', text)

print('Collections:', set(collections))
print('Documents:', set(documents))
print('Blobs:', set(buckets))
print('Prefixes:', set(prefixes))
