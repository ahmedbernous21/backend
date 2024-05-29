from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ContactInfoViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    TestViewSet,
    FileViewSet,
    CategoryViewSet,
    FaqViewSet,
    SpecialtyViewSet,
    BloodFormSubmissionViewSet,
    AppointmentViewSet,
    ContactMessageViewSet,
)


router = DefaultRouter()
router.register(r"contact-info", ContactInfoViewSet)
router.register(r"tests", TestViewSet)
router.register(r"files", FileViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"faqs", FaqViewSet)
router.register(r"specialties", SpecialtyViewSet)
router.register(r"bloodformsubmissions", BloodFormSubmissionViewSet)
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r"contact", ContactMessageViewSet)



urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterView.as_view(), name="auth_register"),
    path("test/", views.testEndPoint, name="test"),
    path("", views.getRoutes),
    path(
        "send-response/<int:message_id>/",
        views.send_response_email,
        name="send_response_email",
    ),
    path("", include(router.urls)),
]
