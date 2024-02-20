from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

from .forms import UserRegistrationForm
from .models import User


class SignUpView(View):
    template_name = 'user/registration.html'

    def _render(self, request, form=None, message=None):
        return render(request, self.template_name, {
            "form": form or UserRegistrationForm(),
            "message": message
        })

    def get(self, request, *args, **kwargs):
        return self._render(request)

    def post(self, request, *args, **kwargs):
        message = None
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if password:
                try:
                    user = User.objects.create_superuser(email=email, password=password)
                    login(request, user)
                    return redirect('admin:index')
                except Exception as e:
                    message = 'An error occurred while creating the user.'
            else:
                message = 'Password is required.'
        else:
            message = 'Form submission failed'

        return self._render(request, form=form, message=message)
