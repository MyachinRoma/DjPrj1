from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls), # подключаем админку
    path('', include('catalog.urls', namespace='catalog')),# подключаем все пути из приложения catalog
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # пробрасываем изображения, чтоб на страничках они отображались
