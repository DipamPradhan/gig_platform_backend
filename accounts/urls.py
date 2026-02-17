from django.urls import path
from .views import (
    DeleteUserView,
    MeView,
    RegisterView,
    BecomeWorkerView,
    UserProfileView,
    WorkerDocumentListView,
    WorkerDocumentUploadView,
    WorkerProfileView,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="user"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("become-worker/", BecomeWorkerView.as_view(), name="become_worker"),
    path("worker/profile/", WorkerProfileView.as_view(), name="worker_profile"),
    path(
        "worker/documents/", WorkerDocumentListView.as_view(), name="worker_documents"
    ),
    path(
        "worker/documents/upload/",
        WorkerDocumentUploadView.as_view(),
        name="upload_document",
    ),
    path("profile/delete/", DeleteUserView.as_view(), name="profile_delete"),
]
