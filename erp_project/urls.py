from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sales.urls')),
    path('inventory/', include('inventory.urls')),
    path('accounting/', include('accounting.urls')),
    path('hr/', include('hr.urls')),
    path('users/', include('users.urls')),
]
