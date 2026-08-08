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
