# built in libraries
import os


IDENTIFIER_FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "identifier.id")
IDENTIFIER_SIZE = 500


def generate_identifier_bytes(identifier_file=IDENTIFIER_FILE_NAME, identifier_size=IDENTIFIER_SIZE):
    identifier_number = os.urandom(identifier_size)
    with open(identifier_file, "wb") as file_handler:
        file_handler.write(identifier_number)
    return identifier_number


def get_identifier_bytes(identifier_file=IDENTIFIER_FILE_NAME):
    if not os.path.isfile(identifier_file):
        return generate_identifier_bytes(identifier_file=identifier_file)

    with open(identifier_file, "rb") as file_handler:
        return file_handler.read()
