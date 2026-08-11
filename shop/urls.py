from django.contrib import admin
from django.urls import path, include
from django.conf import settings
import importlib.util

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('store.urls')),
]

if settings.DEBUG and importlib.util.find_spec('debug_toolbar'):
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
