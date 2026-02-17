from django.urls import path
from .views import RegisterView, UserView, BecomeWorkerView, WorkerDocumentUploadView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", UserView.as_view(), name="user"),
    path("become-worker/", BecomeWorkerView.as_view(), name="become_worker"),
    path(
        "worker/documents/upload/",
        WorkerDocumentUploadView.as_view(),
        name="upload_document",
    ),
]
