import firebase_admin
from firebase_admin import credentials, auth, firestore

key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    firebase_admin.initialize_app(credentials.Certificate(key_path))

db = firestore.client()

utenti = [
  { "nome": "Berradia Ayoub", "email": "ayoubberradia@gmail.com", "password": "324997" },
  { "nome": "Bundo Gerti", "email": "gertibundo1@gmail.com", "password": "351943" },
  { "nome": "Sirbu Catalin", "email": "eucatalin0405@gmail.com", "password": "329664" },
  { "nome": "Mingotto Cristiano", "email": "cristianomingotto69@gmail.com", "password": "347273" },
  { "nome": "Doda Viktor", "email": "viktordoda91@gmail.com", "password": "334271" },
  { "nome": "El Oualladi Aziz", "email": "azizeloualladi@gmail.com", "password": "351716" },
  { "nome": "Jurcau Florin Rares", "email": "jurcauflorin02@gmail.com", "password": "328337" },
  { "nome": "Shuperka Leonard", "email": "Leonard.ms82@gmail.com", "password": "320355" },
  { "nome": "Daboussi Mohamed", "email": "daboussi180@gmail.com", "password": "379252" },
  { "nome": "Shehu Elmas", "email": "shehupadova@gmail.com", "password": "380582" },
  { "nome": "Shqypi Orgito", "email": "orgitoshqypi14@gmail.com", "password": "328441" },
  { "nome": "Ahmed Sufyan", "email": "sufyanahmed01111996@gmail.com", "password": "350585" },
  { "nome": "Skarbinet Vasyl", "email": "ppanteleimon6@gmail.com", "password": "380868" },
  { "nome": "Xheka Jona", "email": "jona.xheka@gmail.com", "password": "345114" },
  { "nome": "Racovita Doina", "email": "racovita.doina@yahoo.it", "password": "123124" }
]

def create_users():
    for u in utenti:
        try:
            # Check if user already exists
            try:
                user = auth.get_user_by_email(u["email"])
                print(f"Utente {u['nome']} ({u['email']}) esiste gia' con UID {user.uid}")
                uid = user.uid
                # Optional: Update password
                # auth.update_user(uid, password=u["password"])
            except auth.UserNotFoundError:
                user = auth.create_user(
                    email=u["email"],
                    password=u["password"],
                    display_name=u["nome"]
                )
                print(f"Creato utente {u['nome']} con UID {user.uid}")
                uid = user.uid

            # Update Firestore
            # We follow the convention: Document ID = UID
            doc_ref = db.collection('users').document(uid)
            doc_ref.set({
                "nome": u["nome"],
                "email": u["email"],
                "uid": uid,
                "ruolo": "autista",
                "tipoTurno": "giornata" # default
            }, merge=True)
            print(f"Documento Firestore {uid} aggiornato per {u['nome']}")

        except Exception as e:
            print(f"Errore per {u['nome']}: {e}")

if __name__ == "__main__":
    create_users()
