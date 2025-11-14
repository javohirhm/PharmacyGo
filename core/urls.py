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
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard/customer/orders/create/', views.create_customer_order, name='create_customer_order'),
    path('dashboard/customer/pharmacies/<int:pk>/', views.pharmacy_detail, name='pharmacy_detail'),
    path('dashboard/pharmacy-store/', views.pharmacy_store_dashboard, name='pharmacy_store_dashboard'),
    path('dashboard/distributor/', views.distributor_dashboard, name='distributor_dashboard'),
    path('dashboard/distributor/tasks/<int:pk>/<str:action>/', views.delivery_task_action, name='delivery_task_action'),
    path('dashboard/distributor/status/<int:pk>/complete/', views.distributor_status_action, name='distributor_status_action'),
    path('dashboard/distributor/status/<int:pk>/update/', views.distributor_status_update, name='distributor_status_update'),
    path('dashboard/distributor/deliveries/<int:pk>/', views.delivery_detail, name='delivery_detail'),
]
