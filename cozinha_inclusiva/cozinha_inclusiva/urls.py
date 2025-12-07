from django.contrib import admin
from django.urls import path, include
from apps.website import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='inicio'),
]
