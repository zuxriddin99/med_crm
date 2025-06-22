from django.urls import include, path

app_name = "api"
urlpatterns = [
    path("reception/", include("api.reception.urls", namespace="reception")),
    path("client/", include("api.client.urls", namespace="client")),
    path("referral/", include("api.referral.urls", namespace="referral")),
]
