"""icebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers
from icebox.views import UserViewSet
from store.views import ProductViewSet, ProductStockListView, ProductStockDetailView, CartView

router = routers.SimpleRouter()


router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/auth/token/', views.obtain_auth_token),
    path('v1/products/<int:product_pk>/stocks/', 
        ProductStockListView.as_view(), 
        name = 'product-stock-list'
    ),
    path('v1/products/<int:product_pk>/stocks/<str:size>/', 
        ProductStockDetailView.as_view(), 
        name = 'product-stock-detail'
    ),
    path('v1/cart/', CartView.as_view(), name = 'cart-view'),
    path('v1/', include(router.urls))
]
