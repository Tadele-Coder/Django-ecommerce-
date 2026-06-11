from django.db import models
from django.contrib.auth.models import User


# Create your models here.


CATEGORY_CHOICES = (
    ('ST', 'Starters'),
    ('BR', 'Burgers'),
    ('PZ', 'Pizza'),
    ('GD', 'Grilled Dishes'),
    ('PS', 'Pasta'),
    ('RS', 'Rice & Asian Dishes'),
    ('SN', 'Sandwiches & Wraps'),
    ('SL', 'Salads'),
    ('DS', 'Desserts'),
    ('JU', 'Fresh Juice & Drinks'),
    ('CM', 'Combo Meals'),
    ('TR', 'Traditional Meals'),
)

STATE_CHOICES = (
    ('BL', 'Bole'),
    ('YK', 'Yeka'),
    ('LM', 'Lemi Kura'),
    ('AR', 'Arada'),
    ('AD', 'Addis Ketema'),
    ('LF', 'Nifas Silk Lafto'),
    ('AK', 'Akaky Kality'),
    ('KR', 'Kirkos'),
    ('GL', 'Gullele'),
    ('LD', 'Lideta'),
    ('KF', 'Kolfe Keranio'),
   
)
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed', 'Packed'),
    ('On the Way','On the Way'),
    ('Delivered', 'Delivered'),
    ('Pending', 'Pending'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title
    
class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    subcity = models.CharField(choices=STATE_CHOICES, max_length=100)
    specific_area = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    additional_phone = models.IntegerField()
    
    def __str__(self):
        return self.full_name
        
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    telebirr_order_id = models.CharField(max_length=100, blank=True, null=True)
    telebirr_payment_status = models.CharField(max_length=100, blank=True, null=True)
    telebirr_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)



class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    ordered_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending'
    )

    @property
    def total_cost(self):
        return self.price * self.quantity
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
