from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='Category')
    # image = models.ImageField(upload_to='category',verbose_name='Category Image')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='Category')
    name = models.CharField(max_length=100,verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Price')
    image = models.ImageField(upload_to='products',verbose_name='Image')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50, null=True, default='')
    last_name = models.CharField(max_length=50, null=True, default='')


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_cart_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity




class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)

    @property
    def get_cart_price(self):
        total_price = self.quantity * self.product.price
        return total_price


