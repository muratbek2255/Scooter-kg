from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from src.cart.models import Cart, CartItem
from src.cart.serializers import CartSerializer, CartItemSerializer
from src.scooter.models import Scooter


class CartViewSet(viewsets.ModelViewSet):
    """
    Просматривание или редактирование тележки.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    @action(detail=True, methods=['post', 'put'])
    def add_to_cart(self, request, pk=None):
        cart = self.get_object()
        try:
            product = Scooter.objects.get(
                pk=request.data['scooter_id']
            )
            quantity = int(request.data['quantity'])
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})

        if product.available_inventory <= 0 or product.available_inventory - quantity < 0:
            print("There is no more product available")
            return Response({'status': 'fail'})

        existing_cart_item = CartItem.objects.filter(product=product).first()

        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            new_cart_item = CartItem(product=product, quantity=quantity)
            new_cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'put'])
    def remove_from_cart(self, request, pk=None):

        cart = self.get_object()
        try:
            product = Scooter.objects.get(
                pk=request.data['product_id']
            )
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})

        try:
            cart_item = CartItem.objects.get(product=product)
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})

        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    Для просматривания и редактирования корзины
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
