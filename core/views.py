from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.crypto import get_random_string

from . import data
from .bootstrap import ensure_seed_records
from .forms import IdentifierAuthenticationForm, PaymentCardForm, SignUpForm, StockItemForm
from .models import (
    DeliveryTask,
    DistributorStatus,
    Notification,
    Order,
    PaymentCard,
    PaymentProvider,
    Pharmacy,
    PharmacyApplication,
    Profile,
    StockItem,
    TimelineEvent,
)


ROLE_TO_URL = {
    Profile.Role.ADMIN: "admin_dashboard",
    Profile.Role.CUSTOMER: "customer_dashboard",
    Profile.Role.DISTRIBUTOR: "distributor_dashboard",
    Profile.Role.PHARMACY: "pharmacy_store_dashboard",
}


def _context(request=None, **extra):
    if request and request.user.is_authenticated:
        active_user = request.user.get_full_name() or request.user.username
        primary_dashboard = _redirect_for_role(request.user)
    else:
        active_user = "Guest"
        primary_dashboard = None
    base = {
        "current_year": data.CURRENT_YEAR,
        "active_user": active_user,
        "primary_dashboard": primary_dashboard,
    }
    base.update(extra)
    return base


def _get_profile(user):
    profile = getattr(user, "profile", None)
    if profile:
        return profile
    profile, _ = Profile.objects.get_or_create(user=user, defaults={"role": Profile.Role.CUSTOMER})
    return profile


def _redirect_for_role(user):
    profile = _get_profile(user)
    role = profile.role or Profile.Role.CUSTOMER
    return ROLE_TO_URL.get(role, "customer_dashboard")


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            profile = _get_profile(request.user)
            if profile.role != role:
                return redirect(_redirect_for_role(request.user))
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator


def login_view(request):
    if request.user.is_authenticated:
        return redirect(_redirect_for_role(request.user))

    ensure_seed_records()
    form = IdentifierAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect(_redirect_for_role(request.user))

    context = _context(
        request,
        page_title="Access",
        roles=data.AUTH_ROLES,
        pharmacies=Pharmacy.objects.all(),
        form=form,
    )
    return render(request, "core/login.html", context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect(_redirect_for_role(request.user))

    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to PharmacyGo! Your workspace is ready.")
        return redirect(_redirect_for_role(user))

    context = _context(
        request,
        page_title="Create account",
        roles=data.AUTH_ROLES,
        form=form,
    )
    return render(request, "core/signup.html", context)


def forgot_password_view(request):
    context = _context(
        request,
        page_title="Reset password",
    )
    return render(request, "core/forgot_password.html", context)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Signed out of PharmacyGo.")
    return redirect("login")


@role_required(Profile.Role.ADMIN)
def admin_dashboard(request):
    ensure_seed_records()
    orders = Order.objects.select_related("pharmacy").order_by("-created_at")[:5]
    applications = PharmacyApplication.objects.order_by("-created_at")[:5]
    user_segments = {
        "customers": _segment_profiles(Profile.Role.CUSTOMER)[:5],
        "stores": _segment_profiles(Profile.Role.PHARMACY)[:5],
        "distributors": _segment_profiles(Profile.Role.DISTRIBUTOR)[:5],
    }
    context = _context(
        request,
        page_title="Admin control",
        admin_kpis=data.ADMIN_KPIS,
        orders=orders,
        user_segments=user_segments,
        approvals=applications,
        admin_change_url=_admin_change_url,
    )
    return render(request, "core/admin_dashboard.html", context)


@role_required(Profile.Role.CUSTOMER)
def customer_dashboard(request):
    ensure_seed_records()
    card_form = PaymentCardForm()
    if request.method == "POST" and request.POST.get("form") == "payment-card":
        card_form = PaymentCardForm(request.POST)
        if card_form.is_valid():
            card_form.save()
            messages.success(request, "New payment card added to your wallet.")
            return redirect("customer_dashboard")
        messages.error(request, "Please fix the errors below and resubmit the card form.")

    context = _context(
        request,
        page_title="Customer journey",
        pharmacies=Pharmacy.objects.all(),
        orders=Order.objects.order_by("-created_at")[:4],
        payments=PaymentProvider.objects.all(),
        cards=PaymentCard.objects.select_related("provider").all(),
        notifications=Notification.objects.filter(audience=Profile.Role.CUSTOMER).order_by("-created_at")[:5],
        card_form=card_form,
    )
    return render(request, "core/customer_dashboard.html", context)


@role_required(Profile.Role.PHARMACY)
def pharmacy_store_dashboard(request):
    ensure_seed_records()
    stock_form = StockItemForm()
    if request.method == "POST" and request.POST.get("form") == "stock-item":
        stock_form = StockItemForm(request.POST)
        if stock_form.is_valid():
            stock_form.save()
            messages.success(request, "SKU saved to stock health.")
            return redirect("pharmacy_store_dashboard")
        messages.error(request, "Please fix the stock form errors.")

    expires_param = request.GET.get("expires")
    expiry_threshold = None
    filtered_stock = StockItem.objects.all().order_by("expires_in_days", "name")
    if expires_param:
        try:
            expiry_threshold = int(expires_param)
            filtered_stock = filtered_stock.filter(expires_in_days__lte=expiry_threshold)
        except ValueError:
            expiry_threshold = None
    expiry_options = [
        {"value": 30, "label": "30 days"},
        {"value": 10, "label": "10 days"},
        {"value": 90, "label": "3 months"},
    ]

    context = _context(
        request,
        page_title="Pharmacy store inventory",
        stock=StockItem.objects.order_by("-updated_at"),
        stock_form=stock_form,
        expiry_options=expiry_options,
        expiry_threshold=expiry_threshold,
        filtered_stock=filtered_stock,
    )
    return render(request, "core/pharmacy_store_dashboard.html", context)


@role_required(Profile.Role.DISTRIBUTOR)
def distributor_dashboard(request):
    ensure_seed_records()
    status_options = []
    seen = set()
    preset_statuses = ["Awaiting pickup", "In progress", "Delivered", "Delayed"]
    for label in preset_statuses + list(DistributorStatus.objects.values_list("status", flat=True)):
        normalized = (label or "").strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            status_options.append(normalized)

    context = _context(
        request,
        page_title="Distributor ops",
        tasks=DeliveryTask.objects.select_related("pharmacy").all(),
        timeline=TimelineEvent.objects.order_by("created_at"),
        status_board=DistributorStatus.objects.all(),
        status_options=status_options,
    )
    return render(request, "core/distributor_dashboard.html", context)


def _admin_change_url(obj):
    opts = obj._meta
    return reverse(f"admin:{opts.app_label}_{opts.model_name}_change", args=[obj.pk])


def _segment_profiles(role):
    qs = Profile.objects.filter(role=role).select_related("user").order_by("-created_at")
    formatted = []
    for profile in qs:
        formatted.append(
            {
                "profile": profile,
                "name": profile.user.get_full_name() or profile.user.username,
                "contact": profile.phone or profile.user.email or "—",
                "meta": profile.organization or profile.get_role_display(),
                "admin_url": _admin_change_url(profile),
            }
        )
    return formatted


def _redirect_back(request, fallback_name):
    fallback = reverse(fallback_name)
    return redirect(request.META.get("HTTP_REFERER") or fallback)


@role_required(Profile.Role.ADMIN)
def order_action(request, pk, action):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        if action == "deliver":
            order.status = Order.Status.DELIVERED
            order.progress = "Delivered"
            order.eta_text = "Completed"
        elif action == "out":
            order.status = Order.Status.OUT
            order.progress = "Out for delivery"
            order.eta_text = "15 min"
        elif action == "cancel":
            order.status = Order.Status.CANCELLED
            order.progress = "Cancelled"
            order.eta_text = "—"
        order.save()
        messages.success(request, f"Order {order.code} updated.")
    return _redirect_back(request, "admin_dashboard")


@role_required(Profile.Role.ADMIN)
def application_action(request, pk, action):
    application = get_object_or_404(PharmacyApplication, pk=pk)
    if request.method == "POST":
        if action == "approve":
            application.status = PharmacyApplication.Status.APPROVED
        elif action == "reject":
            application.status = PharmacyApplication.Status.REJECTED
        application.save()
        messages.success(request, f"{application.pharmacy_name} status updated.")
    return _redirect_back(request, "admin_dashboard")


@role_required(Profile.Role.DISTRIBUTOR)
def delivery_task_action(request, pk, action):
    task = get_object_or_404(DeliveryTask, pk=pk)
    if request.method == "POST":
        if action == "accept":
            task.status = DeliveryTask.Status.IN_PROGRESS
        elif action == "complete":
            task.status = DeliveryTask.Status.DONE
        elif action == "reject":
            task.status = DeliveryTask.Status.AWAITING
        task.save()
        messages.success(request, f"{task.code} set to {task.get_status_display()}.")
    return _redirect_back(request, "distributor_dashboard")


@role_required(Profile.Role.DISTRIBUTOR)
def distributor_status_action(request, pk):
    status_entry = get_object_or_404(DistributorStatus, pk=pk)
    if request.method == "POST":
        status_entry.status = "Delivered"
        status_entry.save()
        messages.success(request, f"{status_entry.order_code} marked delivered.")
    return _redirect_back(request, "distributor_dashboard")


@role_required(Profile.Role.CUSTOMER)
def create_customer_order(request):
    if request.method == "POST":
        pharmacy_id = request.POST.get("pharmacy")
        items = request.POST.get("items", "").strip()
        pharmacy = get_object_or_404(Pharmacy, pk=pharmacy_id)
        generated_code = f"#PG-{get_random_string(4).upper()}"
        Order.objects.create(
            code=request.POST.get("order_code") or generated_code,
            customer_name=request.user.get_full_name() or request.user.username,
            pharmacy=pharmacy,
            items=items or "Custom selection",
            progress="Requested",
            status=Order.Status.PENDING,
            eta_text="TBD",
        )
        messages.success(request, "New delivery request created.")
    return _redirect_back(request, "customer_dashboard")


@role_required(Profile.Role.CUSTOMER)
def pharmacy_detail(request, pk):
    ensure_seed_records()
    pharmacy = get_object_or_404(Pharmacy, pk=pk)
    context = _context(
        request,
        page_title=f"{pharmacy.name} · Details",
        pharmacy=pharmacy,
        recent_orders=pharmacy.orders.order_by("-created_at")[:5],
    )
    return render(request, "core/pharmacy_detail.html", context)


@role_required(Profile.Role.DISTRIBUTOR)
def delivery_detail(request, pk):
    ensure_seed_records()
    task = get_object_or_404(DeliveryTask.objects.select_related("pharmacy"), pk=pk)
    context = _context(
        request,
        page_title=f"{task.code} · Delivery detail",
        task=task,
    )
    return render(request, "core/delivery_detail.html", context)


@role_required(Profile.Role.DISTRIBUTOR)
def distributor_status_update(request, pk):
    status_entry = get_object_or_404(DistributorStatus, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status", "").strip()
        if new_status:
            status_entry.status = new_status
            status_entry.save()
            messages.success(request, f"{status_entry.order_code} updated to {new_status}.")
        else:
            messages.error(request, "Select a valid status option.")
    return _redirect_back(request, "distributor_dashboard")
