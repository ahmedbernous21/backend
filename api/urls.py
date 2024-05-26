from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ContactInfoViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TestViewSet, FileViewSet, CategoryViewSet, FaqViewSet, SpecialtyViewSet


router = DefaultRouter()
router.register(r'contact-info', ContactInfoViewSet)
router.register(r'tests', TestViewSet)
router.register(r'files', FileViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'faqs', FaqViewSet)
router.register(r'specialties', SpecialtyViewSet)



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
    path('', include(router.urls)),

]

