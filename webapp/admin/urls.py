from django.urls import path

from webapp.reception.views import MainPageView

app_name = "doctor"
urlpatterns = [
    path("", MainPageView.as_view(), name="main"),
]
