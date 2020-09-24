# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors.utils import encryption
from tamcolors.tests.test_utils import slow_test


@unittest.skipIf(encryption.CRYPTOGRAPHY_PRESENT, "Has encryption modules")
class NoEncryptionTests(unittest.TestCase):
    def test_init(self):
        self.assertRaises(encryption.EncryptionError, encryption.Encryption)


@unittest.skipIf(not encryption.CRYPTOGRAPHY_PRESENT, "Missing encryption modules!")
class EncryptionTests(unittest.TestCase):
    @slow_test
    def test_init(self):
        self.assertIsInstance(encryption.Encryption(), encryption.Encryption)

    @slow_test
    def test_simple_encrypt_decrypt(self):
        msg = b"This is a test"
        e = encryption.Encryption()
        e_msg = e.encrypt(msg)
        self.assertNotEqual(msg, e_msg)
        self.assertEqual(e.decrypt(e_msg), msg)

    @slow_test
    def test_encrypt_decrypt(self):
        msgs = (b"This is a test",
                b"more random data",
                bytes(1000),
                bytes([(i*2) % 256 for i in range(300)]))

        e1 = encryption.Encryption()
        e2 = encryption.Encryption()
        e1_public_key = e1.get_raw_public_key()

        e_msgs = []
        for msg in msgs:
            e_msg = e2.encrypt_with_public_key(e1_public_key, msg)
            self.assertNotEqual(e_msg, msg)
            e_msgs.append(e_msg)

        for e_msg, right_msg in zip(e_msgs, msgs):
            msg = e1.decrypt(e_msg)
            self.assertEqual(msg, right_msg)

    @slow_test
    def test_build_setting(self):
        for rsa_key_size in (4098, 5000):
            for aes_key_size in (128, 192):
                for nonce_key_size in (12, 32):
                    for authenticator in (bytes([1, 2, 3]), b"authenticator"):
                        for max_random in (15, 1000):
                            msg = b"This is a test"
                            e = encryption.Encryption(rsa_key_size=rsa_key_size,
                                                      aes_key_size=aes_key_size,
                                                      nonce_key_size=nonce_key_size,
                                                      authenticator=authenticator,
                                                      max_random=max_random)
                            e_msg = e.encrypt(msg)
                            self.assertNotEqual(msg, e_msg)
                            self.assertEqual(e.decrypt(e_msg), msg)
