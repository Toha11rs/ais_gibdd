from django import forms
from ais.models import TypeWarning, CodeWarning, GetWarning, Violation, Penalty, BaseValue, District, StatusPenalty, Employee
from django.forms.widgets import DateTimeInput
from django.views.generic.edit import CreateView


class SearchForm(forms.Form):
    number = forms.IntegerField(
        label='Введите номер водительского удостоверения')


class ViolationForm(forms.ModelForm):
    typeWarning = forms.ModelChoiceField(
        queryset=TypeWarning.objects.all(), label="Тип нарушения")
    code = forms.ModelChoiceField(
        queryset=CodeWarning.objects.all(), label="Код нарушения")
    warning = forms.ModelChoiceField(
        queryset=GetWarning.objects.all(), label="Сделать предупреждение")

    class Meta:
        model = Violation
        fields = ['typeWarning', 'code', 'warning']


class PenaltyForm(forms.ModelForm):
    BaseValue = forms.ModelChoiceField(
        queryset=BaseValue.objects.all(), label="Базовое значение")

    District = forms.ModelChoiceField(
        queryset=District.objects.all(), label="Район")

    StatusPenalty = forms.ModelChoiceField(
        queryset=StatusPenalty.objects.all(), label="Статус штрафа")

    Employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(), label="Сотрудник")
    Violation = forms.ModelChoiceField(
        queryset=Violation.objects.all(), label="Нарушение")

    class Meta:
        model = Penalty
        fields = ['PeymantPenalty', 'BaseValue', 'DateTime',
                  'District', 'StatusPenalty', 'Employee', 'Violation']
