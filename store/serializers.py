from rest_framework import serializers
from store.models import Product, Stock, Order, Cart

class StockSerializer(serializers.ModelSerializer):



    def update(self, stock, validated_data):

        stock.quantity = validated_data.get('quantity', stock.quantity)
        stock.save()

        return stock

    class Meta:

        fields = "__all__"
        model = Stock
        extra_kwargs = {
            "product":{
                "read_only": True
            },
            "size":{
                "read_only": True
            }

        }


class ProductSerializer(serializers.ModelSerializer):

    stock_set = StockSerializer(many = True, read_only = True)
    sizes = serializers.SerializerMethodField()

    class Meta:

        fields = "__all__"
        model = Product

    def get_sizes(self, product):

        return [stock.size for stock in product.stock_set.all()]


class OrderSerializer(serializers.ModelSerializer):


    class Meta:

        fields = "__all__"
        model = Order


class CartSerializer(serializers.ModelSerializer):


    order_set = OrderSerializer(read_only = True, many = True)

    class Meta:

        fields = "__all__"
        model = Cart
        extra_kwargs = {
            "user":{
                "read_only": True
            }
        }