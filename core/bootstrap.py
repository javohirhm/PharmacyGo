from datetime import datetime
from decimal import Decimal

from . import data
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


def _parse_distance(raw):
    raw = str(raw).replace('km', '').replace(' ', '').replace(',', '.')
    try:
        return Decimal(raw)
    except Exception:  # pragma: no cover - fallback
        return Decimal("0")


def _parse_time(raw):
    try:
        return datetime.strptime(raw, "%H:%M").time()
    except ValueError:
        return datetime.strptime("00:00", "%H:%M").time()


def _get_or_create_pharmacy(name):
    defaults = {
        "distance_km": Decimal("1.2"),
        "rating": Decimal("4.7"),
        "pin_top": "40%",
        "pin_left": "40%",
    }
    pharmacy, _ = Pharmacy.objects.get_or_create(name=name, defaults=defaults)
    return pharmacy


def ensure_seed_records():
    if not Pharmacy.objects.exists():
        for item in data.CUSTOMER_PHARMACIES:
            Pharmacy.objects.create(
                name=item["name"],
                distance_km=_parse_distance(item["distance"].replace(" km", "")),
                rating=Decimal(str(item["rating"])),
                pin_top=item["pin"]["top"],
                pin_left=item["pin"]["left"],
            )

    if not PharmacyApplication.objects.exists():
        for application in data.PHARMACY_APPROVALS:
            PharmacyApplication.objects.create(
                pharmacy_name=application["name"],
                documents=application["docs"],
                status=PharmacyApplication.Status.PENDING if application["status"].lower() == "pending" else PharmacyApplication.Status.REVIEW,
            )

    if not Order.objects.exists():
        status_map = {
            "Out for delivery": Order.Status.OUT,
            "Delivered": Order.Status.DELIVERED,
            "Awaiting courier": Order.Status.PENDING,
            "Packed": Order.Status.PACKED,
        }
        for recent in data.ADMIN_RECENT_ORDERS:
            Order.objects.create(
                code=recent["order_id"],
                customer_name=recent["customer"],
                pharmacy=_get_or_create_pharmacy(recent["pharmacy"]),
                status=status_map.get(recent["status"], Order.Status.PENDING),
                eta_text=recent["eta"],
                items="Care pack",
                progress=recent["status"],
            )
        for customer_order in data.CUSTOMER_ORDERS:
            code = customer_order["order_id"]
            if Order.objects.filter(code=code).exists():
                continue
            Order.objects.create(
                code=code,
                customer_name="Laylo Karimova",
                pharmacy=_get_or_create_pharmacy(data.CUSTOMER_PHARMACIES[0]["name"]),
                status=Order.Status.OUT if "Delivered" not in customer_order["status"] else Order.Status.DELIVERED,
                items=customer_order["items"],
                progress=customer_order["progress"],
                eta_text=customer_order["status"],
            )

    if not PrescriptionRequest.objects.exists():
        status_map = {
            "Awaiting": PrescriptionRequest.Status.AWAITING,
            "Approved": PrescriptionRequest.Status.APPROVED,
            "Rejected": PrescriptionRequest.Status.REJECTED,
        }
        for item in data.DOCTOR_PRESCRIPTIONS:
            PrescriptionRequest.objects.create(
                patient_name=item["patient"],
                condition=item["condition"],
                medication=item["requested"],
                status=status_map.get(item["status"], PrescriptionRequest.Status.AWAITING),
            )

    if not ChatMessage.objects.exists():
        for message in data.DOCTOR_CHAT:
            ChatMessage.objects.create(
                sender=message["sender"],
                author=message["name"],
                body=message["message"],
                sent_at=_parse_time(message["time"]),
            )

    if not Patient.objects.exists():
        for patient in data.DOCTOR_PATIENTS:
            Patient.objects.create(**patient)

    if not PaymentProvider.objects.exists():
        for provider in data.CUSTOMER_PAYMENTS:
            PaymentProvider.objects.create(
                name=provider["provider"],
                status=provider["status"],
                fee=provider["fee"],
            )

    if not PaymentCard.objects.exists():
        provider_lookup = {p.name: p for p in PaymentProvider.objects.all()}
        for card in data.CUSTOMER_CARDS:
            PaymentCard.objects.create(
                owner_name=card["holder"],
                provider=provider_lookup.get(card["provider"]),
                last4=card["ending"],
                theme=card["theme"],
                spending_limit=card["limit"],
            )

    if not Notification.objects.exists():
        for notice in data.CUSTOMER_NOTIFICATIONS:
            Notification.objects.create(
                audience=Profile.Role.CUSTOMER,
                message=notice["title"],
                type=notice["type"],
            )

    if not StockItem.objects.exists():
        for stock in data.DISTRIBUTOR_STOCK:
            StockItem.objects.create(
                sku=stock["sku"],
                name=stock["name"],
                quantity=stock["qty"],
                status=stock["status"],
                expires_in_days=stock.get("expires_in_days", 30),
            )

    if not DeliveryTask.objects.exists():
        status_map = {
            "Awaiting": DeliveryTask.Status.AWAITING,
            "In progress": DeliveryTask.Status.IN_PROGRESS,
            "Delivered": DeliveryTask.Status.DONE,
        }
        for task in data.DISTRIBUTOR_TASKS:
            DeliveryTask.objects.create(
                code=task["id"],
                pharmacy=_get_or_create_pharmacy(task["pharmacy"]),
                address=task["address"],
                eta_text=task["eta"],
                status=status_map.get(task["status"], DeliveryTask.Status.AWAITING),
            )

    if not TimelineEvent.objects.exists():
        for idx, event in enumerate(data.DISTRIBUTOR_TIMELINE):
            TimelineEvent.objects.create(
                label=event["label"],
                time_text=event["time"],
                is_active=(idx == 2),
            )

    if not DistributorStatus.objects.exists():
        for status in data.DISTRIBUTOR_STATUS_BOARD:
            DistributorStatus.objects.create(
                order_code=status["order_id"],
                pharmacy=status["pharmacy"],
                status=status["status"],
            )
