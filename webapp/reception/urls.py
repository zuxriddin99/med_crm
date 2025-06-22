from django.urls import include, path
from django.contrib.auth.views import LogoutView

from webapp.auth.views import AuthView, logout_view
from webapp.reception.views import MainPageView, ReceptionPageView

app_name = "reception"
urlpatterns = [
    path("", MainPageView.as_view(), name="main"),
    path("list/", ReceptionPageView.as_view(), name="list"),
]
