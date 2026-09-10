from django import forms
from .models import Doctor, DoctorProfile, Service


class DoctorModelForm(forms.ModelForm):
    """الطريقة الأولى: ModelForm تُنشئ الحقول من نموذج Doctor تلقائيًا."""

    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'phone', 'is_active', 'services']
        widgets = {
            'services': forms.CheckboxSelectMultiple(),
            'phone': forms.TextInput(attrs={'placeholder': 'مثال: 777000000'}),
        }


class SearchForm(forms.Form):
    """الطريقة الثانية: forms.Form لنموذج بحث مستقل."""

    q = forms.CharField(required=False, label='كلمة البحث')
    specialty = forms.CharField(required=False, label='التخصص')
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(), required=False, empty_label='كل الخدمات', label='الخدمة'
    )


class DoctorProfileForm(forms.ModelForm):
    """ModelForm لعلاقة One-to-One وملف الطبيب."""

    class Meta:
        model = DoctorProfile
        fields = ['bio', 'room_number']
        widgets = {'bio': forms.Textarea(attrs={'rows': 4})}


class ManualBookingForm(forms.Form):
    """الطريقة الثالثة: Form يدوي متوافق مع قالب الحجز الأصلي."""

    doctor = forms.ChoiceField(label='الطبيب')
    patient = forms.CharField(max_length=100, label='اسم المريض')
    service = forms.ChoiceField(label='الخدمة')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='التاريخ')
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='الوقت')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doctor_queryset = Doctor.objects.active().ordered()
        self.service_queryset = Service.objects.all().order_by('service_name')
        self.fields['doctor'].choices = [('', '-- اختر الطبيب --')] + [
            (doctor.name, f'{doctor.name} ({doctor.specialty})')
            for doctor in self.doctor_queryset
        ]
        self.fields['service'].choices = [('', '-- اختر الخدمة المطلوبة --')] + [
            (service.service_name, f'{service.service_name} ({service.price} ريال)')
            for service in self.service_queryset
        ]

    def clean(self):
        cleaned = super().clean()
        doctor_name = cleaned.get('doctor')
        service_name = cleaned.get('service')
        doctor = self.doctor_queryset.filter(name=doctor_name).first()
        service = self.service_queryset.filter(service_name=service_name).first()
        if doctor_name and not doctor:
            self.add_error('doctor', 'الطبيب غير موجود أو غير متاح.')
        if service_name and not service:
            self.add_error('service', 'الخدمة غير موجودة.')
        cleaned['doctor_object'] = doctor
        cleaned['service_object'] = service
        return cleaned
