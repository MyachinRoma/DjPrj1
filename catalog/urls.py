from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import product_list, product_detail



app_name = CatalogConfig.name

urlpatterns = [
    path('', product_list, name='product'),
    path('catalog/<int:pk>/', product_detail, name='product_detail')
]
