# tamcolors libraries
from tamcolors import tam_io


"""
TAMKeyManger mange key input
"""


class TAMKeyManager:
    def __init__(self, all_keys=tam_io.tam_keys.KEYS):
        """
        info: makes a TAMKeyManager object
        :param all_keys: tuple or list: [(str, str), ...]
        """
        self.__all_keys = {key[0]: 0 for key in all_keys}
        self.__raw_input = ()
        self.__input_generator = self.get_user_input_generator()

    def __iter__(self):
        """
        info: iteration objects
        :return: generator
        """
        return self.__input_generator

    def update(self, keys):
        """
        info: will update key manager with next set of keys
        :param keys: tuple or list: [(str, str), ...]
        :return:
        """
        for key in self.__all_keys:
            self.__all_keys[key] = 0

        for key in keys:
            self.__all_keys[key[0]] += 1

        self.__raw_input = keys
        self.__input_generator = self.get_user_input_generator()

    def get_key_state(self, key):
        """
        info: will get a state of a key
        :param key: str
        :return: int
        """
        return self.__all_keys[key]

    def silent_key_state(self, key):
        """
        info: will get a key state and make it 0
        :param key: str
        :return: int
        """
        key_state = self.__all_keys[key]
        if key_state:
            self.__all_keys[key] = 0
        return key_state

    def get_user_input(self):
        """
        info: will the next key the user enters
        :return: tuple, list or None: (str, str)
        """
        try:
            return next(self.__input_generator)
        except StopIteration:
            pass

    def get_raw_user_input(self):
        """
        info: will get the raw user input
        :return: list or tuple: [(str, str), ...]
        """
        return self.__raw_input

    def get_user_input_generator(self):
        """
        info: yields a key at a time
        :return: list or tuple: (str, str)
        """
        for key in self.__raw_input:
            yield key
