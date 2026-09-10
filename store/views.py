from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DoctorModelForm, DoctorProfileForm, ManualBookingForm, SearchForm
from .models import Booking, Doctor, DoctorProfile, Notification, Patient, Service


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    form = SearchForm(request.GET or None)
    doctors_list = Doctor.objects.with_profile().with_services().active().ordered()
    if form.is_valid():
        q = form.cleaned_data.get('q')
        specialty = form.cleaned_data.get('specialty')
        service = form.cleaned_data.get('service')
        if q:
            doctors_list = doctors_list.search(q)
        if specialty:
            doctors_list = doctors_list.by_specialty(specialty)
        if service:
            doctors_list = doctors_list.with_service(service.pk)
    return render(request, 'store/home.html', {'doctors': doctors_list, 'search_form': form})


def doctors(request):
    form = SearchForm(request.GET or None)
    doctors_list = Doctor.objects.with_profile().with_services().active().ordered()
    if form.is_valid():
        q = form.cleaned_data.get('q')
        specialty = form.cleaned_data.get('specialty')
        service = form.cleaned_data.get('service')
        if q:
            doctors_list = doctors_list.search(q)
        if specialty:
            doctors_list = doctors_list.by_specialty(specialty)
        if service:
            doctors_list = doctors_list.with_service(service.pk)
    return render(request, 'store/doctors.html', {'doctors': doctors_list, 'search_form': form})


def doctor_create(request):
    form = DoctorModelForm(request.POST or None)
    if form.is_valid():
        doctor = form.save()
        DoctorProfile.objects.get_or_create(doctor=doctor)
        return redirect('doctor_detail', doctor.pk)
    return render(request, 'store/doctor_form.html', {'form': form, 'title': 'إضافة طبيب'})


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor.objects.with_profile().with_services(), pk=pk)
    profile, _ = DoctorProfile.objects.get_or_create(doctor=doctor)
    return render(request, 'store/doctor_detail.html', {'doctor': doctor, 'profile': profile})


def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    form = DoctorModelForm(request.POST or None, instance=doctor)
    if form.is_valid():
        form.save()
        return redirect('doctor_detail', doctor.pk)
    return render(request, 'store/doctor_form.html', {'form': form, 'title': 'تعديل بيانات الطبيب'})


def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctors')
    return render(request, 'store/doctor_confirm_delete.html', {'doctor': doctor})


def doctor_profile_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    profile, _ = DoctorProfile.objects.get_or_create(doctor=doctor)
    form = DoctorProfileForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('doctor_detail', doctor.pk)
    return render(request, 'store/profile_form.html', {'form': form, 'doctor': doctor})


def patients(request):
    patients_list = Patient.objects.all().order_by('name')
    return render(request, 'store/patients.html', {'patients': patients_list})


def booking(request):
    form = ManualBookingForm(request.POST or None)
    if form.is_valid():
        doctor = form.cleaned_data['doctor_object']
        service = form.cleaned_data['service_object']
        Booking.objects.create(created_by=request.user if request.user.is_authenticated else None,
                               doctor=doctor.name, patient=form.cleaned_data['patient'], service=service.service_name,
                               price=service.price, date=form.cleaned_data['date'], time=form.cleaned_data['time'])
        return redirect('booking')
    bookings_list = Booking.objects.all().order_by('-date', '-time')
    q = request.GET.get('q')
    if q:
        bookings_list = bookings_list.filter(Q(patient__icontains=q) | Q(doctor__icontains=q) | Q(service__icontains=q))
    max_price = request.GET.get('max_price')
    if max_price and max_price.isdigit():
        bookings_list = bookings_list.filter(price__lte=max_price)
    sort_price = request.GET.get('sort_price')
    if sort_price in {'asc', 'desc'}:
        bookings_list = bookings_list.order_by('price' if sort_price == 'asc' else '-price')
    limit = request.GET.get('limit')
    if limit and limit.isdigit():
        bookings_list = bookings_list[:int(limit)]
    return render(request, 'store/booking.html', {'form': form, 'doctors': Doctor.objects.active().ordered(),
                   'patients': Patient.objects.all().order_by('name'), 'services': Service.objects.all().order_by('service_name'),
                   'bookings': bookings_list})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        if not username or not password:
            messages.error(request, 'يرجى إدخال اسم المستخدم وكلمة المرور.')
        elif password != password_confirm:
            messages.error(request, 'كلمتا المرور غير متطابقتين.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'اسم المستخدم مستخدم مسبقًا.')
        else:
            user = User.objects.create_user(username=username, email=request.POST.get('email', '').strip(), password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'store/register.html')


def notifications(request):
    if not request.user.is_authenticated:
        return redirect('login')
    items = Notification.objects.filter(recipient=request.user)
    return render(request, 'store/notifications.html', {'notifications': items})


def notification_read(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if request.method == 'POST':
        notification.is_read = True
        notification.save(update_fields=['is_read'])
    return redirect('notifications')
