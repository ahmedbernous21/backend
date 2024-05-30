from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import viewsets, permissions

from api.serializer import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    ContactInfoSerializer,
    TestSerializer,
    FileSerializer,
    CategorySerializer,
    FaqSerializer,
    SpecialtySerializer,
    BloodFormSubmissionSerializer,
    AppointmentSerializer,
    ContactMessageSerializer,
)

from rest_framework.decorators import api_view, permission_classes


from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str  # Use force_str here
from django.contrib.auth.tokens import default_token_generator
from .email import send_confirmation_email
from api.models import (
    User,
    ContactMessage,
    BloodFormSubmission,
    ContactInfo,
    Test,
    File,
    Category,
    Faq,
    Specialty,
    Appointment,
)

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render

import json


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_confirmation_email(user)
        return user

# Get All Routes
# api/views.py


def home(request):
    return HttpResponse("Welcome to the API homepage.")


@api_view(["GET"])
def getRoutes(request):
    routes = ["/api/token/", "/api/register/", "/api/token/refresh/"]
    return Response(routes)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == "GET":
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({"response": data}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        text = "Hello buddy"
        data = (
            f"Congratulation your API just responded to POST request with text: {text}"
        )
        return Response({"response": data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)

    
class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset =  ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def send_response_email(request, message_id):
    message = get_object_or_404(ContactMessage, pk=message_id)

    if request.method == "POST":
        response = request.POST.get("response")

        send_mail(
            "Response to Your Message",
            response,
            "admin@example.com",
            [message.email],
            fail_silently=False,
        )

        message.responded = True
        message.save()

        return JsonResponse({"message": "Response sent successfully!"})
    else:
        return render(request, "response_form.html")


class ContactInfoViewSet(viewsets.ModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FaqViewSet(viewsets.ModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class BloodFormSubmissionViewSet(viewsets.ModelViewSet):
    queryset = BloodFormSubmission.objects.all()
    serializer_class = BloodFormSubmissionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConfirmUserEmailView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_confirmed = True
            user.save()
            return render(request, 'confirmation_success.html')
        else:
            return render(request, 'confirmation_failed.html')