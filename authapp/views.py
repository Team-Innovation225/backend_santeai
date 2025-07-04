from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .authentication import FirebaseAuthentication
from rest_framework.response import Response
from rest_framework import status
from .firebase import auth, db
from .serializers import InscriptionSerializer
import datetime
import requests
from django.http import JsonResponse
import json


def verifier_utilisateur_existe(email):
    try:
        auth.get_user_by_email(email)
        print(f"Compte Firebase déjà existant pour : {email}")
        return True
    except auth.UserNotFoundError:
        print(f"Aucun utilisateur Firebase pour : {email}")
        return False

def creer_utilisateur_firebase(data):
    return auth.create_user(
        email=data["email"],
        password=data["mot_de_passe"],
        display_name=f"{data['prenom']} {data['nom']}"
    )

def enregistrer_utilisateur_firestore(utilisateur, data, role):
    doc = {
        "uid": utilisateur.uid,
        "nom": data["nom"],
        "prenom": data["prenom"],
        "email": data["email"],
        "role": role,
        "photo_url": None,
        "date_creation": datetime.datetime.utcnow().isoformat()
    }
    db.collection("utilisateurs").document(utilisateur.uid).set(doc)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def inscription(request):
    serializer = InscriptionSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        role = data.get("role", "patient")
        email = data.get("email", "").strip()

        if not email:
            return Response({"error": "Email manquant ou vide"}, status=status.HTTP_400_BAD_REQUEST)

        if verifier_utilisateur_existe(email):
            return Response({"error": "Cet utilisateur existe déjà"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            utilisateur = creer_utilisateur_firebase(data)
            enregistrer_utilisateur_firestore(utilisateur, data, role)

            return Response(
                {"message": "Utilisateur inscrit avec succès", "uid": utilisateur.uid},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print("Erreur Firebase :", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([FirebaseAuthentication])
@permission_classes([IsAuthenticated])
def profil_utilisateur(request):
    uid = request.auth  
    return Response({"uid": uid, "message": "Accès autorisé"})

@csrf_exempt
def relay_diagnosis(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            response = requests.post(
                "http://localhost:8000/api/predict",  # ou l'URL de ton backend FastAPI
                json=data,
                timeout=10
            )
            return JsonResponse(response.json(), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def relay_feedback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            response = requests.post(
                "http://localhost:8000/api/feedback",
                json=data,
                timeout=10
            )
            return JsonResponse(response.json(), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def relay_monitoring(request):
    try:
        response = requests.get("http://localhost:8000/api/monitoring", timeout=10)
        return JsonResponse(response.json(), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
