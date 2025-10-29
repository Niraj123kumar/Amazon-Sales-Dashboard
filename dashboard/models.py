from django.db import models

# Create your models here.
from django.db import models

class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateField()
    total_price = models.FloatField()

    def __str__(self):
        return f"Order {self.order_id}"
