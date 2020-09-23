# built in libraries
import os
import random
import hashlib
import math


# 3rd party libraries
try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.ciphers import aead
    CRYPTOGRAPHY_PRESENT = True
except:
    CRYPTOGRAPHY_PRESENT = False


"""
Encryption
Encrypts and decrypts bytes using RSA and AES.
RSA Encrypted: [AES key][nonce][sandy check key]
AES Encrypted" [random header][random bytes][data]
SHA3512 makes the sandy check key
"""

MISSING_ENCRYPTION = "Missing Encryption Libraries!\nYou can fix this by running \"pip install tamcolors[encryption]\""


class EncryptionError(Exception):
    pass


class Encryption:
    def __init__(self,
                 rsa_key_size=4096,
                 aes_key_size=256,
                 nonce_key_size=64,
                 authenticator=bytes(),
                 max_random=20):
        """
        info: Makes a Encryption Object. This encrypts bytes using RSA and AES.
        Encrypted data example.
        RSA Encrypted: [AES key][nonce][sandy check key]
        AES Encrypted" [random header][random bytes][data]
        :param rsa_key_size: int: 4096 - inf
        :param aes_key_size: int: 128, 192 or 256
        :param nonce_key_size: int: 12 - inf: A key for AES encryption.
        :param authenticator: bytes: Checks if
        :param max_random: int: 2 - inf: Sets the max number of random bytes that get add it to encryption.
        """

        if not CRYPTOGRAPHY_PRESENT:
            raise EncryptionError(MISSING_ENCRYPTION)

        # generate new private key
        self._private_key = rsa.generate_private_key(public_exponent=65537,
                                                     key_size=rsa_key_size,
                                                     backend=default_backend())
        self._public_key = self._private_key.public_key()

        # aes key sizes
        self._aes_key_size = aes_key_size
        self._nonce_key_size = nonce_key_size

        # authenticator
        self._authenticator = authenticator

        # random bytes
        self._random = random.SystemRandom()
        self._max_random = max_random
        self._random_header_size = math.ceil(math.ceil(math.log(self._max_random, 2) + 1) / 8)

        # rsa hash size
        self._rsa_block_size = len(self._public_key.encrypt(bytes(),
                                                            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                         algorithm=hashes.SHA256(),
                                                                         label=None)))
        # sha hash size
        self._sha_block_size = len(self.make_sandy_check_key(bytes()))

    def encrypt(self, data):
        """
        info: Encrypts data.
        :param data: bytes
        :return: bytes: Encrypted data.
        """
        return self.encrypt_with_public_key(self.get_raw_public_key(), data)

    def decrypt(self, data):
        """
        info: Decrypt message. The data will also be checked for corruption.
        :param data: bytes
        :return: bytes: Unencrypted data.
        """

        try:
            # decrypt rsa block
            rsa_block = self._private_key.decrypt(data[:self._rsa_block_size],
                                                  padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                               algorithm=hashes.SHA256(),
                                                               label=None))

            # get aes key
            aes_raw_key = rsa_block[:-(self._nonce_key_size + self._sha_block_size)]
            # get nonce
            nonce = rsa_block[-(self._nonce_key_size + self._sha_block_size):-self._sha_block_size]
            # get sandy check key
            sandy_check_key = rsa_block[-self._sha_block_size:]
            # make aes decrypter
            aes_key = aead.AESGCM(aes_raw_key)

            # get aes encrypted data
            data = data[self._rsa_block_size:]

            # get unencrypted ase data
            data = aes_key.decrypt(nonce, data, self._authenticator)

            # sandy check data
            if not Encryption.check_sandy_check_key(sandy_check_key, data):
                raise EncryptionError("Sandy Check Failed")

            # remove random bytes
            random_data_size = int.from_bytes(data[:self._random_header_size], byteorder="big", signed=False)

            return data[random_data_size + self._random_header_size:]

        except Exception as e:
            raise EncryptionError("Cant decrypt: {0}".format(e))

    def get_raw_private_key(self):
        """
        info: Gets the raw private key.
        :return: bytes: PEM encoding
        """

        return self._private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                               format=serialization.PrivateFormat.PKCS8,
                                               encryption_algorithm=serialization.NoEncryption())

    def get_raw_public_key(self):
        """
        info: gets the raw public key.
        :return: bytes: PEM encoding
        """

        return self._public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                             format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def encrypt_with_public_key(self, key, data):
        """
        info: Encrypts data with public key.
        :param key: bytes or ras key object
        :param data: bytes
        :return: bytes: encrypted data
        """

        if not isinstance(key, bytes):
            public_key = key
        else:
            public_key = serialization.load_pem_public_key(key, backend=default_backend())

        # setup aes
        aes_raw_key = aead.AESGCM.generate_key(bit_length=self._aes_key_size)
        aes_key = aead.AESGCM(aes_raw_key)
        nonce = os.urandom(self._nonce_key_size)

        # get random data size
        random_data_size = self._random.randint(0, self._max_random)
        raw_random_data_size = random_data_size.to_bytes(length=self._random_header_size,
                                                         byteorder="big",
                                                         signed=False)

        # AES encrypt data [random header][random data][data]
        data = raw_random_data_size + os.urandom(random_data_size) + data
        encrypted_data = aes_key.encrypt(nonce, data, self._authenticator)

        # RSA encrypt [AES key][nonce][sandy check key]
        rsa_header = aes_raw_key + nonce + Encryption.make_sandy_check_key(data)
        encrypted_rsa_header = public_key.encrypt(rsa_header, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                           algorithm=hashes.SHA256(),
                                                                           label=None))

        return encrypted_rsa_header + encrypted_data

    @staticmethod
    def make_sandy_check_key(data):
        """
        info: Hashes data.
        :param data: bytes
        :return: bytes: Hash key.
        """

        return hashlib.sha3_512(data).digest()

    @staticmethod
    def check_sandy_check_key(sandy_key, data):
        """
        info: Checks if the sandy key is equal to the data key.
        :param sandy_key: bytes: sha hash key
        :param data: bytes:
        :return: bool
        """

        return sandy_key == Encryption.make_sandy_check_key(data)
