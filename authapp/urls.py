from django.urls import path
from .views import inscription, profil_utilisateur, diagnose_from_ia, views
urlpatterns = [
    path('inscription/', inscription, name='inscription'),
    path('profil/', profil_utilisateur, name='profil_utilisateur'),
    path('ia/diagnosis/', views.relay_diagnosis),
    path('ia/feedback/', views.relay_feedback),
    path('ia/monitoring/', views.relay_monitoring),
]