import requests
import json
from config import settings


class PaymobPaymentService:
    def __init__(self, currency="SAR"):
        self.PAYMOB_API_KEY = ""
        self.PAYMOB_IFRAME_URL = (
            "https://ksa.paymob.com/unifiedcheckout/?publicKey={}&clientSecret={}"
        )
        self.headers = {"Content-Type": "application/json"}
        self.intention_url = "https://ksa.paymob.com/v1/intention/"
        self.public_key = settings.PAYMOB_PUBLIC_KEY
        self.private_key = settings.PAYMOB_PRIVATE_KEY
        self.payment_methods = [9395]
        self.currency = currency


    def get_iframe_url(self, client_secret):
        return self.PAYMOB_IFRAME_URL.format(self.public_key, client_secret)

    def create_paymob_intention(
        self,
        customer=None,
        amount=None,
        course=None,
        reference_id=None,
        transaction=None,
    ):
        payload = json.dumps(
            {
                "amount": amount,
                "currency": self.currency,
                "payment_methods": self.payment_methods,
                "items": [
                    {
                        "name": course.name,
                        "amount": amount,
                        "description": course.description,
                        "quantity": 1,
                    }
                ],
                "billing_data": {
                    "apartment": "6",
                    "first_name": "Ammar",
                    "last_name": "Sadek",
                    "street": "938, Al-Jadeed Bldg",
                    "building": "939",
                    "phone_number": "+96824480228",
                    "country": "KSA",
                    "email": "AmmarSadek@gmail.com",
                    "floor": "1",
                    "state": "Alkhuwair",
                },
                "customer": {
                    "first_name": "Ammar",
                    "last_name": "Sadek",
                    "email": "AmmarSadek@gmail.com",
                    "extras": {"re": "22"},
                },
                "extras": {"ee": 22},
                "special_reference": f"transaction_id:{reference_id}",
                "notification_url": f"{settings.PAYMOB_CALLBACK_URL}/payments/paymob/callback/",
                "redirection_url": f"https://baronlearning.com/course-content/{course.id}",
            }
        )
        headers = {
            "Authorization": f"Token {self.private_key}",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", self.intention_url, headers=headers, data=payload
        )
        if response.status_code != 201:
            return response.status_code, None
        client_secret = response.json().get("client_secret")
        transaction.client_secret = client_secret
        transaction.save()
        return response.status_code, self.get_iframe_url(client_secret)
