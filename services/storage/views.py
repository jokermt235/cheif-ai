from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from storage.serializers import LoginSerializer
from storage.backends import JWTAuthentication
from injector import inject
from storage.services import FileUploadService

class FileUploadAPIView(APIView):
  
  parser_classes = [MultiPartParser]
  permission_classes = [IsAuthenticated]
  
  @inject
  def __init__(self, service:FileUploadService):
    self.upload_service = service
  
  def post(self, request,format=None):
    file = None
    if 'file' in request.FILES:
      if request.FILES['file']:
        file = request.FILES['file']
        if file:
          return Response({"success" : self.upload_service.upload(file), "data" : {}}, status=status.HTTP_201_CREATED)

    return Response({"success" : False, "data" : {}}, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
  permission_classes = [AllowAny]
  serializer_class = LoginSerializer

  def post(self, request):
    email = request.data.get('email', '')
    password = request.data.get('password', '')
    serializer = self.serializer_class(data={'email' : email, 'password' : password})
    serializer.is_valid(raise_exception = True)

    return Response(serializer.data, status=status.HTTP_200_OK)

class RefreshAPIView(APIView):
  permission_classes = [IsAuthenticated]

  @inject
  def __init__(self, auth: JWTAuthentication):
    self.auth = auth

  def post(self, request):
    user,token = self.auth.authenticate(request)

    if user and token:
      return Response({"token" : user.token}, status=status.HTTP_200_OK)

    return Response({"message" : "Error"}, status=status.HTTP_400_BAD_REQUEST)


