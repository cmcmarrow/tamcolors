# built in libraries
import unittest.mock
from tempfile import TemporaryDirectory
from os.path import join


# tamcolors libraries
from tamcolors.utils import identifier


class IdentifierTests(unittest.TestCase):
    def test_globals(self):
        self.assertIsInstance(identifier.IDENTIFIER_FILE_NAME, str)
        self.assertIsInstance(identifier.IDENTIFIER_SIZE, int)

    def test_generate_identifier(self):
        with TemporaryDirectory() as tmp_dir_name:
            tmp_name = join(tmp_dir_name, "temp.id")
            self.assertIsInstance(identifier.generate_identifier_bytes(tmp_name), bytes)
            self.assertIsInstance(identifier.generate_identifier_bytes(tmp_name), bytes)
            self.assertIsInstance(identifier.generate_identifier_bytes(tmp_name, 1000), bytes)
            self.assertIsInstance(identifier.generate_identifier_bytes(tmp_name, 9999), bytes)

    def test_get_identifier_bytes(self):
        with TemporaryDirectory() as tmp_dir_name:
            tmp_name = join(tmp_dir_name, "temp2.id")
            tmp_id = identifier.get_identifier_bytes(tmp_name)
            self.assertIsInstance(tmp_id, bytes)
            self.assertEqual(len(tmp_id), identifier.IDENTIFIER_SIZE)

            for _ in range(10):
                self.assertEqual(tmp_id, identifier.get_identifier_bytes(tmp_name))

            self.assertNotEqual(identifier.generate_identifier_bytes(tmp_name, identifier.IDENTIFIER_SIZE + 1000),
                                tmp_id)
