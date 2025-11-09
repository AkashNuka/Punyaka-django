from django.db import models
from core.models import User


class Category(models.Model):
    """Product categories"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                               related_name='children')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Product(models.Model):
    """Products (samagri, gifts, etc.)"""
    
    PRODUCT_TYPES = (
        ('samagri', 'Pooja Samagri'),
        ('gift', 'Gift Item'),
        ('kit', 'Kit'),
        ('other', 'Other'),
    )
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPES, default='samagri')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, 
                                 related_name='products')
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Inventory
    stock = models.IntegerField(default=0)
    is_in_stock = models.BooleanField(default=True)
    
    # Images
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Gift options
    gift_wrap_available = models.BooleanField(default=False)
    gift_wrap_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_price(self):
        """Return the effective price"""
        return self.discount_price if self.discount_price else self.price
    
    class Meta:
        ordering = ['-created_at']


class Cart(models.Model):
    """Shopping cart"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart - {self.user.username}"
    
    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())


class CartItem(models.Model):
    """Items in cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    # Gift options
    is_gift = models.BooleanField(default=False)
    gift_message = models.TextField(blank=True, null=True)
    add_gift_wrap = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    def get_subtotal(self):
        subtotal = self.product.get_price() * self.quantity
        if self.add_gift_wrap:
            subtotal += self.product.gift_wrap_price
        return subtotal
    
    class Meta:
        unique_together = ['cart', 'product']


class Order(models.Model):
    """Customer orders"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    order_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    # Shipping address
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_pincode = models.CharField(max_length=10)
    shipping_phone = models.CharField(max_length=15)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, 
                                     default='pending')
    
    # Tracking
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    
    # Gift options
    is_gift = models.BooleanField(default=False)
    gift_message = models.TextField(blank=True, null=True)
    has_gift_wrap = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.quantity}x {self.product_name}"
    
    def get_subtotal(self):
        return self.product_price * self.quantity
