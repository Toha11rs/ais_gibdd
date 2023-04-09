from django.shortcuts import render, redirect, get_object_or_404
from ais.models import Driver, DriverLicense, Status, DriverAddress, Car, TypeWarning, Violation
from base.forms import SearchForm, ViolationForm, TypeWarningForm
from django.contrib import messages


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


def driver_info(request, driver_license_id):
    driver_license = get_object_or_404(DriverLicense, pk=driver_license_id)
    driver = driver_license.driver
    address = driver.address

    return render(request, 'base/driver_info.html', {'drivers': driver, 'driver_license': driver_license, "address": address})


def car(request, id):
    car = get_object_or_404(Car, pk=id)
    return render(request, 'base/search.html', {'cars': car})


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
        form = ViolationForm(request.POST)
        if form.is_valid():
            violation = form.save(commit=False)
            violation.driver = driver
            violation.save()
            messages.success(request, 'Штраф успешно создан',
                             extra_tags='success')
            return redirect('car_info', driver_license_id=driver_license_id)
        else:
            messages.error(request, 'Invalid form data.')
    else:
        form = ViolationForm()

    context['form'] = form
    return render(request, 'base/search.html', context)
