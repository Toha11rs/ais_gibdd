"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path, re_path
from ais import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.views.generic import TemplateView

urlpatterns = [
    path('test', views.test, name='test'),
    path('admin/', admin.site.urls),
    path('serach_license/', views.search_driver_license,
         name='search_driver_license'),  # поиск ВУ для вывода всей информации о водиетле а также выписывание штрафа
    # поиск ВУ для потсановления на учет
    path('auths/', views.AuthDriver, name='auths'),

    # вывод информации о водителе а также выписывание ему  штарфа
    path('car_info/<int:driver_license_id>/', views.car_info, name='car_info'),

    path('', views.main, name='main'),  # главная страница

    path('registercar/<int:driver_id>/',
         views.create_car_information, name='registercar'),  # регистрация автомобиля

    path('entryEmployee', views.entryEmployee,
         name='entryEmployee'),  # вход для сторудников
    # главная странциа сотрудников
    # path('employeeMain', views.EmployeeMain, name='EmployeeMain'),

    path('employeeMain/', views.EmployeeMain, name='EmployeeMain'),

    path('addEmployee', views.addEmployee, name='addEmployee'),

    path('allEmployee', views.allEmployee, name='allEmployee'),
    
    path('allUsers', views.allUsers, name='allUsers'),

    path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),



    path('penalty', views.penalty, name='penalty'),

    path('block_user/<int:id>/', views.block_users, name='block_users'),

    path('unblock_user/<int:id>/', views.unblock_user, name='unblock_user'),
    ######
    # API
    ######
    # path('api/register/', views.api_register, name='user-registration'),


    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),

    path('registration_user', views.registration_view, name='registration_user'),
    path('login_user', views.login_view, name='login_user'),
]
