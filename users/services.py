import stripe
from forex_python.converter import CurrencyRates

from config.settings import APP_DOMAIN, STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_usd(sum_of_payment):
    """Конвертирует рубли в доллары"""

    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    sum_of_payment = float(sum_of_payment)
    return int(sum_of_payment * rate)


def create_stripe_price(sum_of_payment):
    """Создает стоимость в Stripe"""

    return stripe.Price.create(
        currency="usd",
        unit_amount=int(sum_of_payment * 100),
        product_data={"name": "Payment"},
    )


def create_stripe_session(price):
    """Создает сессию и формирует ссылку на оплату"""
    session = stripe.checkout.Session.create(
        success_url=f"{APP_DOMAIN}/success/",
        cancel_url=f"{APP_DOMAIN}/cancel/",
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
