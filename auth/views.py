# views.py
from django.shortcuts import render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.views import View
from users.models import User


class PasswordResetConfirmView(View):
    """
    View to handle the password reset form
    """
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            # Token is valid, show password reset form
            form = SetPasswordForm(user)
            return render(request, 'password_reset_confirm.html', {
                'form': form,
                'uidb64': uidb64,
                'token': token,
                'validlink': True
            })
        else:
            # Invalid link
            return render(request, 'password_reset_confirm.html', {'validlink': False})
    
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'password_reset_complete.html')
            else:
                return render(request, 'password_reset_confirm.html', {
                    'form': form,
                    'uidb64': uidb64,
                    'token': token,
                    'validlink': True
                })
        else:
            return render(request, 'password_reset_confirm.html', {'validlink': False})