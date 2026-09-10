from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def doctor(request):
    return render(request, "doctor.html")

def index(request):

    clinic_name = "Clinic Care"
    doctor_name = "Gamal Osran"
    patient_name = "Mohammed Saleh"
    city = "Ibb"
    message = "Welcome To Clinic Care System"
    description = "Clinic Management System"
    age = 22
    is_open = True

    departments = [
        "الأسنان",
        "القلب",
        "العيون",
        "العظام",
        "الأطفال"
    ]

    context = {
        "clinic_name": clinic_name,
        "doctor_name": doctor_name,
        "patient_name": patient_name,
        "city": city,
        "message": message,
        "description": description,
        "age": age,
        "is_open": is_open,
        "departments": departments,
    }

    return render(request, "index.html", context)

def patient(request):
    return render(request, "patient.html")

def departments(request):
    return render(request, "departments.html")

def services(request):
    return render(request, "services.html")

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")

def doctor(request):
    return render(request, 'doctor.html')

def patient(request):
    return render(request, 'patient.html')

def booking(request):
    return render(request, 'booking.html')