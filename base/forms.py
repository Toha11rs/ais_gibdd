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
    typeWarning = forms.ModelChoiceField(queryset=TypeWarning.objects.all())
    code = forms.ModelChoiceField(queryset=CodeWarning.objects.all())
    warning = forms.ModelChoiceField(queryset=GetWarning.objects.all())

    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(), required=False)

    class Meta:
        model = Violation
        fields = ['typeWarning', 'code',
                  'warning', 'termDeprivation', 'driver']

    # def save(self, driver, commit=True):
    #     violation = super().save(commit=False)
    #     violation.driver = driver
    #     if commit:
    #         violation.save()
    #     return violation
