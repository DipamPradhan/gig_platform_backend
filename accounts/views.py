from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser, UserProfile, WorkerDocument, WorkerProfile
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    WorkerDocumentSerializer,
    BecomeWorkerSerializer,
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


class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class BecomeWorkerView(generics.CreateAPIView):
    serializer_class = BecomeWorkerSerializer
    permission_classes = [IsAuthenticated]
    queryset = WorkerProfile.objects.all()


class WorkerDocumentUploadView(generics.CreateAPIView):
    serializer_class = WorkerDocumentSerializer
    permission_classes = [IsAuthenticated]
    queryset = WorkerDocument.objects.all()
    parser_classes = [MultiPartParser, FormParser]
