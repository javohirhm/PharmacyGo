from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/orders/<int:pk>/<str:action>/', views.order_action, name='order_action'),
    path('dashboard/admin/applications/<int:pk>/<str:action>/', views.application_action, name='application_action'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/doctor/prescriptions/<int:pk>/<str:action>/', views.prescription_action, name='prescription_action'),
    path('dashboard/doctor/chat/', views.doctor_chat_message, name='doctor_chat_message'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard/customer/orders/create/', views.create_customer_order, name='create_customer_order'),
    path('dashboard/distributor/', views.distributor_dashboard, name='distributor_dashboard'),
    path('dashboard/distributor/tasks/<int:pk>/<str:action>/', views.delivery_task_action, name='delivery_task_action'),
    path('dashboard/distributor/status/<int:pk>/complete/', views.distributor_status_action, name='distributor_status_action'),
]
