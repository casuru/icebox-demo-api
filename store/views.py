from rest_framework import viewsets, views, status, response, generics, filters
from rest_framework.permissions import IsAuthenticated
from store.permissions import IsStaffOrReadOnly
from store.models import Product, Stock, Cart, Order
from store.serializers import ProductSerializer, StockSerializer, CartSerializer

class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    permission_classes = (IsStaffOrReadOnly, )


class ProductStockListView(generics.GenericAPIView):

    serializer_class = StockSerializer

    def get_queryset(self):

        return Stock.objects.filter(
            product__pk = self.kwargs['product_pk']
        )

    def get(self, request, product_pk):

        stocks = self.get_queryset()
        
        serialized_stocks = self.serializer_class(stocks, many = True)

        return response.Response(serialized_stocks.data, status = status.HTTP_200_OK)


class ProductStockDetailView(generics.GenericAPIView):


    serializer_class = StockSerializer

    def get_object(self):

        return Stock.objects.get(
            product__pk = self.kwargs['product_pk'],
            size = self.kwargs['size']
        )

    def get(self, request, product_pk, size):

        stock = self.get_object()

        serialized_stock = self.serializer_class(stock)

        return response.Response(serialized_stock.data, status = status.HTTP_200_OK)

    def patch(self, request, product_pk, size):

        stock = self.get_object()

        serialized_stock = self.serializer_class(stock, data = request.data)

        if serialized_stock.is_valid():

            serialized_stock.save()

            return response.Response(serialized_stock.data, status = status.HTTP_200_OK)

        return response.Response(serialized_stock.errors, status = status.HTTP_200_OK)




class CartView(generics.GenericAPIView):

    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, )


    def get_object(self):

        cart, created = Cart.objects.get_or_create(
            user = self.request.user,
            status = Cart.PENDING
        )

        return cart


    def get(self, request):

        cart = self.get_object()

        serialized_cart = self.serializer_class(cart)

        return response.Response(serialized_cart.data, status = status.HTTP_200_OK)

    
    def post(self, request):

        cart = self.get_object()

        action = request.data.pop('action', None)

        if action == 'add':

            cart.add_to_cart(**request.data)

        elif action == 'remove':

            cart.remove_from_cart(**request.data)

        serialized_cart = self.serializer_class(cart)

        return response.Response(serialized_cart.data, status = status.HTTP_200_OK)


    def patch(self, request):

        cart = self.get_object()

        serialized_cart = self.serializer_class(cart, data = request.data)

        if serialized_cart.is_valid():
            
            serialized_cart.save()

            return response.Response(serialized_cart.data, status = status.HTTP_200_OK)

        return response.Response(serialized_cart.errors, status = status.HTTP_400_BAD_REQUEST)












