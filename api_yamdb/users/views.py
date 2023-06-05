from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import AdminOnly

from users.models import CustomUser

from .serializers import (CustomUserSerializer, SignUpSerializer,
                          TokenSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """
    Работает над всеми операциями с пользователями от лица админа.
    Позволяет обычному пользователю редактировать свой профиль.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AdminOnly,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    http_method_names = ["get", "post", "delete", "patch"]

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = get_object_or_404(CustomUser, username=self.request.user)
        if request.method == 'GET':
            serializer = CustomUserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_create(self, serializer):
        serializer.save()


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signup(request):
    try:
        user = CustomUser.objects.get(
            username=request.data['username'],
            email=request.data['email']
        )
        serializer = SignUpSerializer(user, data=request.data)
    except Exception:
        serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        CustomUser,
        username=serializer.validated_data["username"],
        email=serializer.validated_data["email"]
    )
    code = str(randint(100000, 999999))
    serializer.save(confirmation_code=code)
    send_mail(
        'Код для вашей регистрации',
        f'Код: {code}',
        settings.DEFAULT_MAIL,
        [user.email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


class GetToken(APIView):
    """
    Осуществляет выдачу зарегистрированному пользователю.
    Обновляет истекший токен.
    """
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ndata = serializer.validated_data
        user = get_object_or_404(CustomUser, username=ndata['username'])
        if ndata['confirmation_code'] == user.confirmation_code:
            refresh = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(refresh)},
                status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Неверный код'},
            status=status.HTTP_400_BAD_REQUEST
        )
