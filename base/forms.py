from django import forms
from ais.models import TypeWarning, CodeWarning, GetWarning, Violation, Penalty, BaseValue, District, StatusPenalty, Employee
from ais.models import CarInformation, Car, Position
from django.core.validators import RegexValidator
from datetime import date
from django import forms
from ais.fields import YearField
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
import random


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

    PeymantPenalty = forms.IntegerField(label="Сумма штрафа",min_value=0,max_value=50000,initial=0,
        widget=forms.NumberInput(
        attrs={'class': 'my-penalty-field',
                'value_suffix': 'руб.',    
                "step":100,

                }
                )
    )

    DateTime = forms.DateField(
        initial=date.today, widget=forms.DateInput(attrs={'type': 'hidden', 'class': 'my-date-field'})
    )

    deprivationDriving = forms.IntegerField(label="Срок лишения прав",help_text='Значение указывать в месяцах',
                                            min_value=0,initial=0,
        widget=forms.NumberInput(attrs={'class': 'my-deprivation-field'})
    )

    baseValue = forms.ModelChoiceField(
        queryset=BaseValue.objects.all(), label="Базовое значение",initial=1, 
        widget=forms.Select(attrs={'class': 'my-base-value-field'})
    )

    district = forms.ModelChoiceField(
        queryset=District.objects.all(), label="Район",
        widget=forms.Select(attrs={'class': 'my-district-field'})
    )

    statusPenalty = forms.ModelChoiceField(
        queryset=StatusPenalty.objects.all(), label="Статус штрафа",initial=2,
        widget=forms.Select(attrs={'class': 'my-status-penalty-field','type': 'hidden'})
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
    Number = forms.CharField(max_length=50, label="Номер автомобиля",
                             validators=[RegexValidator(
                                 r'^[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}$', 'Неправильно введен номер')],
                             widget=forms.TextInput(attrs={'placeholder': 'Пример: H735HM177','class': 'my-district-field'}))

    Brand = forms.CharField(max_length=50, label="Марка автомобиля",
                            widget=forms.TextInput(attrs={'placeholder': 'Пример: LADA','class': 'my-district-field'}), validators=[
                                RegexValidator(r'^[A-Za-z]{2,}$', 'Неправильна введена марка')])
    Model = forms.CharField(max_length=50, label="Модель автомобиля",
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Пример: VESTA','class': 'my-district-field'}), validators=[
                                RegexValidator(r'^[A-Za-z]{2,}$', 'Неправильна введена модель')])
    Color = forms.CharField(max_length=50, label="Цвет автомобиля",
                            widget=forms.TextInput(attrs={'placeholder': 'Пример: Blue','class': 'my-district-field'}), validators=[
                                RegexValidator(r'^[A-Za-z]{2,}$', 'Неправильно введен цвет')])

    Year = YearField(label="Год автомобиля", widget=forms.TextInput(
        attrs={'placeholder': 'Пример: 2020','class': 'my-district-field'}))

    RegistrationDate = forms.DateField(
        initial=date.today, widget=forms.DateInput(attrs={'class': 'my-district-field'}))

    class Meta: 
        model = CarInformation
        fields = ['Number', 'Brand', 'Model',
                  'Color', 'Year', 'RegistrationDate']
        
    def clean_Number(self):
        number = self.cleaned_data.get('Number')
        if CarInformation.objects.filter(Number=number).exists():
            raise ValidationError('Автомобиль с таким номером уже существует')
        return number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['carinformation']


class EmployeeForm(forms.ModelForm):
    name = forms.CharField(max_length=15, label="Имя",widget=forms.TextInput(attrs={'class': 'my-district-field'}))

    surname = forms.CharField(max_length=15, label="Фамилия", widget=forms.TextInput(attrs={'class': 'my-district-field'}))

    patronimyc = forms.CharField(max_length=15, label="Отчество", widget=forms.TextInput(attrs={'class': 'my-district-field'}))

    PhoneNumber = forms.CharField(max_length=11, label="Номер телефона",
                                   widget=forms.TextInput(attrs={'class': 'my-district-field', 'placeholder':"+7 (xxx) xxx-xx-xx"}))

    Position = forms.ModelChoiceField(queryset=Position.objects.all(), label="Должность",
                                      widget=forms.Select(attrs={'class': 'my-district-field'}))

    number = forms.IntegerField(label="Номер",widget=forms.TextInput(attrs={'class': 'my-district-field'}))

    password = forms.CharField(label="Пароль",widget=forms.PasswordInput(attrs={'class': 'my-district-field'}))
                               

    class Meta:
        model = Employee
        fields = ['name', 'surname', 'patronimyc', 'PhoneNumber', 'Position', 'number', 'password']

    # def clean_number(self):
    #     number = self.cleaned_data.get('number')
    #     if Employee.objects.filter(number=number).exists():
    #         raise forms.ValidationError('Такой сотрудник уже существует')
    #     return number
    
