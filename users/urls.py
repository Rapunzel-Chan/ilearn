from django.urls import path
from django.views.generic import TemplateView

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    # path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("payment/", TemplateView.as_view(template_name="payment.html"), name="payment"),
]