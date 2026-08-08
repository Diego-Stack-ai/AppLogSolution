import logging
from firebase_functions import https_fn
from infrastructure.firebase_setup import get_db

logger = logging.getLogger(__name__)

def handle_admin_reset_password(req: https_fn.CallableRequest) -> dict:
    """
    Cloud Function invocabile solo dagli amministratori per reimpostare la password di un altro utente.
    """
    try:
        from firebase_admin import auth
        import firebase_admin.auth
        db = get_db()
        
        caller_uid = req.auth.uid if req.auth else None
        if not caller_uid:
            raise https_fn.HttpsError(
                code=https_fn.FunctionsErrorCode.UNAUTHENTICATED,
                message="Utente non autenticato."
            )
            
        caller_doc = db.collection('dipendenti').document(caller_uid).get()
        if not caller_doc.exists:
            raise https_fn.HttpsError(
                code=https_fn.FunctionsErrorCode.PERMISSION_DENIED,
                message="Profilo amministratore non trovato."
            )
            
        caller_data = caller_doc.to_dict()
        if caller_data.get('ruolo', '').lower() != 'amministratore':
            raise https_fn.HttpsError(
                code=https_fn.FunctionsErrorCode.PERMISSION_DENIED,
                message="Solo un Amministratore può forzare il cambio password."
            )

        data = req.data
        target_email = data.get('email')
        new_password = data.get('newPassword')

        if not target_email or not new_password:
            raise https_fn.HttpsError(
                code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT,
                message="Email e nuova password sono obbligatori."
            )

        if len(new_password) < 6:
            raise https_fn.HttpsError(
                code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT,
                message="La password deve essere di almeno 6 caratteri."
            )

        try:
            user = auth.get_user_by_email(target_email)
        except firebase_admin.auth.UserNotFoundError:
            raise https_fn.HttpsError(
                code=https_fn.FunctionsErrorCode.NOT_FOUND,
                message=f"L'utente con email {target_email} non è stato trovato nel sistema di autenticazione Firebase. Assicurati che l'email sia corretta o che l'utente sia stato registrato correttamente."
            )
            
        # DEBITO TECNICO - NON MODIFICATO IN FASE 1B.1
        auth.update_user(user.uid, password=new_password)
        
        # Sblocchiamo anche l'utente nel caso fosse disabilitato o avesse needsPasswordChange
        db.collection('dipendenti').document(user.uid).update({
            'needsPasswordChange': False
        })

        return {
            "status": "success",
            "message": f"Password per {target_email} aggiornata con successo."
        }
        
    except https_fn.HttpsError as he:
        raise he
    except Exception as e:
        logger.error(f"Errore in admin_reset_password: {e}")
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.INTERNAL,
            message=str(e)
        )

import typing
from firebase_admin import firestore

@firestore.transactional
def _update_role_transaction(transaction, sys_status_ref, user_ref, action, target_uid, target_role, caller_uid):
    sys_status_doc = sys_status_ref.get(transaction=transaction)
    user_doc = user_ref.get(transaction=transaction)
    
    if not user_doc.exists:
        raise ValueError(f"L'utente {target_uid} non esiste nel database.")
        
    admins = sys_status_doc.to_dict().get('admins', []) if sys_status_doc.exists else []
    
    user_data = user_doc.to_dict()
    old_role = user_data.get('ruolo', 'sconosciuto')
    is_target_admin = (target_uid in admins) or (old_role == 'amministratore')
    
    if action == 'PROMOTE_ADMIN':
        if is_target_admin:
            raise ValueError(f"L'utente {target_uid} e' gia' un amministratore.")
        if target_uid not in admins:
            admins.append(target_uid)
        transaction.update(user_ref, {'ruolo': 'amministratore'})
        
    elif action in ('REVOKE_ADMIN', 'DELETE_USER', 'DISABLE_USER'):
        if is_target_admin:
            if len(admins) <= 1 and target_uid in admins:
                raise ValueError("Protezione ultimo amministratore: impossibile revocare o eliminare l'ultimo amministratore rimasto.")
            if target_uid in admins:
                admins.remove(target_uid)
                
        if action == 'REVOKE_ADMIN':
            if target_role not in ['autista', 'fornitore', 'impiegata', 'soel']:
                raise ValueError("Ruolo di destinazione per la revoca non valido.")
            transaction.update(user_ref, {'ruolo': target_role})
            
        elif action == 'DISABLE_USER':
            transaction.update(user_ref, {'disabled': True})
            
        elif action == 'DELETE_USER':
            transaction.delete(user_ref)
            
    else:
        raise ValueError("Azione non valida.")
        
    transaction.set(sys_status_ref, {'admins': admins}, merge=True)
    return old_role

def handle_admin_update_role(req: https_fn.CallableRequest) -> typing.Any:
    if not req.auth or not req.auth.uid:
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.UNAUTHENTICATED, message="Non autenticato")
        
    db = get_db()
    caller_uid = req.auth.uid
    
    caller_doc = db.collection('dipendenti').document(caller_uid).get()
    if not caller_doc.exists or caller_doc.to_dict().get('ruolo') != 'amministratore':
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.PERMISSION_DENIED, message="Privilegi insufficienti")
        
    data = req.data
    action = data.get('action')
    target_uid = data.get('targetUid')
    target_role = data.get('targetRole')
    
    if not action or not target_uid:
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message="Dati mancanti")
        
    sys_status_ref = db.collection('config').document('system_status')
    user_ref = db.collection('dipendenti').document(target_uid)
    
    transaction = db.transaction()
    
    try:
        old_role = _update_role_transaction(transaction, sys_status_ref, user_ref, action, target_uid, target_role, caller_uid)
        
        # Auth delete (solo per DELETE_USER)
        if action == 'DELETE_USER':
            from firebase_admin import auth
            try:
                auth.delete_user(target_uid)
            except Exception as e:
                print(f"Errore eliminazione Firebase Auth per {target_uid}: {e}")
                
        # Audit log
        audit_ref = db.collection('audit_logs_admin').document()
        audit_ref.set({
            'timestamp': firestore.SERVER_TIMESTAMP,
            'callerUid': caller_uid,
            'targetUid': target_uid,
            'action': action,
            'targetRole': target_role,
            'oldRole': old_role
        })
        
        return {"status": "success", "message": f"Azione {action} completata su {target_uid}"}
        
    except ValueError as ve:
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.FAILED_PRECONDITION, message=str(ve))
    except Exception as e:
        print(f"Errore in admin_update_role: {e}")
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INTERNAL, message=str(e))
