from datetime import datetime

ADMIN_KPIS = [
    {"label": "Orders today", "value": "1,248", "delta": "+12% vs yesterday"},
    {"label": "Avg. delivery", "value": "24 min", "delta": "-3 min faster"},
    {"label": "Active pharmacies", "value": "86", "delta": "+4 new"},
]

ADMIN_RECENT_ORDERS = [
    {"order_id": "#PG-2148", "customer": "Laylo Karimova", "pharmacy": "PharmaLife Downtown", "status": "Out for delivery", "eta": "12 min"},
    {"order_id": "#PG-2145", "customer": "Aziz Yuldashev", "pharmacy": "CityMeds Park", "status": "Delivered", "eta": "Completed"},
    {"order_id": "#PG-2142", "customer": "Mavluda Rustam", "pharmacy": "UzPharma Green", "status": "Awaiting courier", "eta": "Assign rider"},
    {"order_id": "#PG-2137", "customer": "Sardor Mardan", "pharmacy": "CarePoint Sergeli", "status": "Packed", "eta": "18 min"},
]

ADMIN_USERS = {
    "customers": [
        {"name": "Laylo Karimova", "phone": "+998 90 112 33 44", "orders": 12},
        {"name": "Umid Abdullaev", "phone": "+998 97 223 54 11", "orders": 5},
    ],
    "doctors": [
        {"name": "Dr. Saodat Bek", "email": "saodat@pharmacygo.uz", "patients": 34},
        {"name": "Dr. Kamol Idris", "email": "kamol@pharmacygo.uz", "patients": 21},
    ],
    "distributors": [
        {"name": "Flow Logistics", "email": "ops@flow.uz", "fleet": 18},
        {"name": "MedExpress", "email": "contact@medexpress.uz", "fleet": 11},
    ],
}

PHARMACY_APPROVALS = [
    {"name": "NovaPharm Mirzo", "submitted": "6 min ago", "docs": "License + Tax ID", "status": "Pending"},
    {"name": "HealthHub Sergeli", "submitted": "22 min ago", "docs": "Warehouse permit", "status": "Review"},
]

DOCTOR_PRESCRIPTIONS = [
    {"patient": "Laylo Karimova", "condition": "Seasonal allergy", "requested": "Xyzal 5mg", "status": "Awaiting"},
    {"patient": "Umid Abdullaev", "condition": "Bronchitis", "requested": "Amoxil 500mg", "status": "Approved"},
    {"patient": "Nodira Jura", "condition": "Hypertension", "requested": "Losartan 50mg", "status": "Awaiting"},
]

DOCTOR_CHAT = [
    {"sender": "customer", "name": "Laylo", "time": "09:18", "message": "Doctor, can I take Xyzal twice today?"},
    {"sender": "doctor", "name": "Dr. Saodat", "time": "09:19", "message": "Keep it to one dose every 24 hours."},
    {"sender": "customer", "name": "Laylo", "time": "09:20", "message": "Noted, thank you!"},
]

DOCTOR_PATIENTS = [
    {"name": "Azamat Jalil", "condition": "Diabetes", "contact": "+998 90 119 11 98", "status": "Stable"},
    {"name": "Laylo Karimova", "condition": "Allergy", "contact": "+998 97 005 77 22", "status": "Follow-up"},
    {"name": "Mavluda Rustam", "condition": "Hypertension", "contact": "+998 93 023 43 00", "status": "Pending"},
]

CUSTOMER_PHARMACIES = [
    {"name": "PharmaLife Downtown", "distance": "0.8 km", "rating": 4.9, "pin": {"top": "32%", "left": "48%"}},
    {"name": "UzMed Express", "distance": "1.1 km", "rating": 4.7, "pin": {"top": "55%", "left": "22%"}},
    {"name": "CarePoint Sergeli", "distance": "1.6 km", "rating": 4.8, "pin": {"top": "18%", "left": "72%"}},
]

CUSTOMER_ORDERS = [
    {"order_id": "#PG-2148", "items": "Xyzal 5mg", "status": "Courier assigned", "progress": "In progress"},
    {"order_id": "#PG-2091", "items": "Amoxil 500mg", "status": "Delivered", "progress": "Delivered"},
]

CUSTOMER_PAYMENTS = [
    {"provider": "Uzum", "status": "Connected", "fee": "0% instant"},
    {"provider": "Uzcard", "status": "Connected", "fee": "0.7%"},
    {"provider": "Humo", "status": "Pending", "fee": "0.5%"},
]

CUSTOMER_CARDS = [
    {"id": "wallet-primary", "holder": "Laylo Karimova", "provider": "Uzcard", "ending": "2345", "theme": "ocean", "limit": "25,000,000 UZS"},
    {"id": "wallet-second", "holder": "Laylo Karimova", "provider": "Uzum", "ending": "1121", "theme": "sunrise", "limit": "12,000,000 UZS"},
]

CUSTOMER_NOTIFICATIONS = [
    {"title": "Courier Bekzod is 5 minutes away", "type": "info"},
    {"title": "Prescription approved by Dr. Saodat", "type": "success"},
    {"title": "New promo: 15% off immunity boosters", "type": "warning"},
]

DISTRIBUTOR_STOCK = [
    {"sku": "AMX-500", "name": "Amoxil 500mg", "qty": 320, "status": "Healthy"},
    {"sku": "GLC-20", "name": "Glucophage XR", "qty": 110, "status": "Watch"},
    {"sku": "XYZ-5", "name": "Xyzal 5mg", "qty": 540, "status": "Healthy"},
]

DISTRIBUTOR_TASKS = [
    {"id": "#DL-902", "pharmacy": "PharmaLife Downtown", "eta": "12:40", "status": "Awaiting", "address": "Yunusabad 12"},
    {"id": "#DL-898", "pharmacy": "UzMed Express", "eta": "13:10", "status": "In progress", "address": "Chilanzar 4"},
]

DISTRIBUTOR_TIMELINE = [
    {"label": "Assigned", "time": "09:05"},
    {"label": "Picked up", "time": "09:40"},
    {"label": "In transit", "time": "10:15"},
    {"label": "Delivered", "time": "10:48"},
]

DISTRIBUTOR_STATUS_BOARD = [
    {"order_id": "#PG-2148", "pharmacy": "PharmaLife Downtown", "status": "In progress"},
    {"order_id": "#PG-2145", "pharmacy": "CityMeds Park", "status": "Delivered"},
    {"order_id": "#PG-2139", "pharmacy": "UzMed Express", "status": "Awaiting pickup"},
]

AUTH_ROLES = [
    {"name": "Admin", "description": "Manage platform health & approvals"},
    {"name": "Doctor", "description": "Review prescriptions & chat"},
    {"name": "Customer", "description": "Order medicines & pay securely"},
    {"name": "Distributor", "description": "Deliver and update stock"},
]

CURRENT_YEAR = datetime.now().year
