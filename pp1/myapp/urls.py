from django.urls import path,include
from .import views


urlpatterns = [
    path('home/',views.home),
    path('detail/',views.user_detail),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
]
