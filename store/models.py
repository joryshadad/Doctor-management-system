from django.contrib.auth.models import User
from django.db import models


class DoctorQuerySet(models.QuerySet):
    """دوال QuerySet مخصصة للبحث والتصفية في بيانات الأطباء."""

    def by_name(self, value):
        return self.filter(name__icontains=value)

    def by_specialty(self, value):
        return self.filter(specialty__icontains=value)

    def with_service(self, service_id):
        return self.filter(services__id=service_id)

    def active(self):
        return self.filter(is_active=True)

    def ordered(self, field='name'):
        allowed = {'name', '-name', 'specialty', '-specialty'}
        return self.order_by(field if field in allowed else 'name')

    def search(self, value):
        return self.filter(
            models.Q(name__icontains=value)
            | models.Q(specialty__icontains=value)
            | models.Q(phone__icontains=value)
        )

    def with_profile(self):
        return self.select_related('profile').prefetch_related('services')

    def with_services(self):
        return self.prefetch_related('services')

    def newest(self):
        return self.order_by('-id')


class Doctor(models.Model):
    name = models.CharField(max_length=100, verbose_name='اسم الطبيب')
    specialty = models.CharField(max_length=100, verbose_name='التخصص')
    phone = models.CharField(max_length=20, verbose_name='الهاتف', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='متاح للحجز')

    objects = DoctorQuerySet.as_manager()

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=100, verbose_name='اسم المريض')
    age = models.IntegerField(verbose_name='العمر')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')

    def __str__(self):
        return self.name


class Service(models.Model):
    service_name = models.CharField(max_length=100, verbose_name='اسم الخدمة')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر')
    description = models.TextField(verbose_name='الوصف', blank=True)

    def __str__(self):
        return self.service_name


class DoctorProfile(models.Model):
    """علاقة One-to-One: لكل طبيب ملف مهني واحد فقط."""
    doctor = models.OneToOneField(
        Doctor, on_delete=models.CASCADE, related_name='profile', verbose_name='الطبيب'
    )
    bio = models.TextField(blank=True, verbose_name='نبذة')
    room_number = models.CharField(max_length=20, blank=True, verbose_name='رقم العيادة')

    def __str__(self):
        return f'ملف {self.doctor.name}'


# علاقة Many-to-Many: الطبيب يستطيع تقديم عدة خدمات، والخدمة يقدمها عدة أطباء.
Doctor.add_to_class(
    'services',
    models.ManyToManyField(Service, blank=True, related_name='doctors', verbose_name='الخدمات')
)


class Booking(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings', verbose_name='أنشأه')
    doctor = models.CharField(max_length=100, verbose_name='الطبيب')
    patient = models.CharField(max_length=100, verbose_name='المريض')
    service = models.CharField(max_length=100, verbose_name='الخدمة')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='السعر')
    date = models.DateField(verbose_name='التاريخ')
    time = models.TimeField(verbose_name='الوقت')

    def __str__(self):
        return f'{self.patient} - {self.service} - {self.date}'


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='المستلم')
    message = models.CharField(max_length=255, verbose_name='الرسالة')
    link = models.CharField(max_length=255, blank=True, verbose_name='الرابط')
    is_read = models.BooleanField(default=False, verbose_name='مقروء')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='وقت الإنشاء')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.recipient.username}: {self.message}'
