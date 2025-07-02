from rest_framework import authentication
from firebase_admin import auth as firebase_auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import AbstractBaseUser

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        print("🔐 Authorization reçu :", auth_header)

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        id_token = auth_header.split(' ')[1]

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token.get("uid")
            print("✅ Token Firebase vérifié. UID :", uid)
        except Exception as e:
            print("❌ Erreur Firebase :", str(e))
            raise AuthenticationFailed("Token invalide ou expiré")

        if not uid:
            raise AuthenticationFailed("UID manquant dans le token")

        user = FirebaseUser(uid=uid)
        return (user, uid)
class FirebaseUser(AbstractBaseUser):
    def __init__(self, uid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid = uid

    @property
    def is_authenticated(self):
        return True
