from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import viewsets

from api.serializer import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    ContactInfoSerializer

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


from api.models import User, ContactMessage, BloodFormSubmission, ContactInfo

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

@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])  # Adjust based on your authentication method
def submit_blood_form(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        email = data.get("email")
        address = data.get("address")
        phone = data.get("phone")
        appointment_date = data.get("appointmentDate")
        message = data.get("message")

        print("message", message)
        print("first_name", first_name)

        prescription = None
        if "prescription" in request.FILES:
            prescription = request.FILES["prescription"]

        BloodFormSubmission.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            phone=phone,
            appointment_date=appointment_date,
            message=message,
            prescription=prescription,
        )

        return JsonResponse({"message": "Form submitted successfully!"}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)


class ContactInfoViewSet(viewsets.ModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
