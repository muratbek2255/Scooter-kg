from django.urls import path

from src.payment import views

urlpatterns = [
    path('payments/stripe', views.InitiateStripePayment.as_view()),
    path('payments/stripe/<payment_intent_id>', views.ConfirmStripePayment.as_view()),
]
