
from django.forms import IntegerField
from django.core.exceptions import ValidationError


class YearField(IntegerField):
    def validate(self, value):
        super().validate(value)
        if not (1950 <= value <= 2023):
            raise ValidationError(
                'Год автомобиля должен быть от 1950 до 2023 года')
