from ecdsa import SigningKey, SECP256k1
from Modules.transaction import Transaction

class Wallet:
    def __init__(self, private_key=None):
        if private_key:
            self.private_key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        else:
            self.private_key = SigningKey.generate(curve=SECP256k1)

        self.public_key = self.private_key.get_verifying_key()

    def get_private_key_hex(self):
        return self.private_key.to_string().hex()

    def get_public_key_hex(self):
        return self.public_key.to_string().hex()

    def create_signed_transaction(self, to_address, amount):
        tx = Transaction(
            from_address=self.get_public_key_hex(),
            to_address=to_address,
            amount=amount
        )
        tx.sign_transaction(self.private_key)
        return tx
