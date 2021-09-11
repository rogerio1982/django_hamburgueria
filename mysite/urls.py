from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
 path('admin/', admin.site.urls),
 path('', views.home, name='home'),
 path("detalhes/<int:pk>/", views.detail, name="detail"),
 path("carrinho/<int:pk>/", views.addCart, name="addCart"),
 path("carrinho/", views.verCar, name="verCar"),
 path("enviar/", views.enviar, name="enviar"),
 path("cadcli/", views.cadcli, name="cadcli"),
 path("cadclichama/", views.cadclichama, name="cadclichama"),
 path("excpedido/<int:pk>/", views.excpedido, name="excpedido"),
]