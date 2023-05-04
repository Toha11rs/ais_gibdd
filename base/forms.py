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
        queryset=TypeWarning.objects.all(), label="Тип нарушения")

    code = forms.ModelChoiceField(
        queryset=CodeWarning.objects.all(), label="Код нарушения")

    warning = forms.ModelChoiceField(
        queryset=GetWarning.objects.all(), label="Сделать предупреждение")

    PeymantPenalty = forms.IntegerField(label="Укажите сумму штрафа")

    DateTime = forms.DateField(
        initial=date.today, widget=forms.DateInput(attrs={'type': 'hidden'}))

    deprivationDriving = forms.IntegerField(label="Укажите срок лишения прав")

    baseValue = forms.ModelChoiceField(
        queryset=BaseValue.objects.all(), label="Базовое значение")

    district = forms.ModelChoiceField(
        queryset=District.objects.all(), label="Район")

    statusPenalty = forms.ModelChoiceField(
        queryset=StatusPenalty.objects.all(), label="Статус штрафа")

    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(), label="Сотрудник")

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
