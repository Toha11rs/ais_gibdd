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
    token = models.IntegerField()

    class Meta:
        db_table = 'car'


###################################
# VIOLATION
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


class Violation(models.Model):
    typeWarning = models.ForeignKey(TypeWarning, on_delete=models.CASCADE)
    code = models.ForeignKey(CodeWarning, on_delete=models.CASCADE)
    warning = models.ForeignKey(GetWarning, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    class Meta:
        db_table = 'violation'


###################################
# PENALTY
###################################


class BaseValue (models.Model):
    BaseValue = models.IntegerField()

    class Meta:
        db_table = 'base_value'

    def __str__(self):
        return f"{self.BaseValue}"


class District (models.Model):
    District = models.CharField(max_length=100)

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


class Employee(models.Model):
    Name = models.CharField(max_length=100)
    Surname = models.CharField(max_length=100)
    Patronimyc = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=100)
    Position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        db_table = 'employee'


class Penalty (models.Model):
    PeymantPenalty = models.IntegerField()
    BaseValue = models.ForeignKey(BaseValue, on_delete=models.CASCADE)
    DateTime = models.DateTimeField()
    DeprivationDriving = models.DateField()
    Disrict = models.ForeignKey(District, on_delete=models.CASCADE)
    StatusPenalty = models.ForeignKey(StatusPenalty, on_delete=models.CASCADE)
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Violation = models.ForeignKey(Violation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'penalty'
