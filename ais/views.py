from django.shortcuts import render, redirect, get_object_or_404
from ais.models import Driver, DriverLicense, Car, Employee, Penalty, District
from base.forms import UserRegistrationForm
from base.forms import SearchForm, CarInformationForm, PenaltyForm, AuthForm, EntryEmployeeForm,EmployeeForm,RegistrationForm,LoginForm
from django.contrib import messages
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from ais.serializer import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
import requests
import json
from django.http import JsonResponse


def main(request):

    return render(request, 'base/main.html')


def test(request):
    penalty_counts = Penalty.objects.values(
        'district__District').annotate(count=Count('id'))
    districts = District.objects.annotate(
        num_penalties=Count('penalty')).order_by('-num_penalties')
    data = {}
    for district in districts:
        data[district.District] = 0
    for penalty_count in penalty_counts:
        data[penalty_count['district__District']] = penalty_count['count']
    context = {
        'data': data
    }
    return render(request, 'base/test.html', context)


def search_driver_license(request):
    form = SearchForm()
    error_message = ''
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            try:
                driver_license = DriverLicense.objects.get(number=number)
                return redirect('car_info', driver_license_id=driver_license.id)
            except DriverLicense.DoesNotExist:
                error_message = 'Водительское удостоверение с номером {} не найдено'.format(
                    number)
    return render(request, 'base/search_driver_license.html', {'form': form, 'error_message': error_message})


def entryEmployee(request):
    if request.method == 'POST':
        form = EntryEmployeeForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            password = form.cleaned_data['password']
            try:
                Employee.objects.get(number=number, password=password)
                return redirect('EmployeeMain')
            except Employee.DoesNotExist:
                error = "Такого сотруднкиа не существует"
                return render(request, 'base/entryEmployee.html', {'form': form, 'error': error})
    else:
        form = EntryEmployeeForm()
    return render(request, 'base/entryEmployee.html', {'form': form})


def create_car_information(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)

    if request.method == 'POST':
        car_information_form = CarInformationForm(request.POST)
        if car_information_form.is_valid():
            car_information = car_information_form.save(commit=False)
            car_information.driver = driver
            car_information.save()

            car = Car(carinformation=car_information, driver=driver)
            car.save()
            messages.success(request, 'Машина зарегистрирована успешно!')

            return redirect('registercar', driver_id=driver_id)
        else:
            messages.error(request, 'Ошибка регистрации')
         

    else:
        car_information_form = CarInformationForm()

    context = {
        'car_information_form': car_information_form
    }

    return render(request, 'base/registercar.html', context)


def AuthDriver(request):
    form = AuthForm()
    error_message = ''
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            try:
                driver_license = DriverLicense.objects.get(number=number)
                return redirect('registercar', driver_id=driver_license.id)
            except DriverLicense.DoesNotExist:
                error_message = 'Водительское удостоверение с номером {} не найдено'.format(
                    number)
    return render(request, 'base/auth.html', {'form': form, 'error_message': error_message})


def car_info(request, driver_license_id):
    driver_license = get_object_or_404(DriverLicense, pk=driver_license_id)
    driver = driver_license.driver
    cars = Car.objects.filter(driver=driver)
    address = driver.address

    if request.method == 'POST':
        form = PenaltyForm(request.POST)
        if form.is_valid():
            penalty = form.save(commit=False)
            penalty.driver = driver
            penalty.save()
            messages.success(request, 'Штраф успешно создан')
            return redirect('car_info', driver_license_id=driver_license_id)
        else:
            messages.error(request, 'Ошибка при созданни штрафа')
    else:
        form = PenaltyForm()
    context = {
        'cars': cars,
        'driver': driver,
        'address': address,
        'driver_license': driver_license,
                                   
    }

    context['form'] = form

    return render(request, 'base/search.html', context)


def EmployeeMain(request):
    penalty_counts = Penalty.objects.values(
        'district__District').annotate(count=Count('id'))
    districts = District.objects.annotate(
        num_penalties=Count('penalty')).order_by('-num_penalties')
    data = {}
    for district in districts:
        data[district.District] = 0
    for penalty_count in penalty_counts:
        data[penalty_count['district__District']] = penalty_count['count']
    context = {
        'data': data
    }
    return render(request, 'base/employeeMain.html', context)


def addEmployee(request):


    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сотрудник успешко добавлен!')
            return redirect('addEmployee')
    else:

        form = EmployeeForm()

    return render(request, 'base/add_employee.html', {'form': form})

def allEmployee(request):
        
    employees = Employee.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        employees = employees.filter(Q(name__icontains=search_query) |
                                     Q(surname__icontains=search_query) |
                                     Q(PhoneNumber__icontains=search_query) |
                                     Q(number__icontains=search_query) |                                
                                     Q(patronimyc__icontains=search_query))
 

    context = {'employees': employees}

    return render(request, 'base/all_employee.html',context)


def penalty(request):
    penaltyes = Penalty.objects.all()
    context = { "penaltyes":penaltyes}

    return render(request, 'base/penalty.html',context)

def delete_employee(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect('allEmployee')


def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            hashed_password = make_password(password)
            user = User.objects.create(username=username, password=hashed_password)
            return redirect('main')  
    else:
        form = RegistrationForm()
    return render (request,'base/auth/register.html',{'form': form})


def login_user(request):
    error_message = ''

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                error_message = 'Неверное имя пользователя или пароль'
        else:
            error_message = 'Некорректные данные'
    else:
        form = LoginForm()

    return render(request, 'base/auth/login.html', {'form': form, 'error_message': error_message})



##########################################
# API
##########################################



def registrationView(request):
    if request.method == 'POST':
        url = 'http://127.0.0.1:8000/auth/users/'

        data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
        }

        response = requests.post(url, data=data)

        if response.status_code == 201:
            messages.success(request, 'Регистрация успешна!')
            return redirect('success')  # Перенаправление на другую страницу
        elif response.status_code == 400:
            errors = response.json()
            for field, error_messages in errors.items():
                for error_message in error_messages:
                    messages.error(request, f' {error_message}')
        else:
            messages.error(request, 'Произошла ошибка регистрации')
    return render(request, 'base/auth/registration.html',)
