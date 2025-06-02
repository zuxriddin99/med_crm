from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import generic

from apps.staff.models import StaffUser
from webapp.auth import forms

class MainPageView(generic.TemplateView):
    template_name = "index.html"