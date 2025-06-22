from django.urls import include, path

from api.referral.views import ReferralPersonShortListAPIView

app_name = "referral"
urlpatterns = [
    path("person-short/list/", ReferralPersonShortListAPIView.as_view(), name="person-short-list"),
]
