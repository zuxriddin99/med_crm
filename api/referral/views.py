import datetime
import time

from django.db.models import Q
from rest_framework import permissions, generics
from rest_framework.response import Response

from api.referral import serializers
from api.views import CustomListView
from apps.client.models import Client
from apps.reception.models import ReferralPerson
from core.pagination import CustomPagination


class ReferralPersonShortListAPIView(CustomListView):
    queryset = ReferralPerson.objects.all()
    serializer_class = serializers.ReferralPersonShortListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        q_filter = Q()
        if search:
            q_filter = Q(full_name__icontains=search)
            if search.isdigit():
                q_filter |= Q(id=search)
        queryset = ReferralPerson.objects.filter(q_filter).order_by('-updated_at')
        data = self.get_response_data(self.serializer_class, queryset, many=True)
        return Response(data)
