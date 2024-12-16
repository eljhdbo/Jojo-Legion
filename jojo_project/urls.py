from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jojo_api.urls')),  # Remplacez 'jojo_api' par le nom réel de votre application
]
