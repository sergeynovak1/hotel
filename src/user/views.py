from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from typing import Any, Union

from .forms import UserRegistrationForm
from .models import User


class SignUpView(View):
    template_name: str = 'user/registration.html'

    def _render(self, request: HttpRequest, form: UserRegistrationForm = None, message: str = None) -> HttpResponse:
        """Render the signup view with the provided form and message."""
        return render(request, self.template_name, {"form": form or UserRegistrationForm(), "message": message})

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests."""
        return self._render(request)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle POST requests."""
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            return self._handle_valid_form(request, form)
        else:
            return self._handle_invalid_form(request, form)

    def _handle_valid_form(self, request: HttpRequest, form: UserRegistrationForm) -> Union[HttpResponse, None]:
        """Handle form submission when the form is valid."""
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
        return self._render(request, form=form, message=message)

    def _handle_invalid_form(self, request: HttpRequest, form: UserRegistrationForm) -> HttpResponse:
        """Handle form submission when the form is invalid."""
        return self._render(request, form=form, message='Form submission failed')
