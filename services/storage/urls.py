from django.urls import path, include
from storage.views import FileUploadAPIView, UserAPIView, RefreshAPIView, RecipeAnalyzeAPIView

urlpatterns = [
    path('upload/', FileUploadAPIView.as_view(), name='Uploader'),
    path('login/', UserAPIView.as_view(), name='UserAPI'),
    path('refresh/', RefreshAPIView.as_view(), name='RefreshToken'),
    path('analyze/', RecipeAnalyzeAPIView.as_view(), name='RecipeAnalyze'),
]