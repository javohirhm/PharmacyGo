from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        DOCTOR = "doctor", "Doctor"
        CUSTOMER = "customer", "Customer"
        DISTRIBUTOR = "distributor", "Distributor"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField(max_length=32, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} · {self.get_role_display()}"


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def admin_url(self):
        opts = self._meta
        return reverse(f"admin:{opts.app_label}_{opts.model_name}_change", args=[self.pk])


class Pharmacy(TimeStampedModel):
    name = models.CharField(max_length=255)
    distance_km = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    address = models.CharField(max_length=255, blank=True)
    pin_top = models.CharField(max_length=8, default="50%")
    pin_left = models.CharField(max_length=8, default="50%")

    def __str__(self):
        return self.name


class PharmacyApplication(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REVIEW = "review", "Review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    pharmacy_name = models.CharField(max_length=255)
    documents = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.pharmacy_name} ({self.get_status_display()})"


class Order(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PACKED = "packed", "Packed"
        OUT = "out", "Out for delivery"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    code = models.CharField(max_length=32, unique=True)
    customer_name = models.CharField(max_length=255)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    items = models.CharField(max_length=255, blank=True)
    progress = models.CharField(max_length=64, blank=True)
    eta_text = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.code


class PrescriptionRequest(TimeStampedModel):
    class Status(models.TextChoices):
        AWAITING = "awaiting", "Awaiting"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    patient_name = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    medication = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AWAITING)

    def __str__(self):
        return f"{self.patient_name} · {self.medication}"


class Patient(TimeStampedModel):
    name = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    contact = models.CharField(max_length=64)
    status = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class ChatMessage(TimeStampedModel):
    class Sender(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        DOCTOR = "doctor", "Doctor"

    sender = models.CharField(max_length=20, choices=Sender.choices)
    author = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.TimeField()

    def __str__(self):
        return f"{self.author}: {self.body[:40]}"


class PaymentProvider(TimeStampedModel):
    name = models.CharField(max_length=64)
    status = models.CharField(max_length=64, default="Connected")
    fee = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class PaymentCard(TimeStampedModel):
    owner_name = models.CharField(max_length=255)
    provider = models.ForeignKey(PaymentProvider, on_delete=models.CASCADE, related_name="cards")
    last4 = models.CharField(max_length=4)
    theme = models.CharField(max_length=32, default="ocean")
    spending_limit = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.provider.name} · ••{self.last4}"


class Notification(TimeStampedModel):
    class Type(models.TextChoices):
        INFO = "info", "Info"
        SUCCESS = "success", "Success"
        WARNING = "warning", "Warning"

    audience = models.CharField(max_length=20, choices=Profile.Role.choices, default=Profile.Role.CUSTOMER)
    message = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.INFO)

    def __str__(self):
        return self.message


class StockItem(TimeStampedModel):
    sku = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=64, default="Healthy")

    def __str__(self):
        return self.name


class DeliveryTask(TimeStampedModel):
    class Status(models.TextChoices):
        AWAITING = "awaiting", "Awaiting"
        IN_PROGRESS = "in_progress", "In progress"
        DONE = "done", "Delivered"

    code = models.CharField(max_length=32)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="delivery_tasks")
    address = models.CharField(max_length=255)
    eta_text = models.CharField(max_length=64)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AWAITING)

    def __str__(self):
        return self.code


class TimelineEvent(TimeStampedModel):
    label = models.CharField(max_length=64)
    time_text = models.CharField(max_length=32)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.label


class DistributorStatus(TimeStampedModel):
    order_code = models.CharField(max_length=64)
    pharmacy = models.CharField(max_length=255)
    status = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.order_code} · {self.status}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
