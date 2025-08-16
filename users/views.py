from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import Payment, User
from users.serializers import PaymentCreateSerializer, UserPrivateSerializer, UserPublicSerializer, UserSerializer
from users.services import convert_rub_to_usd, create_stripe_price, create_stripe_session

# Create your views here.


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="create")
    def create_payment(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save(user=request.user)

        sum_of_payment_in_usd = convert_rub_to_usd(payment.sum_of_payment)
        price = create_stripe_price(sum_of_payment_in_usd)
        session_id, payment_link = create_stripe_session(price.id)

        payment.session_id = session_id
        payment.link = payment_link
        payment.price_id = price.id
        payment.save()

        return Response(
            {
                "id": payment.id,
                "course": payment.course.id,
                "lesson": payment.lesson.id,
                "sum_of_payment": payment.sum_of_payment,
                "payment_type": payment.payment_type,
                "link": payment.link,
            }
        )


# class PaymentCreateAPIView(CreateAPIView):
#     serializer_class = PaymentCreateSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Payment.objects.all()
#
#     def perform_create(self, serializer):
#         payment = serializer.save(user=self.request.user)
#         sum_of_payment_in_usd = convert_rub_to_usd(payment.sum_of_payment)
#         price = create_stripe_price(sum_of_payment_in_usd)
#         session_id, payment_link = create_stripe_session(price.id)
#         payment.session_id = session_id
#         payment.link = payment_link
#         payment.price_id = price.id
#         payment.save()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [
        AllowAny,
    ]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserProfileAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.pk == self.get_object().pk:
            return UserPrivateSerializer
        return UserPublicSerializer

    def get_queryset(self):
        return User.objects.all()
