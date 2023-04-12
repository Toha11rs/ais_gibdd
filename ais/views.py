from django.shortcuts import render, redirect, get_object_or_404
from ais.models import Driver, DriverLicense, Car, Penalty
from base.forms import SearchForm, ViolationForm, PenaltyForm, CustomPenaltyForm
from django.contrib import messages
from django.http import JsonResponse


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


def car_info(request, driver_license_id):
    driver_license = get_object_or_404(DriverLicense, pk=driver_license_id)
    driver = driver_license.driver
    cars = Car.objects.filter(driver=driver)
    address = driver.address

    context = {
        'cars': cars,
        'driver': driver,
        'address': address,
        'driver_license': driver_license,
    }

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

    context['form'] = form

    return render(request, 'base/search.html', context)


def RegisterCar(request):
    return render(request, 'base/registercar.html')


def test(request):

    return render(request, 'base/test.html')
