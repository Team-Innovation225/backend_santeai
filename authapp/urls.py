from django.urls import path
from .views import inscription
urlpatterns = [
    path('inscription/', inscription, name='inscription'),
]