from django.contrib import admin

from .models import (
    ChatMessage,
    DeliveryTask,
    DistributorStatus,
    Notification,
    Order,
    Patient,
    PaymentCard,
    PaymentProvider,
    Pharmacy,
    PharmacyApplication,
    PrescriptionRequest,
    Profile,
    StockItem,
    TimelineEvent,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone", "organization", "created_at")
    list_filter = ("role",)
    search_fields = ("user__username", "user__first_name", "phone", "organization")


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ("name", "distance_km", "rating", "address")
    search_fields = ("name", "address")


@admin.register(PharmacyApplication)
class PharmacyApplicationAdmin(admin.ModelAdmin):
    list_display = ("pharmacy_name", "documents", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("pharmacy_name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("code", "customer_name", "pharmacy", "status", "eta_text", "created_at")
    list_filter = ("status",)
    search_fields = ("code", "customer_name")


@admin.register(PrescriptionRequest)
class PrescriptionRequestAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "medication", "condition", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("patient_name", "medication")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "condition", "contact", "status")
    search_fields = ("name", "condition")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("author", "sender", "body", "sent_at")
    list_filter = ("sender",)
    search_fields = ("author", "body")


@admin.register(PaymentProvider)
class PaymentProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "fee")


@admin.register(PaymentCard)
class PaymentCardAdmin(admin.ModelAdmin):
    list_display = ("owner_name", "provider", "last4", "theme", "spending_limit")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("message", "audience", "type", "created_at")
    list_filter = ("audience", "type")


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "quantity", "status", "expires_in_days")
    search_fields = ("sku", "name")


@admin.register(DeliveryTask)
class DeliveryTaskAdmin(admin.ModelAdmin):
    list_display = ("code", "pharmacy", "status", "eta_text", "address")
    list_filter = ("status",)


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ("label", "time_text", "is_active")


@admin.register(DistributorStatus)
class DistributorStatusAdmin(admin.ModelAdmin):
    list_display = ("order_code", "pharmacy", "status")
