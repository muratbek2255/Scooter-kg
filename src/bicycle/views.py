import logging

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework import viewsets, permissions
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from src.bicycle.models import (
    Bicycle, RatingBicycleRelation
)
from src.bicycle.serializers import (
    BicyclePublicSerializer, BicycleRelationSerializer
)

logger = logging.getLogger(__name__)


class BicyclePublicViewSet(viewsets.ModelViewSet):
    """View для самокатов"""
    queryset = Bicycle.objects.all()
    serializer_class = BicyclePublicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    permission_classes_by_action = {
        'get': [permissions.IsAuthenticatedOrReadOnly],
        'post': [permissions.IsAdminUser],
        'update': [permissions.IsAdminUser],
        'destroy': [permissions.IsAdminUser],
    }
    lookup_field = 'name_of_lookup_field'

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 60))
    def dispatch(self, *args, **kwargs):
        return super(BicyclePublicViewSet, self).dispatch(*args, **kwargs)


class BicycleRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RatingBicycleRelation.objects.select_related('user').select_related('bicycle').all()
    serializer_class = BicycleRelationSerializer
    lookup_field = 'bicycle'

    def get_object(self):
        bicycle_obj = RatingBicycleRelation.objects.get_or_create(
            user=self.user,
            bicycle_id=self.kwargs['bicycle']
        )
        logger.info('Create rating')
        return bicycle_obj


def index(request):
    return render(request, 'index.html')
