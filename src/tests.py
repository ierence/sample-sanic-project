from random import randint

from sanic_testing import TestManager

from main import app
from utils.webhook_signature import generate_signature

mgr = TestManager(app)


def test_webhook(mgr: TestManager):
    user_id = 17922994
    bill_id = 47086591
    transaction_id = randint(100000000, 999999999)
    amount = 40
    signature = generate_signature(
        transaction_id, user_id, bill_id, amount
    )

    json = {
        "user_id": user_id,
        "bill_id": bill_id,
        "transaction_id": transaction_id,
        "amount": amount,
        "signature": signature
    }

    request, response = mgr.test_client.post('/payment/webhook', json=json)

    return (request, response)


result = test_webhook(mgr)
print(result)
