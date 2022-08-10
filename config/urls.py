from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from src.user.views import auth
from src.bicycle.views import index

from config.yasg import urlpatterns as doc_urls


router = DefaultRouter()


urlpatterns = [
    # admin urls
    path(r'^jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),

    # rest_api urls and token urls
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # for through social network auth
    # path('', include('social_django.urls', namespace='social')),
    # path('auth/', auth),
    # path('index', index),
    # path('accounts/', include('allauth.urls')),
    # for payments
    path('api/v1/payments/', include('src.payments.stripe_payment.urls')),
    # for push notification
    path('api/v1/push/', include('src.notification.urls')),
    # django model translation
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += doc_urls

urlpatterns += i18n_patterns(
    path('pages/', include('django.contrib.flatpages.urls')),
    # user and auth urls
    path('api/v1/', include('src.user.urls')),
    # scooter urls
    path('api/v2/', include('src.scooter.urls')),
    # bicycle urls
    path('api/v3/', include('src.bicycle.urls'))
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
