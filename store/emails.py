from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_welcome_email(user):
    """ترسل رسالة ترحيب متعددة الأجزاء عند إنشاء حساب جديد."""
    if not user.email:
        return 0

    context = {"user": user}
    text_body = (
        f"مرحبًا {user.username}\n\n"
        "تم إنشاء حسابك في نظام إدارة العيادة بنجاح.\n"
        "يمكنك الآن تصفح الأطباء وإدارة الحجوزات."
    )
    html_body = render_to_string("emails/welcome.html", context)
    message = EmailMultiAlternatives(
        subject="مرحبًا بك في نظام إدارة العيادة",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    message.attach_alternative(html_body, "text/html")
    return message.send()
