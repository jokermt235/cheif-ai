from django.urls import path, include
from storage.views  import (
    FileUploadAPIView,
    UserAPIView,
    RefreshAPIView,
)

urlpatterns = [
    path('/upload', FileUploadAPIView.as_view(), name='Uploader'),
    path('/login', UserAPIView.as_view(), name='UserAPI'),
    path('/refresh', RefreshAPIView.as_view(), name='RefreshToken'),
]
