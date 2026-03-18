import firebase_admin
from firebase_admin import credentials, auth

key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    firebase_admin.initialize_app(credentials.Certificate(key_path))

def verify_all_existing_users():
    # Recupera tutti gli utenti
    page = auth.list_users()
    count = 0
    while page:
        for user in page.users:
            if not user.email_verified:
                auth.update_user(user.uid, email_verified=True)
                print(f"Utente {user.email} (UID: {user.uid}) impostato come VERIFICATO.")
                count += 1
        page = page.get_next_page()
    
    print(f"\nOperazione completata. {count} utenti verificati manualmente.")

if __name__ == "__main__":
    verify_all_existing_users()
