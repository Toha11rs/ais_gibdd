from django.db import models


class Status(models.Model):
    status = models.CharField(max_length=10)

    class Meta:
        db_table = 'status'


class Driver(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    class Meta:
        db_table = 'driver'


class DriverLicense(models.Model):
    number = models.IntegerField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    class Meta:
        db_table = 'driver_license'


class DriverAddress(models.Model):
    City = models.CharField(max_length=50)
    Street = models.CharField(max_length=50)
    House = models.IntegerField()
    Flat = models.IntegerField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    class Meta:
        db_table = 'driver_address'
