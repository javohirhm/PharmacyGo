# PharmacyGo

PharmacyGo is a Django-powered prototype that unifies every stakeholder in the pharmacy delivery journey: Admins, Doctors, Customers, and Distributors. The UI focuses on a clean white/blue system with dark-mode support, consistent spacing, and smooth hover transitions.

## Features

- **Single auth flow** with role selection, dedicated sign-up (phone-first for customers, email for professionals), and a dummy forgot-password process.
- **Universal layout** featuring a shared navbar, text-based PharmacyGo logo, profile pill, and a global dark/light toggle persisted with `localStorage`.
- **Admin workspace** delivering KPI cards, order controls (mark delivered, cancel), live user segments, and pharmacy approval queues hooked to real models.
- **Doctor tools** to triage prescriptions, approve/reject requests, chat with customers, and review patient rosters — all persisted.
- **Customer experience** combining a mock Google Maps card with DB-backed pharmacies, order creation form, payment connectors (Uzum, Uzcard, Humo), theme-able cards, and notification feeds.
- **Distributor cockpit** for stock snapshots, accepting or rejecting delivery tasks, updating statuses, and visualizing fulfillment timelines through editable models.
- **Seed + admin management**: `core/bootstrap.py` hydrates the DB with realistic data on first run so every section has content that you can later edit in Django admin.

## Getting Started

1. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations** to set up the SQLite database:
   ```bash
   python manage.py migrate
   ```
4. (Optional) **Create an internal admin user** for Django admin access or to seed other roles:
   ```bash
   python manage.py createsuperuser
   ```
5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```
6. Visit `http://127.0.0.1:8000/` to use the live login/sign-up flow. The role you register with dictates which dashboard becomes available; authenticated users are redirected automatically.

### Managing live data

- The first request seeds demo pharmacies, orders, prescriptions, cards, etc. via `core/bootstrap.ensure_seed_records`.
- Every entity shown on dashboards has a matching Django admin model (Pharmacies, Orders, Pharmacy Applications, Prescriptions, Patients, Chat Messages, Payment Providers/Cards, Notifications, Stock Items, Delivery Tasks, Timeline Events, Distributor Status entries).
- Use the dashboard buttons (Approve/Reject/Accept/etc.) for quick status changes, or open `/admin` for full CRUD control. Newly added records via admin appear instantly on the dashboards.

### Authentication & Roles

- **Sign up** on `/signup/` choosing one of: Customer (phone), Doctor/Admin/Distributor (email). New accounts are persisted and visible inside the Django admin (`/admin`) if you created a superuser.
- **Login** on `/` by selecting your role first, then entering your phone (customers) or email (pros) with the password you set. The system enforces that the selected role matches the account's role.
- **Dashboards** (`/dashboard/<role>/`) are protected—users can only access the workspace tied to their profile.

## Project Structure

```
pharmacygo/
├── core/
│   ├── data.py          # Dummy analytics, orders, chats, etc.
│   ├── views.py         # Role-based views and context assembly
│   └── urls.py          # App URL definitions
├── pharmacygo/
│   ├── settings.py      # Template/static configuration
│   └── urls.py          # Project-level routing
├── templates/
│   ├── base.html        # Shared navbar + layout
│   └── core/            # Role-specific pages
├── static/
│   ├── css/style.css    # Design system & components
│   └── js/theme.js      # Dark/light toggle & card theme logic
└── manage.py
```

## Next Steps

- Replace dummy arrays with real database models and Django forms.
- Connect to live pharmacy search and real Google Maps or Mapbox widgets.
- Hook up authentication (Django Allauth or custom) with SMS/email verifications per role.
- Add WebSocket channels for real-time chat and courier tracking.

Enjoy the prototype and iterate as you plug in production services!
