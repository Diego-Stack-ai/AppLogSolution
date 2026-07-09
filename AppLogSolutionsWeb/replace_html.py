import re
import codecs

filepath = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend\gestione_anomalie.html"

with codecs.open(filepath, 'r', 'utf-8') as f:
    content = f.read()

# Replace 1:
content = content.replace(
    "id=\"cli-${id}-codF\" value=\"${(d.tipo === 'FRUTTA' || d.tipo === 'GRAND CHEF' || tenant === 'GRAN CHEF') ? id : 'p00000'}\">",
    "id=\"cli-${id}-codF\" value=\"${(d.tipo === 'FRUTTA' || d.tipo === 'GRAND CHEF' || tenant === 'GRAN CHEF' || d.tipo === 'CATTEL' || tenant === 'CATTEL') ? id : 'p00000'}\">"
)

# Replace 2:
content = content.replace(
    "Frutta: ${c.codice_frutta || 'p00000'}",
    "Frutta: ${c.codice_frutta !== 'p00000' ? c.codice_frutta : 'p00000'}"
)

# Replace 3:
content = content.replace(
    "codice_frutta: (d.tipo === 'FRUTTA' || d.tipo === 'GRAND CHEF' || d.tipo === 'CATTEL') ? id : 'p00000',",
    "codice_frutta: (d.tipo === 'FRUTTA' || d.tipo === 'GRAND CHEF' || d.tipo === 'CATTEL') ? id : 'p00000',"
)

content = content.replace(
    "codice_frutta: d.tipo === 'FRUTTA' ? id : 'p00000',",
    "codice_frutta: (d.tipo === 'FRUTTA' || d.tipo === 'GRAND CHEF' || d.tipo === 'CATTEL') ? id : 'p00000',"
)

with codecs.open(filepath, 'w', 'utf-8') as f:
    f.write(content)

print("Done replacing in html")
