from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser, UserProfile, WorkerDocument, WorkerProfile
from .serializers import (
    UserProfileSerializer,
    UserSerializer,
    RegisterSerializer,
    WorkerDocumentSerializer,
    BecomeWorkerSerializer,
    WorkerProfileSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.user_profile


class BecomeWorkerView(generics.CreateAPIView):
    serializer_class = BecomeWorkerSerializer
    permission_classes = [IsAuthenticated]
    queryset = WorkerProfile.objects.all()


class WorkerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = WorkerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user

        if not hasattr(user, "worker_profile"):
            return None
        return user.worker_profile

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return Response(
                {"detail": "Worker profile not found. Become a worker first."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(self.get_serializer(obj).data)


class WorkerDocumentListView(generics.ListAPIView):
    serializer_class = WorkerDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not hasattr(user, "worker_profile"):
            return WorkerDocument.objects.none()

        return WorkerDocument.objects.filter(worker_profile=user.worker_profile)


class WorkerDocumentUploadView(generics.CreateAPIView):
    serializer_class = WorkerDocumentSerializer
    permission_classes = [IsAuthenticated]
    queryset = WorkerDocument.objects.all()
    parser_classes = [MultiPartParser, FormParser]


class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response(
            {"message": "Account deleted successfully"}, status=status.HTTP_200_OK
        )
