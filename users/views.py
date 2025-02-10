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


class PurchasesCreateOrDeliteOrUpdateAPIView(generics.CreateAPIView):
    serializer_class = PurchasesSerializer
    queryset = Purchases.objects.all()
    permission_classes = [IsOwner]

    def post(self, request, *args, **kwargs):
        owner = request.user
        if request.data.get('product') is None:
            return Response({"message": "Отсутствует обязательное поле product"}, status.HTTP_400_BAD_REQUEST)
        elif request.data.get('quantity') is None:
            return Response({"message": "Отсутствует обязательное поле quantity"}, status.HTTP_400_BAD_REQUEST)
        else:
            product_slug = request.data['product']
            quantity = request.data['quantity']
            product_item = get_object_or_404(Product, slug=product_slug)
            purchases_item = Purchases.objects.filter(owner=owner, product=product_item)
            if purchases_item.exists():
                if quantity == 0:
                    purchases_item[0].delete()
                    message = 'продукт удален'
                else:
                    purchases_item[0].quantity = quantity
                    purchases_item[0].save()
                    message = f'колличество изменено, текущее колличество {quantity}'
            else:
                purchases_item = Purchases(owner=owner, product=product_item, quantity=quantity)
                purchases_item.save()
                message = f'продукт: {product_item.name} добавлен в колличестве: {quantity}'

            return Response({"message": message}, status.HTTP_200_OK)


class PurchasesListAPIView(generics.ListAPIView):
    serializer_class = PurchasesAllSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)


@api_view(['POST'])
@permission_classes([IsOwner])
def delete_all_purchases(request):
    """Удаление корзины целиком"""
    if request.method == 'POST':
        user = request.user
        purchases_list = Purchases.objects.filter(owner=user)
        if purchases_list.exists():
            purchases_list.delete()
            message = "Корзина удалена"
        else:
            message = "У пользователя отсутвуют продукты в корзине"
        return Response({"message": message}, status=status.HTTP_200_OK)
