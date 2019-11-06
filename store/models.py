from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from rest_framework import serializers

# Create your models here.

User = get_user_model()


class Product(models.Model):

    name = models.CharField(max_length = 225)
    price = models.FloatField(default = 14.99)
    description = models.CharField(max_length = 750)

    def __str__(self):

        return self.name



class Stock(models.Model):

    EXTRA_SMALL = 'xs'
    SMALL = 'sm'
    MEDIUM = 'md'
    LARGE = 'lg'
    EXTRA_LARGE = 'xl'

    SIZE_OPTIONS = (
        (EXTRA_SMALL, 'Extra Small'),
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (EXTRA_LARGE, 'Extra Large')
    )

    product = models.ForeignKey('store.Product', on_delete = models.CASCADE)
    size = models.CharField(max_length = 2, choices = SIZE_OPTIONS)
    quantity = models.PositiveIntegerField(default = 50)

    
    def __str__(self):

        return self.product.name


    class Meta:

        unique_together = (('product', 'size', ), )




class Order(models.Model):

    EXTRA_SMALL = 'xs'
    SMALL = 'sm'
    MEDIUM = 'md'
    LARGE = 'lg'
    EXTRA_LARGE = 'xl'

    SIZE_OPTIONS = (
        (EXTRA_SMALL, 'Extra Small'),
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (EXTRA_LARGE, 'Extra Large')
    )


    cart = models.ForeignKey('store.Cart', on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    size = models.CharField(max_length = 2, choices = SIZE_OPTIONS)
    product = models.ForeignKey('store.Product', on_delete = models.CASCADE)


    def __str__(self):


        return self.cart.user.username


    def save(self, *args, **kwargs):

        if not self.id:

            stock = self.product.stock_set.get(size = self.size)
            new_stock = stock.quantity - self.quantity

            if  new_stock >= 0:

                stock.quantity = new_stock
                stock.save()

            elif new_stock < 0:

                raise serializers.ValidationError({
                    "quantity": "There is not enough inventory for this order"
                })

        super(Order, self).save(*args, **kwargs)

class Cart(models.Model):

    PENDING = 'p'
    CHECKED_OUT = 'c'
    TIMED_OUT = 't'
    DELETED = 'd'

    STATUS_OPTIONS = (
        (PENDING, 'Pending'),
        (CHECKED_OUT, 'Checked Out'),
        (TIMED_OUT, 'Timed Out'),
        (DELETED, 'Deleted'),
    )

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.CharField(max_length = 2, choices = STATUS_OPTIONS, default = PENDING)

    def __str__(self):

        return self.user.username

    
    def add_to_cart(self, product = None, size = None, quantity = None):

        product = Product.objects.get(pk = product)

        if quantity is not None:

            order, created = self.order_set.get_or_create(
                product = product,
                size = size,
            )

            stock = order.product.stock_set.get(size = size)

            old_stock = stock.quantity + order.quantity

            order.quantity = quantity

            new_stock = old_stock - order.quantity

            if new_stock >= 0:

                stock.quantity = new_stock
                stock.save()
                order.save()

            elif new_stock < 0:

                raise serializers.ValidationError({
                    "quantity":"There is not enough inventory for this order."
                })

        return order


    def remove_from_cart(self, product = None, size = None):

        product = Product.objects.get(pk = product)

        order = self.order_set.get(product__pk = product.id, size = size)

        if self.status == self.PENDING:

            stock = order.product.stock_set.get(size = size)
            stock.quantity += order.quantity
            stock.save()

        order.delete()

        return True




@receiver(post_save, sender = Product)
def create_initial_product_inventory(sender, instance, created, **kwargs):

    if created:

        for choice in Stock.SIZE_OPTIONS:

            Stock.objects.create(product = instance, size = choice[0])

