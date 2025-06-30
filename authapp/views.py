from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .firebase  import db, auth 
import datetime

status =["patient","medecin"]
@csrf_exempt
def inscription(request):
    if request.method == 'POST':
        data=request.POST 
        try:
            role= data.get('role','patient').lower()
            if role not in status:
                return JsonResponse({'erreur': 'role invalide'}, status=400)

            utilisateur = auth.create_user(email=data['email'], password=data['password'], display_name=f"{data['nom']} {data['prenom']}")
            document = {
                'uid': utilisateur .uid,
                'nom': data['nom'],
                'prenom': data['prenom'],
                'email': data['email'],
                'role': role,
                "date creation": datetime.datetime.utcnow().isoformat(),
            }
            db.collection('utilisateurs').document(utilisateur.uid).set(document)
            return JsonResponse({'message': 'Utilisateur créé avec succès', 'uid': utilisateur.uid})
        except Exception as e:
            return JsonResponse({'erreur': str(e)}, status=400)
    return JsonResponse({'message': 'Méthode non autorisée'}, status=405)