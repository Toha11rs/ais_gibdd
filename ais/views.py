from django.shortcuts import render, redirect, get_object_or_404
from ais.models import Driver, DriverLicense, Car, Penalty, BaseValue, District, StatusPenalty, Employee, Violation, TypeWarning, CodeWarning, GetWarning, District, BaseValue, StatusPenalty, Position, Employee, Violation, Penalty
from base.forms import SearchForm, ViolationForm, PenaltyForm
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect


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
        form = ViolationForm(request.POST)
        if form.is_valid():
            violation = form.save(commit=False)
            violation.driver = driver
            violation.save()
            messages.success(request, 'Штраф успешно создан')
            return redirect('car_info', driver_license_id=driver_license_id)
        else:
            messages.error(request, 'Ошибка при созданни штрафа')
    else:
        form = ViolationForm()

    context['form'] = form

    return render(request, 'base/search.html', context)


def penalty_view(request, driver_id):
    driver = Driver.objects.get(id=driver_id)

    if request.method == 'POST':
        violation_form = ViolationForm(request.POST)
        penalty_form = PenaltyForm(request.POST)
        if violation_form.is_valid() and penalty_form.is_valid():
            type_warning = TypeWarning.objects.get(
                id=request.POST['type_warning'])
            code_warning = CodeWarning.objects.get(
                id=request.POST['code_warning'])
            get_warning = GetWarning.objects.get(
                id=request.POST['get_warning'])

            # Сохранение новой записи Violation в базу данных
            violation = Violation.objects.create(
                typeWarning=type_warning,
                code=code_warning,
                warning=get_warning,
                driver=driver
            )

            # Сохранение новой записи Penalty в базу данных
            penalty = penalty_form.save(commit=False)
            penalty.Violation = violation
            penalty.save()

            return HttpResponseRedirect(f'/driver/{driver_id}/')

    else:
        violation_form = ViolationForm()
        penalty_form = PenaltyForm()

    return render(request, 'base/penalty.html', {'violation_form': violation_form, 'penalty_form': penalty_form})
