"""
URL configuration for zapatos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('registro_ventas_1', views.registro_ventas_1, name='registro_ventas_1'),
    path('registro_ventas_2', views.registro_ventas_2, name='registro_ventas_2'),
    path('reporte_ventas', views.reporte_ventas, name='reporte_ventas'),
    path('comisiones', views.comisiones, name='comisiones'),
    path('agregar_producto', views.agregar_producto, name='agregar_producto'),
    path('borrar_producto', views.borrar_producto, name='borrar_producto'),
    path('cantidad_producto', views.cantidad_producto, name='cantidad_producto'),
    path('registrar_venta', views.registrar_venta, name='registrar_venta'),
    path('detalle_ventas', views.detalle_ventas, name='detalle_ventas'),
    path('imprimir_recibo', views.imprimir_recibo, name='imprimir_recibo'),
    path('autenticador', views.autenticador, name='autenticador'),
    path('agregar_inventario', views.agregar_inventario, name='agregar_inventario'),
]
