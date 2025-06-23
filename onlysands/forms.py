import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Review


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 4:
            raise ValidationError("Username must be at least 4 characters long.")
        if len(username) > 30:
            raise ValidationError("Username cannot be longer than 30 characters.")
        if not re.match(r"^[A-Za-z0-9_.-]+$", username):
            raise ValidationError(
                "Usernames can only contain letters, numbers, underscores, hyphens, and periods."
            )
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"\d", password):
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )
        return password

    def clean_email(self):
        email = self.cleaned_data.get("email").strip().lower()
        email_regex = (
            r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"  # RFC 5322 pattern
        )

        if not re.match(email_regex, email):
            raise ValidationError("Please enter a valid email address.")

        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
        

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 7}),
            'text': forms.Textarea(attrs={'rows': 4}),
        }
