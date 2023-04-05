from django.db import models


class Status(models.Model):
    status = models.CharField(max_length=10)

    class Meta:
        db_table = 'status'


class DriverAddress(models.Model):
    City = models.CharField(max_length=50)
    Street = models.CharField(max_length=50)
    House = models.IntegerField()
    Flat = models.IntegerField()

    class Meta:
        db_table = 'driver_address'


class Driver(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    address = models.ForeignKey(DriverAddress, on_delete=models.CASCADE)

    class Meta:
        db_table = 'driver'


class DriverLicense(models.Model):
    number = models.IntegerField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    # address = models.ForeignKey(DriverAddress, on_delete=models.CASCADE)

    class Meta:
        db_table = 'driver_license'


class CarInformation(models.Model):
    Number = models.CharField(max_length=50)
    Brand = models.CharField(max_length=50)
    Model = models.CharField(max_length=50)
    Color = models.CharField(max_length=50)
    Year = models.IntegerField()
    RegistrationDate = models.DateField()

    class Meta:
        db_table = 'carInformation'


class Car(models.Model):
    carinformation = models.ForeignKey(
        CarInformation, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    token = models.IntegerField()

    class Meta:
        db_table = 'car'


class TypeWarning(models.Model):
    Type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.Type}"

    class Meta:
        db_table = 'type'


class CodeWarning(models.Model):
    Code = models.IntegerField()

    def __str__(self):
        return f"{self.Code}"

    class Meta:
        db_table = 'code'


class GetWarning(models.Model):
    GetWarning = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.GetWarning}"

    class Meta:
        db_table = 'warning'


class Violation(models.Model):
    typeWarning = models.ForeignKey(TypeWarning, on_delete=models.CASCADE)
    code = models.ForeignKey(CodeWarning, on_delete=models.CASCADE)
    warning = models.ForeignKey(GetWarning, on_delete=models.CASCADE)
    termDeprivation = models.IntegerField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    class Meta:
        db_table = 'violation'

    # penaltie = models.ForeignKey(Penaltie, on_delete=models.CASCADE)
    # employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
