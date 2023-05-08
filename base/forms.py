from django import forms
from ais.models import TypeWarning, CodeWarning, GetWarning, Violation, Penalty, BaseValue, District, StatusPenalty, Employee
from ais.models import CarInformation, Car
from django.core.validators import RegexValidator
from datetime import date
from django import forms
from ais.fields import YearField


class SearchForm(forms.Form):
    number = forms.IntegerField(
        label='Введите номер водительского удостоверения')


class EntryEmployeeForm(forms.Form):
    number = forms.CharField(max_length=50, required=False,
                             label="Номер сотрудника")
    password = forms.IntegerField(label="Пароль")


class AuthForm(forms.Form):
    number = forms.IntegerField(
        label='Введите номер водительского ')


class ViolationForm(forms.ModelForm):
    typeWarning = forms.ModelChoiceField(
        queryset=TypeWarning.objects.all(), label="Тип нарушения")
    code = forms.ModelChoiceField(
        queryset=CodeWarning.objects.all(), label="Код нарушения")
    GetWarning = forms.ModelChoiceField(
        queryset=GetWarning.objects.all(), label="Сделать предупреждение")

    class Meta:
        model = Violation
        fields = ['typeWarning', 'code', 'warning']


class PenaltyForm(forms.ModelForm):
    typeWarning = forms.ModelChoiceField(
        queryset=TypeWarning.objects.all(), label="Тип нарушения", 
        widget=forms.Select(attrs={'class': 'my-type-warning-field'})
    )

    code = forms.ModelChoiceField(
        queryset=CodeWarning.objects.all(), label="Код нарушения",
        widget=forms.Select(attrs={'class': 'my-code-warning-field'})
    )

    warning = forms.ModelChoiceField(
        queryset=GetWarning.objects.all(), label="Сделать предупреждение",
        widget=forms.Select(attrs={'class': 'my-warning-field'})
    )

    PeymantPenalty = forms.IntegerField(label="Укажите сумму штрафа",
        widget=forms.NumberInput(attrs={'class': 'my-penalty-field'})
    )

    DateTime = forms.DateField(
        initial=date.today, widget=forms.DateInput(attrs={'type': 'hidden', 'class': 'my-date-field'})
    )

    deprivationDriving = forms.IntegerField(label="Укажите срок лишения прав",
        widget=forms.NumberInput(attrs={'class': 'my-deprivation-field'})
    )

    baseValue = forms.ModelChoiceField(
        queryset=BaseValue.objects.all(), label="Базовое значение",
        widget=forms.Select(attrs={'class': 'my-base-value-field'})
    )

    district = forms.ModelChoiceField(
        queryset=District.objects.all(), label="Район",
        widget=forms.Select(attrs={'class': 'my-district-field'})
    )

    statusPenalty = forms.ModelChoiceField(
        queryset=StatusPenalty.objects.all(), label="Статус штрафа",
        widget=forms.Select(attrs={'class': 'my-status-penalty-field'})
    )

    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(), label="Сотрудник",
        widget=forms.Select(attrs={'class': 'my-employee-field'})
    )

    class Meta:
        model = Penalty
        fields = ['code', 'warning', 'typeWarning', 'PeymantPenalty', 'employee', 'baseValue', 'DateTime',
                  'deprivationDriving', 'district', 'statusPenalty']
        


class AuthForms(forms.ModelForm):
    number = forms.IntegerField(
        label='Введите номер водительского удостоверения')


class CarInformationForm(forms.ModelForm):
    Number = forms.CharField(max_length=50, label="Номер автомобиля")
    Brand = forms.CharField(max_length=50, label="Марка автомобиля")
    Model = forms.CharField(max_length=50, label="Модель автомобиля")
    Color = forms.CharField(max_length=50, label="Цвет автомотбиля")

    Year = YearField(label="Год автомобиля", widget=forms.TextInput(
        attrs={'placeholder': 'Пример: 2020'}))

    RegistrationDate = forms.DateField(
        initial=date.today, widget=forms.DateInput(attrs={'type': 'hidden'}))

    class Meta:
        model = CarInformation
        fields = ['Number', 'Brand', 'Model',
                  'Color', 'Year', 'RegistrationDate']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['carinformation']
