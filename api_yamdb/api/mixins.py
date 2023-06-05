from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ListPostDeleteViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, GenericViewSet
):
    pass
