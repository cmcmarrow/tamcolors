# Charles McMarrow libraries
from tamcolors import tam
from tamcolors import checks

# Charles McMarrow

"""
TMAKeyManger mange key input
"""


class TMAKeyManagerError(Exception):
    pass


class TMAKeyManager:
    def __init__(self, all_keys=tam.tma_keys.KEYS):
        """
        info: makes a TMAKeyManager object
        :param all_keys: tuple or list: [(str, str), ...]
        """
        checks.checks.instance_check(all_keys, set, TMAKeyManagerError)
        for key in all_keys:
            checks.checks.in_instances_check(key, (list, tuple), TMAKeyManagerError)
            checks.checks.is_equal_check(len(key), 2, TMAKeyManagerError)
            checks.checks.instance_check(key[0], str, TMAKeyManagerError)
            checks.checks.instance_check(key[1], str, TMAKeyManagerError)

        self.__all_keys = {key[0]: False for key in all_keys}
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
        checks.checks.in_instances_check(keys, (tuple, list), TMAKeyManagerError)
        for key in keys:
            checks.checks.in_instances_check(key, (list, tuple), TMAKeyManagerError)
            checks.checks.is_equal_check(len(key), 2, TMAKeyManagerError)
            checks.checks.instance_check(key[0], str, TMAKeyManagerError)
            checks.checks.instance_check(key[1], str, TMAKeyManagerError)

        for key in self.__all_keys:
            self.__all_keys[key] = False

        for key in keys:
            self.__all_keys[key[0]] = True

        self.__raw_input = keys
        self.__input_generator = self.get_user_input_generator()

    def get_key_state(self, key):
        """
        info: will get a state of a key
        :param key: str
        :return: bool
        """
        checks.checks.item_in_object(key, self.__all_keys, TMAKeyManagerError)
        return self.__all_keys[key]

    def silent_key_state(self, key):
        """
        info: will get a key state and make it False
        :param key: str
        :return: bool
        """
        checks.checks.item_in_object(key, self.__all_keys, TMAKeyManagerError)
        key_state = self.__all_keys[key]
        if key_state:
            self.__all_keys[key] = False
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
