from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, product_list, product_detail
from django.contrib import admin


app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("", contacts, name="contacts"),
    path("admin/", admin.site.urls),
    path('', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail')
]
