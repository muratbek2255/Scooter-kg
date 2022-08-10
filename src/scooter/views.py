import logging

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets, permissions
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from src.scooter.models import (
    Scooter, RatingScooterRelation
)
from src.scooter.serializers import (
    ScooterPublicSerializer, ScooterRelationSerializer
)

logger = logging.getLogger(__name__)


class ScooterPublicViewSet(viewsets.ModelViewSet):
    """View для самокатов"""
    queryset = Scooter.objects.all()
    serializer_class = ScooterPublicSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    permission_classes_by_action = {
        'get': [permissions.IsAuthenticated],
        'post': [permissions.IsAdminUser],
        'update': [permissions.IsAdminUser],
        'destroy': [permissions.IsAdminUser],
    }
    lookup_field = 'name_of_lookup_field'

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 60))
    def dispatch(self, *args, **kwargs):
        return super(ScooterPublicViewSet, self).dispatch(*args, **kwargs)


class BicycleRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RatingScooterRelation.objects.select_related('user').\
        select_related('scooter').all()
    serializer_class = ScooterRelationSerializer
    lookup_field = 'scooter'

    def get_object(self):
        scooter_obj = RatingScooterRelation.objects.get_or_create(
            user=self.user,
            scooter_id=self.kwargs['scooter']
        )
        logger.info('Create rating')
        return scooter_obj
