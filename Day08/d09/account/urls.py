from django.urls import path
from .views import LoginView, getUsername, logout, updateCSRFToken



urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("getUsername/", getUsername, name="getUsername"),
    path("logout/", logout, name="logout"),
    path("updateCRSFToken/", updateCSRFToken, name="updateCRSFToken"),
]