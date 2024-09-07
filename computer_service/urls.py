"""
URL configuration for computer_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from management.views import create_order, load_technicians, order_status, technician_login, register_technician, \
    technician_dashboard, edit_order, technician_profile, logout_view, home, report_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('new-order/', create_order, name='new_order'),
    path('ajax/load-technicians/', load_technicians, name='ajax_load_technicians'),
    path('order-status/<int:order_id>/', order_status, name='order_status'),
    path('technician/login/', technician_login, name='technician_login'),
    path('register/technician/', register_technician, name='register_technician'),
    path('technician/dashboard/', technician_dashboard, name='technician_dashboard'),
    path('technician/order/edit/<int:order_id>/', edit_order, name='edit_order'),
    path('technician/profile/', technician_profile, name='technician_profile'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),
    path('report/', report_view, name='report_view'),

]
