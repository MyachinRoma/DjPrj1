from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts
from django.contrib import admin

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("admin/", admin.site.urls),
]
