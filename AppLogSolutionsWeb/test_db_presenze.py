import firebase_admin
from firebase_admin import credentials, firestore
import collections

def main():
    cred = credentials.Certificate('prod_key.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    docs = db.collection('presenze').limit(2000).stream()
    clienti_counter = collections.Counter()
    
    for doc in docs:
        s = doc.to_dict()
        cliente = s.get('cliente', '')
        if cliente:
            clienti_counter[cliente] += 1
            
    print("\nTop Clienti salvati in presenze:")
    print(clienti_counter.most_common(10))
    
    # Ora guardiamo pianificazione_viaggi
    pian_docs = db.collection('clienti').document('DNR').collection('pianificazione_viaggi').limit(10).stream()
    print("\nEsempio pianificazione_viaggi:")
    count = 0
    for doc in pian_docs:
        print(f"Data: {doc.id}")
        data = doc.to_dict()
        assegnazioni = data.get('assegnazioni', [])
        print(f" Assegnazioni: {len(assegnazioni)}")
        if len(assegnazioni) > 0:
            print(f"  Esempio assegnazione: {assegnazioni[0]}")
        count += 1
        
    print(f"Trovati {count} documenti in pianificazione_viaggi")

if __name__ == '__main__':
    main()
