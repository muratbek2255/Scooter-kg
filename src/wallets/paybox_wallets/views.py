from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import PayboxWallet, Transaction
from .serializers import FundSerializer, WithdrawSerializer, WalletSerializer, TransactionSerializer, PaySerializer


class WalletView(viewsets.ModelViewSet):
    queryset = PayboxWallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated,)


class FundWalletView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FundSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save(owner=request.user)
        transaction.save()
        return Response(data={'response': 'Успешное заполнение'}, status=status.HTTP_200_OK)


class WithdrawWalletView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WithdrawSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save(owner=request.user)
        transaction.save()
        return Response(data={'response': 'Успешный вывод'}, status=status.HTTP_200_OK)


class PayWalletView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(data={'response': 'Successful payment'}, status=status.HTTP_200_OK)


class TransactionsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_wallet = PayboxWallet.objects.get(owner=self.request.user)
        users_transactions = Transaction.objects.filter(
            wallet=user_wallet
        )
        return Transaction.objects.filter(id__in=users_transactions)
