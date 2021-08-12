from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/login/", views.login, name='login'),
    path("user/register/", views.register, name='register'),
    path('user/<int:key_id>/', views.id, name = 'id'),
    path('bot/getInfo/<int:key_id>/', views.getBotInfoWithID, name = 'get bot info with id'),
    path('bot/getInfo/', views.getBotInfo, name = 'get bot info'),
]
