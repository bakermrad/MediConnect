from django.contrib import admin
from django.urls import include, path
from MediConnect import settings
from mainapp.views import *
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
