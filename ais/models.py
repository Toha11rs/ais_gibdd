from django.db import models

###################################
# DRIVER
###################################


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


###################################
# DRIVER_LICENSE
###################################


class Status(models.Model):
    status = models.CharField(max_length=10)

    class Meta:
        db_table = 'status'


class DriverLicense(models.Model):
    number = models.IntegerField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    # address = models.ForeignKey(DriverAddress, on_delete=models.CASCADE)

    class Meta:
        db_table = 'driver_license'


###################################
# CAR
###################################

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

    class Meta:
        db_table = 'car'


###################################
# PENALTY
###################################

class TypeWarning(models.Model):
    Type = models.CharField(max_length=50)

    class Meta:
        db_table = 'type'

    def __str__(self):
        return f"{self.Type}"


class CodeWarning(models.Model):
    Code = models.IntegerField()

    class Meta:
        db_table = 'code'

    def __str__(self):
        return f"{self.Code}"


class GetWarning(models.Model):
    GetWarning = models.CharField(max_length=50)

    class Meta:
        db_table = 'warning'

    def __str__(self):
        return f"{self.GetWarning}"


class BaseValue (models.Model):
    BaseValue = models.IntegerField()

    class Meta:
        db_table = 'base_value'

    def __str__(self):
        return f"{self.BaseValue}"


class District (models.Model):
    District = models.CharField(max_length=200)

    class Meta:
        db_table = 'district'

    def __str__(self):
        return f"{self.District}"


class StatusPenalty(models.Model):
    StatusPenalty = models.CharField(max_length=100)

    class Meta:
        db_table = 'status_penalty'

    def __str__(self):
        return f"{self.StatusPenalty}"


class Position(models.Model):
    Position = models.CharField(max_length=100)

    class Meta:
        db_table = 'position'

    def __str__(self):
        return f"{self.Position}"

###################################
# EMPLOYEE
###################################


class Employee(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronimyc = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=100)
    Position = models.ForeignKey(Position, on_delete=models.CASCADE)
    number = models.IntegerField()
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'employee'

    def __str__(self):
        return f"{self.name}"

###################################
# Penalty
###################################


class Penalty (models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    typeWarning = models.ForeignKey(TypeWarning, on_delete=models.CASCADE)
    code = models.ForeignKey(CodeWarning, on_delete=models.CASCADE)
    warning = models.ForeignKey(GetWarning, on_delete=models.CASCADE)
    PeymantPenalty = models.IntegerField()
    baseValue = models.ForeignKey(BaseValue, on_delete=models.CASCADE)
    DateTime = models.DateField()
    deprivationDriving = models.IntegerField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    statusPenalty = models.ForeignKey(StatusPenalty, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        db_table = 'penalty'

###################################
# VIOLATION
###################################


class Violation(models.Model):
    typeWarning = models.ForeignKey(TypeWarning, on_delete=models.CASCADE)
    code = models.ForeignKey(CodeWarning, on_delete=models.CASCADE)
    warning = models.ForeignKey(GetWarning, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    class Meta:
        db_table = 'violation'
