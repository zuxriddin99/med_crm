from django.urls import include, path

from api.client.views import ClientsListAPIView

app_name = "client"
urlpatterns = [
    path("list/", ClientsListAPIView.as_view(), name="list"),
]
