# products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, AddToWishlistView, RemoveFromWishlistView
from .views import ProductListView, CreateOrderView

router = DefaultRouter()
router.register(r'Products', ProductViewSet)
router.register(r'Categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('wishlist/add/<int:product_id>/', AddToWishlistView.as_view(), name='add-to-wishlist'),
    path('wishlist/remove/<int:product_id>/', RemoveFromWishlistView.as_view(), name='remove-from-wishlist'),
    path('order/<int:product_id>/', CreateOrderView.as_view(), name='create-order'),
    path('products_list/', ProductListView.as_view(), name='Products List'),
]

