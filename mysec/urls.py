"""mysec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from index import views
from index import views_api

urlpatterns = [

    path('', views.root),
    path('index/', views.index),
    path('test/', views.test),
    path('target/add/',views.target_add),
    path('target/edit/<int:target_id>/',views.target_edit),
    path('target/<int:target_id>/',views.target),
    path('target/domain/<int:target_id>/', views.subdomain_list),
    path('target/iplist/<int:target_id>/', views.ip_list),

    # api 接口
    path('api/target/add/', views_api.api_target_add),
    path('api/target/edit/', views_api.api_target_edit),
    path('api/target/del/', views_api.api_target_del),
    path('api/target/list/', views_api.api_target_list),
    path('api/target/scan/', views_api.api_target_scan),
    path('api/domain/list/<int:target_id>/', views_api.api_domain_list),
    path('api/ip/list/<int:target_id>/', views_api.api_ip_list),

    # ------------ C段 -----------
    path('c/', views.c_ip),
    path('c/add/', views.c_add),

    path('c/ip2domain/<int:target_id>/',views.cdomain_list),


    path('api/c/add/', views_api.api_c_add),
    path('api/c/list/', views_api.api_c_list),
    path('api/c/scan/', views_api.api_c_scan),

    path('api/c/ip2domain/list/<int:target_id>/', views_api.api_c_ip2doamin_list),

]
