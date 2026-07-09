import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate(r"C:\Users\Diego\Documents\antigravity\elegant-goodall\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json")
firebase_admin.initialize_app(cred)
bucket = storage.bucket(name="log-solution-60007.appspot.com")

print("Files in DDT_ESTRATTI for 07-07-2026:")
blobs = bucket.list_blobs(prefix="split_ddt/07-07-2026/")
for b in blobs:
    print(b.name)
    
print("\nFiles in DDT_ESTRATTI for 07-06-2026:")
blobs2 = bucket.list_blobs(prefix="split_ddt/07-06-2026/")
for b2 in blobs2:
    print(b2.name)
    
print("\nFiles in DDT_ORIGINALI recenti:")
for b3 in bucket.list_blobs(prefix="DDT_ORIGINALI/"):
    if "2026" in b3.name: # Just check if there's anything recent
        pass
