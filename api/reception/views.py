import datetime
import time

from django.db.models import Q
from rest_framework import permissions, generics
from rest_framework.response import Response

from api.reception import serializers
from api.views import CustomListView
from apps.reception.models import Visit
from core.pagination import CustomPagination


class VisitListAPIView(CustomListView):
    queryset = Visit.objects.all()
    serializer_class = serializers.VisitListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        branch_id = request.session.get("branch_id")
        search = request.GET.get('search')
        q_filter = Q()
        if search:
            q_filter = Q(Q(client__first_name__icontains=search) | Q(client__last_name__icontains=search))
        if branch_id:
            q_filter &= Q(branch_id=branch_id)
        queryset = Visit.objects.filter(q_filter).order_by('-updated_at')
        data = self.get_response_data(self.serializer_class, queryset, many=True)
        return Response(data)
