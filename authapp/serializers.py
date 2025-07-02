from rest_framework import serializers

class InscriptionSerializer(serializers.Serializer):
    prenom = serializers.CharField(max_length=100)
    nom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    mot_de_passe = serializers.CharField(write_only=True, min_length=6)
    role = serializers.CharField(default="patient", required=False)

    def validate_role(self, value):
        allowed_roles = ["patient", "medecin", "admin"]  # adapte selon tes rôles
        if value not in allowed_roles:
            raise serializers.ValidationError("Role invalide.")
        return value