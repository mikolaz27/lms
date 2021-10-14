from django.core.exceptions import ValidationError


def no_elon_validator(email):
    if "elon" in email.lower():
        raise ValidationError("No more Elons, please!")
