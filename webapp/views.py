import datetime
import locale

from rest_framework import mixins, viewsets, generics
from rest_framework.serializers import Serializer
from django.views import generic
from django.contrib.auth.mixins import AccessMixin

from apps.staff.models import StaffUser


class LoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    login_url = 'web:auth:login'
    permission_denied_message = "Sizda bu saxifaga kirishga ruxsat yo'q."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.has_department(request.user):
            return self.handle_no_permission()
        if not self.has_access_department(request):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def has_department(self, user: StaffUser):
        return bool(user.branch_id)

    def has_access_department(self, request):
        req_branch_id = request.session['branch_id']
        user_branch_id = request.user.branch_id
        return req_branch_id == user_branch_id


class TestView(generic.TemplateView):
    template_name = 'index.html'
