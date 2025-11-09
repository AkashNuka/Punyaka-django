from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
import uuid
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer,
    OrderSerializer, CheckoutSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for product categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for products"""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by product type
        product_type = self.request.query_params.get('type', None)
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        
        # Featured products
        featured = self.request.query_params.get('featured', None)
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # In stock only
        in_stock = self.request.query_params.get('in_stock', None)
        if in_stock == 'true':
            queryset = queryset.filter(is_in_stock=True, stock__gt=0)
        
        return queryset


class CartViewSet(viewsets.ViewSet):
    """ViewSet for shopping cart"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """Get user's cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Check stock
        if product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        # Handle gift options
        if request.data.get('is_gift'):
            cart_item.is_gift = True
            cart_item.gift_message = request.data.get('gift_message', '')
            cart_item.add_gift_wrap = request.data.get('add_gift_wrap', False)
            cart_item.save()
        
        return Response({
            'message': 'Item added to cart',
            'cart': CartSerializer(cart).data
        })
    
    @action(detail=False, methods=['post'])
    def update_item(self, request):
        """Update cart item quantity"""
        cart = get_object_or_create(Cart, user=request.user)[0]
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity', 1))
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        if quantity <= 0:
            cart_item.delete()
            return Response({'message': 'Item removed from cart'})
        
        if cart_item.product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response({
            'message': 'Cart updated',
            'cart': CartSerializer(cart).data
        })
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Remove item from cart"""
        cart = Cart.objects.get(user=request.user)
        item_id = request.data.get('item_id')
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        return Response({
            'message': 'Item removed from cart',
            'cart': CartSerializer(cart).data
        })
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Clear cart"""
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        
        return Response({'message': 'Cart cleared'})


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for orders"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """Checkout and create order"""
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create order
        order = Order.objects.create(
            order_number=f"ORD-{uuid.uuid4().hex[:10].upper()}",
            user=request.user,
            shipping_address=serializer.validated_data['shipping_address'],
            shipping_city=serializer.validated_data['shipping_city'],
            shipping_state=serializer.validated_data['shipping_state'],
            shipping_pincode=serializer.validated_data['shipping_pincode'],
            shipping_phone=serializer.validated_data['shipping_phone'],
            subtotal=cart.get_total(),
            shipping_charge=50,  # Fixed shipping
            total_amount=cart.get_total() + 50,
            payment_status='paid'  # Demo: auto-mark as paid
        )
        
        # Create order items from cart
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_price=cart_item.product.get_price(),
                quantity=cart_item.quantity,
                is_gift=cart_item.is_gift,
                gift_message=cart_item.gift_message,
                has_gift_wrap=cart_item.add_gift_wrap
            )
            
            # Update stock
            product = cart_item.product
            product.stock -= cart_item.quantity
            if product.stock <= 0:
                product.is_in_stock = False
            product.save()
        
        # Clear cart
        cart.items.all().delete()
        
        return Response({
            'message': 'Order placed successfully',
            'order': OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)
