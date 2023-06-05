from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from .permissions import (
    IsAuthorModeratorAdminOrReadOnlyPermission, IsAdminUserOrReadOnly,
    IsAdminOrReadOnlyPermission)
from .serializers import (ReviewSerializer, CommentSerializer,
                          GenreSerializer, CategorySerializer,
                          TitleSerializerGet, TitleSerializerPost)
from reviews.models import Title, Review, Category, Genre
from .filters import TitleFilter
from .mixins import ListPostDeleteViewSet


class CategoryViewSet(ListPostDeleteViewSet):
    """Реализует методы GET, POST, DEL для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission, )
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListPostDeleteViewSet):
    """Реализует методы GET, POST, DEL для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission, )
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """Работает над всеми операциями с произведениями."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializerGet
        return TitleSerializerPost


class ReviewViewSet(ModelViewSet):
    """Работает над всеми операциями с отзывам."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnlyPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """Работает над всеми операциями с комментариями к отзывам."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnlyPermission,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        title_id = int(self.kwargs.get('title_id'))
        if title_id == review.title_id:
            return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        title_id = int(self.kwargs.get('title_id'))
        if title_id == review.title_id:
            serializer.save(author=self.request.user, review=review)
