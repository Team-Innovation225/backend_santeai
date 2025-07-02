from rest_framework import authentication, exceptions
from firebase_admin import auth as firebase_auth
#

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        if not auth_header.startswith('Bearer '):
            raise exceptions.AuthenticationFailed('Format Authorization invalide.')

        id_token = auth_header.split(' ')[1]

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.AuthenticationFailed('Token invalide ou expiré.')

        uid = decoded_token.get('uid')
        if not uid:
            raise exceptions.AuthenticationFailed('Token invalide: pas de UID.')

        # Retourne un tuple (user, auth), ici user = None, auth = uid
        return (None, uid)

