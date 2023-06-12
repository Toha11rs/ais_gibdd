from audioop import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from ais.models import Driver, DriverLicense, Car, Employee, Penalty, District,UserTryLogin
from base.forms import SearchForm, CarInformationForm, PenaltyForm, AuthForm, EntryEmployeeForm,EmployeeForm,RegistrationForm,LoginForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
import requests
from django.utils import timezone
import pytz
import time
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash



def main(request):

    return render(request, 'base/main.html')


# @api_view(['GET'])    
# @permission_classes([IsAuthenticated])
@login_required
def test(request):

    return render(request, 'base/test.html')


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

# @api_view(['GET'])    
# @permission_classes([IsAuthenticated])
@login_required
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



def block_users(request, id):
    try:
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect('allUsers')  
    except User.DoesNotExist:
        return redirect('allUsers')

def unblock_user(request, id):
    try:
        user = User.objects.get(id=id)
        user.is_active = True
        user.save()
        return redirect('allUsers')  
    except User.DoesNotExist:
        return redirect('allUsers')


@login_required
def allUsers(request):
    users = User.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(last_login__icontains=search_query)
        )
    login_attempts = UserTryLogin.objects.filter(user__in=users, attempt_number__gt=5)
    context = {
        'users': users,
        'login_attempts':login_attempts,
               }

    return render(request, 'base/admin/allusers.html', context)

##########################################
# API
##########################################



def registration_view(request):

    

    maxAttempts = 3
    lock_time = 10  # Время блокировки в секундах
    incorrectAttempts = request.session.get('incorrect_attempts', 0)
    lastAttemptTime = request.session.get('last_attempt_time')
    
    if request.method == 'POST':

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print("пароли совпадают")

        if password != confirm_password:
            error_message = 'Пароли не совпадают'
            print("пароли  не совпадают")
            return render(request, 'base/auth/registration.html', {'error_message': error_message})
        
        if lastAttemptTime and time.time() - lastAttemptTime < lock_time:
            remainingTime = lock_time - (time.time() - lastAttemptTime)
           
            return redirect('registration_user')  
        
        if incorrectAttempts >= maxAttempts:
            request.session['last_attempt_time'] = time.time()  # Сохранить время последней попытки
            request.session['incorrect_attempts'] = 2  # сброс счетчика некорректных попыток

            return redirect('registration_user')  
        
        url = 'http://127.0.0.1:8000/auth/users/'

        data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
        }

        response = requests.post(url, data=data)

        if response.status_code == 201:
            messages.success(request, 'Регистрация успешна!')
            return redirect('main') 
        elif response.status_code == 400:
            errors = response.json()
            for field, error_messages in errors.items():
                for error_message in error_messages:
                    messages.error(request, f'{error_message}')
            # Увеличить счетчик некорректных попыток
            request.session['incorrect_attempts'] = incorrectAttempts + 1
        else:
            messages.error(request, 'Произошла ошибка регистрации')

    remainingTime = int(lock_time - (time.time() - lastAttemptTime)) if lastAttemptTime else 0
    return render(request, 'base/auth/registration.html', {'remaining_time': remainingTime})


def login_view(request):
    employees = UserTryLogin.objects.all()
    print(employees)
    maxAttempts = 3
    lock_time = 10  
    incorrectAttempts = request.session.get('incorrect_attempts', 0)
    lastAttemptTime = request.session.get('last_attempt_time')

    if request.method == 'POST':
        url = 'http://127.0.0.1:8000/auth/token/login/'

        data = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            token = response.json().get('auth_token')
            request.session['token'] = token


            user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                user.last_login = timezone.now().astimezone(pytz.timezone('Europe/Moscow'))
                user.save()
            messages.success(request, 'Вход выполнен успешно!')

                # обнуление счетчика неудачных попыток
            username = request.POST.get('username')     
            password = request.POST.get('password')     
            is_staff = request.POST.get('is_staff')     
            
            user = authenticate(request, username=username, password=password,is_staff=is_staff)

            login_attempt, _ = UserTryLogin.objects.get_or_create(user=request.user)
            login_attempt.clear_attempt()

            is_staff = user.is_staff
            print(is_staff)
            if user.is_staff == True:
                print("админ")
                return redirect("allUsers")

            else:
                print("юзер")
                return redirect("main")


                # вход по токену( не рабоает)
            # url = 'http://127.0.0.1:8000/test'
            # response['Authorization'] = f'Token {token}'
            # response = requests.get(url, headers={'Authorization': f'Token {token}'})
            
        
        elif response.status_code == 400:
                    request.session['incorrect_attempts'] = incorrectAttempts + 1
                    request.session['last_attempt_time'] = time.time()  #  время последней попытки

                     #счетчик неудачных попыток
                    try:
                        login_attempt, _ = UserTryLogin.objects.get_or_create(user=request.user)
                        login_attempt.increase_attempt()
                    except:
                        messages.error(request, 'Неправильный логин или пароль')
                        return redirect("login_user")

                    if incorrectAttempts + 1 >= maxAttempts:

                        return redirect('login_user') 
                    else:
                        messages.error(request, 'Неправильный логин или пароль')
        else:
                    messages.error(request, 'Произошла ошибка входа')
    remainingTime = int(lock_time - (time.time() - lastAttemptTime)) if lastAttemptTime else 0
    return render(request, 'base/auth/loginT.html', {'remaining_time': remainingTime})

@login_required(login_url='login_user') 
def user_page(request):
    user = request.user


    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль успешно изменен.')
            return redirect('user')
    else:
        form = PasswordChangeForm(user)

    context = {
        'form': form,
    }
    return render(request, 'base/user/user_page.html', context)
