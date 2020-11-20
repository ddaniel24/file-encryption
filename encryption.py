from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from file import File


class Cryptography:
    def __init__(self, source: File, destination: File):
        self.source = source
        self.destination = destination
        # A salt value is a random data added as an addition to the input of a one-way function.
        # Salt values may be personalised, so that multiple users / files do not share the same value.
        # For decrypting a file, make sure to always use the same salt as the one used for encryption.
        # Otherwise, the passphrases will not match and decryption will fail.
        self.salt = b'salt_value_for_key_generation'
        # This stores the key used for encryption / decryption
        self.key = b''

    def set_passphrase(self, passphrase: str):
        # Encode the passphrase to bytes
        passphrase = passphrase.encode()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=self.salt,
                         iterations=50000, backend=default_backend())

        # Encode the key to be used for encryption / decryption
        self.key = base64.urlsafe_b64encode(kdf.derive(passphrase))

    def encrypt(self):
        # Get file contents (the one which we want to encrypt)
        file_stream = self.source.read_file()

        # Encrypt file using key
        fernet = Fernet(self.key)
        encrypted_file_stream = fernet.encrypt(file_stream)

        # Write encrypted bytes to output file
        self.destination.write_file(encrypted_file_stream)

    def decrypt(self):
        # Get file contents (the one which we want to decrypt)
        file_stream = self.source.read_file()

        # Decrypt using key
        fernet = Fernet(self.key)

        try:
            decrypted_file_stream = fernet.decrypt(file_stream)

            # Write decrypted stream to file
            self.destination.write_file(decrypted_file_stream)

            return True

        except InvalidToken as e:
            # Decryption key invalid
            return False

