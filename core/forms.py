from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password

from .models import Profile

User = get_user_model()


class StyledFormMixin:
    field_css_class = "pg-input"

    def _apply_styles(self):
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {self.field_css_class}".strip()


class SignUpForm(StyledFormMixin, forms.Form):
    ROLE_CHOICES = Profile.Role.choices

    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Sign up as")
    full_name = forms.CharField(label="Full name")
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False, label="Phone (customers)")
    organization = forms.CharField(required=False, help_text="Clinic / Pharmacy / Delivery fleet")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "full_name": "Laylo Karimova",
            "email": "saodat@pharmacygo.uz",
            "phone": "+998 90 123 45 67",
            "organization": "PharmaLife Downtown",
            "password1": "••••••••",
            "password2": "••••••••",
        }
        for name, placeholder in placeholders.items():
            if name in self.fields:
                self.fields[name].widget.attrs.setdefault("placeholder", placeholder)
        self._apply_styles()

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        email = (cleaned.get("email") or "").strip().lower()
        phone = (cleaned.get("phone") or "").strip()
        cleaned["email"] = email
        cleaned["phone"] = phone

        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")

        if role == Profile.Role.CUSTOMER and not phone:
            self.add_error("phone", "Customers must sign up with a phone number.")
        if role != Profile.Role.CUSTOMER and not email:
            self.add_error("email", "Doctors, admins, and distributors must use a work email.")

        identifier = phone if role == Profile.Role.CUSTOMER else email
        if identifier:
            if User.objects.filter(username__iexact=identifier).exists():
                self.add_error("email" if role != Profile.Role.CUSTOMER else "phone", "Account already exists for this identifier.")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")
        if password1:
            validate_password(password1)

        return cleaned

    def save(self):
        role = self.cleaned_data["role"]
        full_name = self.cleaned_data["full_name"]
        email = self.cleaned_data.get("email", "")
        phone = self.cleaned_data.get("phone", "")
        organization = self.cleaned_data.get("organization", "")
        password = self.cleaned_data["password1"]

        identifier = phone if role == Profile.Role.CUSTOMER else email
        user = User.objects.create_user(
            username=identifier,
            email=email,
            password=password,
            first_name=full_name,
        )

        profile = user.profile
        profile.role = role
        profile.phone = phone
        profile.organization = organization
        profile.save()
        return user


class IdentifierAuthenticationForm(StyledFormMixin, AuthenticationForm):
    username = forms.CharField(label="Email, username, or phone")
    role_hint = forms.ChoiceField(choices=Profile.Role.choices, label="Sign in as")

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields["username"].widget.attrs.setdefault("placeholder", "saodat@pharmacygo.uz or +998 90 123 45 67")
        self.fields["password"].widget.attrs.setdefault("placeholder", "••••••••")
        self.fields["role_hint"].widget.attrs.setdefault("class", "pg-input")
        self._apply_styles()

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        role_hint = self.cleaned_data.get("role_hint")

        if username and password:
            user = self._attempt_auth(username, password)
            if user is None:
                raise forms.ValidationError("Invalid credentials. Check your email/phone and password.")
            profile = getattr(user, "profile", None)
            if profile and role_hint and profile.role != role_hint:
                raise forms.ValidationError(
                    f"You selected {Profile.Role(role_hint).label} but this account is {profile.get_role_display()}."
                )
            self.confirm_login_allowed(user)
            self.user_cache = user
        return self.cleaned_data

    def _attempt_auth(self, identifier, password):
        from django.contrib.auth import authenticate

        user = authenticate(self.request, username=identifier, password=password)
        if user:
            return user

        email_matches = User.objects.filter(email__iexact=identifier).order_by("id")
        if email_matches.exists():
            email_match = email_matches.first()
            user = authenticate(self.request, username=email_match.username, password=password)
            if user:
                return user

        from .models import Profile

        try:
            profile = Profile.objects.select_related("user").get(phone=identifier)
            user = authenticate(self.request, username=profile.user.username, password=password)
            if user:
                return user
        except Profile.DoesNotExist:
            pass
        return None
