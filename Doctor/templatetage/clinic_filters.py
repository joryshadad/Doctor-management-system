from django import template

register = template.Library()

@register.filter(name='doctor_title')
def doctor_title(value):
    """فلتر مخصص يضيف لقب الدكتور قبل الاسم"""
    return f"د. {value}"