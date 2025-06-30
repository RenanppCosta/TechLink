from django.urls import path
from pagamentos.views import (
    CheckoutView,
    create_payment,
    abacate_pay_webhook
)
from pagamentos.views.create_preference_view import payment_success_view

app_name = 'pagamentos'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='pagamentos'),
    path("create-payment-intent/", create_payment, name="create_payment"),
     path("sucesso/", payment_success_view, name="payment_success"),
    path("/webhook/abacatepay/", abacate_pay_webhook, name="abacate_pay_webhook")
]

