from django.core.mail import send_mail
from django.shortcuts import redirect

def send_login_email(request):
    send_mail(
        'Your login link for Superlists', 
        'body text',
        'amirrezaamp2170@gmail.com', 
        ['mysuperlists2170@gmail.com'],
    )
    return redirect('/')
