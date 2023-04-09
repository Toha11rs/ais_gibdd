from django import forms
from ais.models import Violation, TypeWarning, CodeWarning, GetWarning, Driver


class SearchForm(forms.Form):
    number = forms.IntegerField(
        label='Введите номер водительского удостоверения')


class TypeWarningForm(forms.ModelForm):
    class Meta:
        model = TypeWarning
        fields = ["Type"]


class ViolationForm(forms.ModelForm):
    typeWarning = forms.ModelChoiceField(
        queryset=TypeWarning.objects.all(), label='Тип нарушения')
    code = forms.ModelChoiceField(
        queryset=CodeWarning.objects.all(), label='Код штрафа')
    warning = forms.ModelChoiceField(
        queryset=GetWarning.objects.all(), label='Сделать предупреждение')
    termDeprivation = forms.IntegerField(label="Введи сумму штрафа")

    class Meta:
        model = Violation
        fields = ['typeWarning', 'code', 'warning', 'termDeprivation']

    def __init__(self, *args, **kwargs):
        driver_id = kwargs.pop('driver_id', None)
        super(ViolationForm, self).__init__(*args, **kwargs)
        if driver_id:
            self.fields['driver'].queryset = Driver.objects.filter(
                pk=driver_id)

    def save(self, commit=True, driver_id=None):
        violation = super().save(commit=False)
        if driver_id:
            violation.driver_id = driver_id
        if commit:
            violation.save()
        return violation
