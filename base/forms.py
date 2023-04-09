from django import forms
from ais.models import TypeWarning, CodeWarning, GetWarning, Violation


class SearchForm(forms.Form):
    number = forms.IntegerField(
        label='Введите номер водительского удостоверения')


class ViolationForm(forms.ModelForm):
    typeWarning = forms.ModelChoiceField(queryset=TypeWarning.objects.all())
    code = forms.ModelChoiceField(queryset=CodeWarning.objects.all())
    warning = forms.ModelChoiceField(queryset=GetWarning.objects.all())
    termDeprivation = forms.IntegerField()

    class Meta:
        model = Violation
        fields = ['typeWarning', 'code', 'warning', 'termDeprivation']
