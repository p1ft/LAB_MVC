from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('cocktails/', include('cocktails.urls')),
    path('admin/', admin.site.urls),
]
