import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(r"C:\Users\Diego\Documents\antigravity\elegant-goodall\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

viaggi_ref = db.collection('clienti').document('DNR').collection('viaggi ddt')
query = viaggi_ref.stream()

dates = set()
for v in query:
    dates.add(v.to_dict().get("data_lavoro"))

for d in sorted(list(dates)):
    if d and "-07-" in d:
        print(f"Trovata data di luglio: {d}")
    if d and ("-7-" in d or "/07/" in d or "/7/" in d):
        print(f"Trovata data anomala: {d}")

print("Tutte le date:")
print(sorted(list(dates))[-20:])
