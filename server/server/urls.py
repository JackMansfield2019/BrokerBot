from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/login/", views.login, name='login'),
    path('user/<int:key_id>/', views.id, name = 'id'),
]
