from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet

app_name = UsersConfig.name

router = DefaultRouter()

router.register(r"payments", PaymentViewSet, basename="payment")
urlpatterns = router.urls
