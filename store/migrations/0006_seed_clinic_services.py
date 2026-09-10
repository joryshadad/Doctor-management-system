from django.db import migrations


def seed_services(apps, schema_editor):
    Service = apps.get_model('store', 'Service')
    services = [
        ('جهاز ايكو للقلب', 50, 'فحص وتصوير صدى القلب ECHO.'),
        ('فحص CBC', 15, 'فحص الدم الشامل.'),
        ('تخطيط قلب', 20, 'تسجيل الإشارات الكهربائية للقلب.'),
    ]
    for name, price, description in services:
        Service.objects.get_or_create(
            service_name=name,
            defaults={'price': price, 'description': description},
        )


def remove_seeded_services(apps, schema_editor):
    Service = apps.get_model('store', 'Service')
    Service.objects.filter(service_name__in=['جهاز ايكو للقلب', 'فحص CBC', 'تخطيط قلب']).delete()


class Migration(migrations.Migration):
    dependencies = [('store', '0005_doctor_is_active_doctor_services_alter_booking_date_and_more')]
    operations = [migrations.RunPython(seed_services, remove_seeded_services)]
