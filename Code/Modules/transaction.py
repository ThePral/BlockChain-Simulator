import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1

class Transaction:
    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.signature = None

    def calculate_hash(self):
        tx_str = f"{self.from_address}{self.to_address}{self.amount}"
        return hashlib.sha256(tx_str.encode()).hexdigest()

    def sign_transaction(self, signing_key):
        if not isinstance(signing_key, SigningKey):
            raise TypeError("sign_transaction expects a SigningKey object")
        
        if signing_key.get_verifying_key().to_string().hex() != self.from_address:
            raise Exception("You cannot sign transactions for other wallets!")

        tx_hash = self.calculate_hash()
        self.signature = signing_key.sign(tx_hash.encode()).hex()

    def is_valid(self):
        if self.from_address == "System":
            return True

        if not self.signature:
            raise Exception("No signature in this transaction")

        try:
            verifying_key = VerifyingKey.from_string(bytes.fromhex(self.from_address), curve=SECP256k1)
            return verifying_key.verify(bytes.fromhex(self.signature), self.calculate_hash().encode())
        except:
            return False
