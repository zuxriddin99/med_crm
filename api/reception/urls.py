from django.urls import include, path

from api.reception.views import VisitListAPIView

app_name = "reception"
urlpatterns = [
    path("list/", VisitListAPIView.as_view(), name="list"),
]
