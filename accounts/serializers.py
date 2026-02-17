from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, UserProfile, WorkerDocument, WorkerProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "user_type",
            "profile_picture",
            "is_verified",
            "date_joined",
        )
        read_only_fields = ("id", "is_verified", "user_type", "date_joined")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
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
        validated_data.pop("password2")

        email = validated_data["email"].lower()
        password = validated_data.pop("password")

        base_username = email.split("@")[0]
        username = base_username
        counter = 1

        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=validated_data["phone_number"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            user_type=CustomUser.Choice.USER,
        )
        UserProfile.objects.create(user=user)

        return user


class BecomeWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerProfile
        fields = (
            "service_category",
            "skills",
            "bio",
            "hourly_rate",
            "service_latitude",
            "service_longitude",
            "service_radius_km",
        )

    def create(self, validated_data):
        user = self.context["request"].user

        if user.user_type == CustomUser.Choice.ADMIN:
            raise serializers.ValidationError("Admin cannot become worker.")

        if hasattr(user, "worker_profile"):
            raise serializers.ValidationError("Worker profile already exists.")

        worker_profile = WorkerProfile.objects.create(worker=user, **validated_data)

        user.user_type = CustomUser.Choice.WORKER
        user.save(update_fields=["user_type"])

        return worker_profile


class WorkerDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerDocument
        fields = (
            "id",
            "document_type",
            "document_number",
            "document_file",
            "uploaded_at",
        )
        read_only_fields = ["id", "uploaded_at"]

    def create(self, validated_data):
        user = self.context["request"].user

        if not hasattr(user, "worker_profile"):
            raise serializers.ValidationError("Create worker profile first.")

        if user.user_type != CustomUser.Choice.WORKER:
            raise serializers.ValidationError("Only workers can upload documents.")

        return WorkerDocument.objects.create(
            worker_profile=user.worker_profile, **validated_data
        )
