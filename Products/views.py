# products/views.py
from rest_framework import viewsets
from .models import Products, Category, Wishlist, Order
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category_name']
    ordering_fields = ['price', 'created_at']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductListView(ListAPIView):
    queryset = Products.objects.all()  # Fetch all products
    serializer_class = ProductSerializer  

class AddToWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = Products.objects.get(id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if created:
            return Response({"message": "Product added to wishlist."}, status=201)
        return Response({"message": "Product is already in your wishlist."}, status=200)

class RemoveFromWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = Products.objects.get(id=product_id)
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

        if wishlist_item:
            wishlist_item.delete()
            return Response({"message": "Product removed from wishlist."}, status=200)
        return Response({"message": "Product not found in wishlist."}, status=404)
    
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = Products.objects.get(id=product_id)
        quantity = int(request.data.get('quantity'))

        # Ensure stock is sufficient
        if product.stock < quantity:
            return Response({"error": "Not enough stock available."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate total price
        total_price = product.price * quantity

        # Create the order
        order = Order.objects.create(user=request.user, product=product, quantity=quantity, total_price=total_price)
        
        # Reduce stock
        product.stock -= quantity
        product.save()

        return Response({"message": "Order placed successfully."}, status=status.HTTP_201_CREATED)

