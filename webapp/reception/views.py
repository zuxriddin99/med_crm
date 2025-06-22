from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import generic

from apps.staff.models import StaffUser
from webapp.auth import forms
from webapp.views import LoginRequiredMixin


class MainPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "reception/main.html"

    def get(self, request, *args, **kwargs):
        print(request.session['branch_id'])
        return render(request, self.template_name)

class ReceptionPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "reception/list.html"
