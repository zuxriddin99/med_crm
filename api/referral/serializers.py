from rest_framework import serializers

from apps.reception.models import ReferralPerson


class ReferralPersonShortListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralPerson
        fields = [
            "id",
            "full_name",
        ]

