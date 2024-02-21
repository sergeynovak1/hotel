from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = PhoneNumberField(unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['city'])
        ]

    def clean(self):
        """
        Checks the format of the phone number when saving the hotel object.
        """
        phone_number = to_python(self.phone)
        if phone_number and not phone_number.is_valid():
            raise ValidationError("Invalid phone number format")

    def __str__(self):
        return self.name
