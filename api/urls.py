from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterView.as_view(), name="auth_register"),
    path("test/", views.testEndPoint, name="test"),
    path("", views.getRoutes),
    path("submit-form/", views.handle_contact_form, name="submit_form"),
    path(
        "send-response/<int:message_id>/",
        views.send_response_email,
        name="send_response_email",
    ),
    path("submit-blood-form/", views.submit_blood_form, name="submit_blood_form"),
]
