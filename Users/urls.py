from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserView, UserViewSet

router = DefaultRouter()
router.register(r'Users', UserViewSet)  # Register the UserViewSet

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUserView.as_view(), name='register'),
]