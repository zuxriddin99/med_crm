from rest_framework import serializers

from apps.reception.models import Visit


class VisitListSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='client.formated_phone_number', read_only=True)

    class Meta:
        model = Visit
        fields = ["id", "client_full_name", "is_completed", "created_at_str", "phone_number"]
