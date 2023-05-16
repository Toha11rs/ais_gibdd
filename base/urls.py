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
from django.urls import path
from ais import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('admin/', admin.site.urls),
    path('serach_license/', views.search_driver_license,
         name='search_driver_license'),  # поиск ВУ для вывода всей информации о водиетле а также выписывание штрафа
    # поиск ВУ для потсановления на учет
    path('auth/', views.AuthDriver, name='auth'),

    # вывод информации о водителе а также выписывание ему  штарфа
    path('car_info/<int:driver_license_id>/', views.car_info, name='car_info'),

    path('', views.main, name='main'),  # главная страница

    path('registercar/<int:driver_id>/',
         views.create_car_information, name='registercar'),  # регистрация автомобиля
    path('entryEmployee', views.entryEmployee,
         name='entryEmployee'),  # вход для сторудников
    # главная странциа сотрудников
    path('employeeMain', views.EmployeeMain, name='EmployeeMain'),

    path('addEmployee', views.addEmployee, name='addEmployee'),

    path('allEmployee', views.allEmployee, name='allEmployee'),
    
    path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),
]
