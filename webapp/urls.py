from django.urls import include, path

app_name = "webapp"
urlpatterns = [
    path("", include("webapp.auth.urls", namespace="auth")),
    path("reception/", include("webapp.reception.urls", namespace="reception")),
    path("doctor/", include("webapp.doctor.urls", namespace="doctor")),
    path("admin/", include("webapp.admin.urls", namespace="admin")),
    path("labaratory/", include("webapp.laboratory.urls", namespace="laboratory")),
]
