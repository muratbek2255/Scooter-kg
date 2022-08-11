import json
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views, status, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from src.order.models import OrderItem, Order
from src.order.serializers import OrderDetailsSerializer
from src.payment.backends import WalletController
from src.payment.models import PaymentModel
from src.payment.serializers import PaymentSerializer, StripePaymentIntentConfirmSerializer
from src.wallets.stripe_wallets.models import Transaction
from src.wallets.stripe_wallets.tasks import send_order_info

stripe.api_key = settings.STRIPE_SECRET_KEY

User = get_user_model()


def update_products_quantity(cart, payment, payment_intent_id, *args, **kwargs):
    for item in cart.items.all():
        try:
            product = item.product
            product.quantity = product.quantity - item.quantity
            product.save()
            wallet = WalletController().get(product.created_by)
            user = User.objects.get(id=kwargs['pk'])
            Transaction.objects.create(wallet=wallet,
                                       email=user.email,
                                       type='payment_fill',
                                       value=Decimal('value'))
            send_order_info.delay(email=user.email, message='Transaction confirm')
        except Exception as e:
            print(str(e))
            pass


class InitiateStripePayment(generics.GenericAPIView):

    serializer_class = PaymentSerializer

    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        user = request.user
        payload = request.data
        serializer = PaymentSerializer(data=payload)
        serializer.is_valid(raise_exception=True)

        try:
            customer = stripe.Customer.create(
                name=user.username,
                email=user.email
            )
            intent = stripe.PaymentIntent.create(
                payment_method_types=[payload['method']],
                amount=payload['amount'] * 100,
                currency=payload['currency'],
                customer=customer.id,
                metadata={
                    "order_number": payload['order_number']
                },
                receipt_email=user.email
            )
            serializer.save()
            response = {
                'data': {
                    'token': intent['client_secret'],
                    'public_key': settings.STRIPE_PUBLISHABLE_KEY,
                    'payment': serializer.data
                },
                'status': status.HTTP_200_OK
            }
        except Exception as e:
            response = {
                'data': {
                    'error': str(e)
                },
                'status': status.HTTP_403_FORBIDDEN
            }
        return JsonResponse(response['data'], status=response['status'], safe=False)


class ConfirmStripePayment(generics.RetrieveUpdateAPIView):
    def updateOrderItemStatus(self, order, status, payment_intent_id):
        items = OrderItem.objects.filter(order=order)
        for item in items:
            item.payment_intent_id = payment_intent_id
            item.status = status
            item.save()

    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def update(self, request, payment_intent_id):
        user = request.user
        payload = json.loads(request.body)
        serializer = StripePaymentIntentConfirmSerializer(data=payload)
        serializer.is_valid(raise_exception=True)

        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            response = {
                'body': {
                    'error': 'Intent not valid or Order number not valid'
                },
                'status': status.HTTP_400_BAD_REQUEST
            }

            if intent['status'] == 'succeeded' and intent['metadata']['order_number'] == payload['order_number']:
                try:
                    order = Order.objects.get(number=payload['order_number'], user=user)
                    payment = PaymentModel.objects.get(order_number=payload['order_number'])
                    order.status = Order.CONFIRMED
                    order.save()
                    payment.status = PaymentModel.DONE
                    payment.save()
                    send_order_info.delay(email=user.email, message='Transaction confirm')
                    update_products_quantity(order.cart, payment, payment_intent_id)
                    self.updateOrderItemStatus(order, Order.CONFIRMED, payment_intent_id)
                    response['body'] = OrderDetailsSerializer(order).data
                    response['status'] = status.HTTP_200_OK
                except ObjectDoesNotExist:
                    response['body']['error'] = 'Order or payment not founded'
                    response['status'] = status.HTTP_400_BAD_REQUEST

        except Exception as e:
            response = {
                'body': {
                    'error': str(e)
                },
                'status': status.HTTP_403_FORBIDDEN
            }
        return JsonResponse(response['body'], status=response['status'], safe=False)
