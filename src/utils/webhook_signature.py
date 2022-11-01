from configuration import CONFIG
from Crypto.Hash import SHA1


def generate_signature(transaction_id, user_id, bill_id, amount):
    signature = SHA1.new(
        f'{CONFIG["WEBHOOK_SECRET"]}:{transaction_id}:{user_id}:{bill_id}:{amount}'.encode()
    ).hexdigest()
    return signature
