import requests


class PaymobPaymentService:
    def __init__(self):
        self.PAYMOB_API_KEY = "your_paymob_api_key"
        self.PAYMOB_IFRAME_URL = "https://accept.paymob.com/api/acceptance/iframe"  # noqa
        self.auth_url = "https://accept.paymob.com/api/auth/tokens"
        self.payment_url = "https://accept.paymob.com/api/acceptance/iframe" # noqa
        self.order_url = "https://accept.paymob.com/api/ecommerce/orders"
        self.headers = {"Content-Type": "application/json"}
        self.payload = {"api_key": self.PAYMOB_API_KEY}

    def generate_token(self):
        response = requests.post(self.auth_url, json=self.payload,
                                 headers=self.headers)
        return response.json().get("token")

    def create_paymob_payment(self, currency, amount, user):
        payment_url = f"{self.PAYMOB_IFRAME_URL}/asdasdasdpl';ccxcv"
        return payment_url

        token = self.generate_token()

        # Create an order
        order_payload = {
            "auth_token": token,
            "delivery_needed": False,
            "amount_cents": str(int(amount * 100)),
            "currency": currency,
            "items": [],
        }

        order_response = requests.post(
            self.order_url, json=order_payload, headers=self.headers
        )
        order_id = order_response.json().get("id")

        # Get payment link
        payment_key_payload = {
            "auth_token": token,
            "amount_cents": str(int(amount * 100)),
            "expiration": 3600,
            "order_id": order_id,
            "billing_data": {
                "first_name": user.full_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "country": "EG",
            },
            "currency": currency,
            "integration_id": "your_integration_id",
        }

        payment_key_response = requests.post(
            self.payment_url, json=payment_key_payload, headers=self.headers
        )
        payment_token = payment_key_response.json().get("token")

        payment_url = f"{self.PAYMOB_IFRAME_URL}/{payment_token}"
        return payment_url
