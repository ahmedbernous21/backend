from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import viewsets

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

)

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication  # Or use your authentication method
from rest_framework.views import APIView



from api.models import User, ContactMessage, BloodFormSubmission, ContactInfo, Test, File, Category, Faq, Specialty

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render

import json


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


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


@api_view(["GET", "POST"])
def handle_contact_form(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        sujet = data.get("sujet")
        message = data.get("message")
        print("name", name)
        print("email", email)
        print("phone", phone)
        print("sujet", sujet)
        print("message", message)

        ContactMessage.objects.create(
            name=name, email=email, phone=phone, sujet=sujet, message=message
        )

        return JsonResponse({"message": "Form submitted successfully!"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


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

class BloodFormSubmissionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BloodFormSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
