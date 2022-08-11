from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path('fund/', views.FundWalletView.as_view(), name='fund'),
    path('withdraw/', views.WithdrawWalletView.as_view(), name='withdraw'),
    path('pay/', views.PayWalletView.as_view(), name='pay'),
    path('transactions/', views.TransactionsView.as_view(), name='details')
]

router = DefaultRouter()
router.register(r'wallets', views.WalletView)

urlpatterns += router.urls
