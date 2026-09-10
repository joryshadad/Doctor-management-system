from django.db import models

class Booking(models.Model):
    doctor = models.CharField(max_length=100)
    patient = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.patient} - {self.service}"
# 1. إنشاء جدول الأطباء
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 2. إنشاء جدول المرضى
class Patient(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# 3. جدول الحجوزات مع الربط (Foreign Key)
class Booking(models.Model):
    # الربط بجدول الأطباء
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    # الربط بجدول المرضى
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
   
    service = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.patient.name} - {self.service}"