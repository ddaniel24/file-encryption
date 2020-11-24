from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from modules.file import File


class Cryptography:
    def __init__(self, source: File, destination: File):
        """
        Constructor for Cryptography object
        :param source: source file (as File object). For encryption, this is the plain text (unencrypted) file.
        For decryption, this is the encrypted file.
        :param destination: destination file (as File object). For encryption, this is the file which will hold the
        encrypted content. For decryption, this is the plain text (unencrypted) file.
        """
        self.source = source
        self.destination = destination

        """
        A salt value is random data added as an addition to the input of a one-way function.
        Salt values may be personalised, so that multiple users / files do not share the same value.
        For decrypting a file, make sure to always use the same salt as the one used for encryption. Otherwise, the
        passphrases will not match and decryption will fail.
        """
        self.salt = b'salt_value_for_key_generation'

        # This variable stores the encoded key used for encryption / decryption
        self.key = b''

    def set_passphrase(self, passphrase: str):
        """
        Encode the passphrase as bytes and generate the encryption / decryption key. The passphrase is combined with
        the salt value.
        :param passphrase: human-readable passphrase
        """
        # Encode the passphrase to bytes
        passphrase = passphrase.encode()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=self.salt,
                         iterations=50000, backend=default_backend())

        # Encode the key to be used for encryption / decryption
        self.key = base64.urlsafe_b64encode(kdf.derive(passphrase))

    def encrypt(self):
        """
        Encrypt source file using key. Output to destination file (*.enc).
        """

        file_stream = self.source.read_file()

        fernet = Fernet(self.key)
        encrypted_file_stream = fernet.encrypt(file_stream)

        self.destination.write_file(encrypted_file_stream)

    def decrypt(self):
        """
        Decrypt source file (*.enc) using key. Output to destination file.
        :rtype: True if decryption was successful using key. False otherwise.
        """

        file_stream = self.source.read_file()

        fernet = Fernet(self.key)

        try:
            decrypted_file_stream = fernet.decrypt(file_stream)

            self.destination.write_file(decrypted_file_stream)

            return True

        except InvalidToken:
            # Decryption key invalid
            return False
