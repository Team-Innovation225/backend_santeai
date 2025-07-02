from django.urls import path
from .views import inscription, profil_utilisateur
urlpatterns = [
    path('inscription/', inscription, name='inscription'),
    path('profil/', profil_utilisateur, name='profil_utilisateur'),
]