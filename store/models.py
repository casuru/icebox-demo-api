from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Cart(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.CharField(max_length = 2)

    def __str__(self):

        return self.user.username


class Product(models.Model):

    name = models.CharField(max_length = 225)
    price = models.FloatField(default = 14.99)


    def __str__(self):

        return self.name


class Size(models.Model):

    name = models.CharField(max_length = 2)

    def __str__(self):

        return self.name


class Stock(models.Model):

    product = models.ForeignKey('store.Product', on_delete = models.CASCADE)
    size = models.ForeignKey('store.Size', on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 50)


    def __str__(self):

        return self.quantity


class Order(models.Model):

    cart = models.ForeignKey('store.Cart', on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    size = models.ForeignKey('store.Size', on_delete = models.CASCADE)
    product = models.ForeignKey('store.Product', on_delete = models.CASCADE)


    def __str__(self):


        return self.cart.user.username




    
