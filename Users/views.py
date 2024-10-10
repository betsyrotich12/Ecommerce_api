from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
         """
        Set permissions for each action:
        - List and Retrieve: Admin users can view users.
        - Create, Update, Delete: Only authenticated users can manage users.
        """
         if self.action in ['list', 'retrieve']:
              self.permission_classes = [IsAdminUser]

         else:
              self.permission_classes = [IsAuthenticated]
         
         return super().get_permissions()
    
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class CustomTokenObtainPairView(APIView):

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             # Create a new token for the user
#             refresh = RefreshToken.for_user(user)

#             # Redirect to homepage after successful login
#             response = redirect('/')
#             response.set_cookie('access', str(refresh.access_token))
#             response.set_cookie('refresh', str(refresh))

#             return response
#         else:
#             return Response({"error": "Invalid credentials"}, status=401)