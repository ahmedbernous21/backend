from api.models import User, BloodFormSubmission
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "phone_number", "address")


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # These are claims, you can add custom claims
        token["full_name"] = user.profile.full_name
        token["username"] = user.username
        token["email"] = user.email
        token["phone_number"] = user.phone_number
        token["address"] = user.address
        token["bio"] = user.profile.bio
        token["image"] = str(user.profile.image)
        token["verified"] = user.profile.verified
        # ...
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "phone_number",
            "address",
            "password",
            "password2",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            address=validated_data["address"],
            phone_number=validated_data["phone_number"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
