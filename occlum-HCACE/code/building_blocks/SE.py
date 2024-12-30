from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.toolbox.symcrypto import MessageAuthenticator
from charm.toolbox.pairinggroup import PairingGroup
from charm.core.math.integer import randomBits
import hashlib

class SE:
    def __init__(self, key=None):
        self.key = None
        if key is None:
            self.key = hashlib.sha256(str(randomBits(128)).encode()).digest()
        else:
            self.key = hashlib.sha256(str(key).encode()).digest()

        self.crypto = SymmetricCryptoAbstraction(self.key)

    def encrypt(self, plaintext):
        return self.crypto.encrypt(plaintext)

    def decrypt(self, ciphertext):
        return self.crypto.decrypt(ciphertext)


if __name__ == "__main__":
    se = SE()

    plaintext = "Hello, this is a secret message!"

    ciphertext = se.encrypt(plaintext)
    print(f"Ciphertext: {ciphertext}")

    decrypted_message = se.decrypt(ciphertext)
    print(f"Decrypted Message: {decrypted_message.decode('utf-8')}")
