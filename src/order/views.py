from django.contrib.auth import get_user_model
from django.db.models import Sum, F, FloatField
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from src.order.models import Order, OrderItem
from src.order.serializers import OrderSerializer, OrderItemSerializer

User = get_user_model()


class OrderViewSet(viewsets.ModelViewSet):
    """
    View для позволяние просматривать или создавать заказы.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        try:
            purchaser_id = self.request.data['user']
            user = User.objects.get(pk=purchaser_id)
        except Exception as e:
            raise serializers.ValidationError(
                'Пользователь не найден'
            )

        cart = user.carts

        for cart_item in cart.items.all():
            if cart_item.product.quantity - cart_item.quantity < 0:
                raise serializers.ValidationError(
                    'У нас недостаточно запасов ' + str(cart_item.product.title) +
                    'чтобы завершить покупку. Извините, мы скоро пополним запасы'
                )
        order = serializer.save(user=user)

        order_items = []
        for cart_item in cart.items.all():
            order_items.append(OrderItem(order=order, product=cart_item.product, quantity=cart_item.quantity))
            cart_item.product.quantity -= cart_item.quantity
            cart_item.product.save()

        OrderItem.objects.bulk_create(order_items)
        cart.items.clear()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, url_path="order_history/(?P<customer_id>[0-9])")
    def order_history(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)

        except Exception as e:
            return Response({'status': 'fail'})

        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    View для просматривание или редактирование элементы заказа.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
