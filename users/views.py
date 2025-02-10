from drf_spectacular.utils import extend_schema
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from shop.models import Product
from users.models import User, Purchases
from users.permissions import IsOwner
from users.serializers import UserCreateSerializer, PurchasesSerializer, PurchasesAllSerializer


class LoginAPIView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(username=request.data['username'])
            user.save()
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


@extend_schema(
    summary="Добавление, удаление или обновление колличества товаров в корзине",
    request=PurchasesSerializer,
    responses={
        200: {"message": "колличество изменено, текущее колличество {quantity}"},
        201: {"message": "продукт: {product_name} добавлен в колличестве: {quantity}"},
        202: {"message": "продукт удален"},
        400: {"message": "Отсутствует обязательное поле (product/quantity)"},
        403: {"message": "Количество должно быть больше ноля"},
    }
)
class PurchasesCreateOrDeliteOrUpdateAPIView(generics.CreateAPIView):
    serializer_class = PurchasesSerializer
    queryset = Purchases.objects.all()
    permission_classes = [IsOwner]

    def post(self, request, *args, **kwargs):
        serializer = PurchasesSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        owner = request.user
        if request.data.get('product') is None:
            return Response({"message": "Отсутствует обязательное поле product"}, status.HTTP_400_BAD_REQUEST)
        elif request.data.get('quantity') is None:
            return Response({"message": "Отсутствует обязательное поле quantity"}, status.HTTP_400_BAD_REQUEST)
        elif int(request.data.get('quantity')) < 0:
            return Response({"message": "Количество должно быть больше ноля"}, status.HTTP_403_FORBIDDEN)
        else:
            product_slug = request.data['product']
            quantity = request.data['quantity']
            product_item = get_object_or_404(Product, slug=product_slug)
            purchases_items = Purchases.objects.filter(owner=owner, product=product_item)
            if purchases_items.exists():
                purchases_item = purchases_items[0]
                if quantity == 0:
                    purchases_item.delete()
                    message = 'продукт удален'
                    return Response({"message": 'продукт удален'},
                                    status.HTTP_202_ACCEPTED)
                else:
                    purchases_item.quantity = quantity
                    purchases_item.save()
                    return Response({"message": f'колличество изменено, текущее колличество {quantity}'},
                                    status.HTTP_200_OK)
            else:
                purchases_item = Purchases(owner=owner, product=product_item, quantity=quantity)
                purchases_item.save()
                return Response({"message": f'продукт: {product_item.name} добавлен в колличестве: {quantity}'},
                                status.HTTP_201_CREATED)


class PurchasesListAPIView(generics.ListAPIView):
    serializer_class = PurchasesAllSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)


@extend_schema(
    summary="Удаление корзины целиком",
    responses={
        200: {"message": "Корзина удалена"},
        400: {"message": "У пользователя отсутствуют продукты в корзине"},
    }
)
@api_view(['GET'])
@permission_classes([IsOwner])
def delete_all_purchases(request):
    """Удаление корзины целиком"""
    if request.method == 'GET':
        user = request.user
        purchases_list = Purchases.objects.filter(owner=user)
        if purchases_list.exists():
            purchases_list.delete()
            message = "Корзина удалена"
            status_http = status.HTTP_200_OK
        else:
            message = "У пользователя отсутствуют продукты в корзине"
            status_http = status.HTTP_400_BAD_REQUEST
        return Response({"message": message}, status=status_http)
