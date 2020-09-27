# built in libraries
from functools import lru_cache
import json


@lru_cache(maxsize=5000)
def save_int(number):
    """
    info: Saves an unsigned int
    :param number: int
    :return: bytes
    """
    return save_data(number.to_bytes(number.bit_length() // 8 + min(number.bit_length() % 8, 1), byteorder="big"))


def load_int(object_byte_array):
    """
    info: Loads an unsigned int
    :param object_byte_array: bytearray
    :return: int
    """
    return int.from_bytes(load_data(object_byte_array), byteorder="big")


@lru_cache(maxsize=5000)
def save_data(data):
    """
    info: Saves bytes
    :param data: bytes
    :return: bytes
    """
    data_size = len(data)
    data_size_in_bytes = data_size.to_bytes(data_size.bit_length() // 8 + min(data_size.bit_length() % 8, 1),
                                            byteorder="big")
    number_size = len(data_size_in_bytes)
    return bytes((number_size, *data_size_in_bytes, *data))


def load_data(object_byte_array):
    """
    info: Loads bytes
    :param object_byte_array: bytearray
    :return: bytes
    """
    number_size = object_byte_array[0]
    data_size = int.from_bytes(object_byte_array[1:number_size+1], byteorder="big")
    data = object_byte_array[number_size+1: number_size+1+data_size]
    del object_byte_array[:number_size+1+data_size]
    return data


class FastHandObjectPacker:
    def __bytes__(self):
        """
        info: object to bytes
        :return: bytes
        """
        return self.to_bytes()

    def to_bytes(self):
        """
        info: object to bytes
        :return: bytes
        """
        raise NotImplementedError()

    @classmethod
    def start_from_bytes(cls, object_bytes):
        """
        info: from bytes to object
        :param object_bytes: bytearray, bytes, list, tuple
        :return: object
        """
        if isinstance(object_bytes, (bytes, list, tuple)):
            return cls.from_bytes(bytearray(object_bytes))
        return cls.from_bytes(object_bytes)

    @classmethod
    def from_bytes(cls, object_byte_array):
        """
        info: from bytes to object
        :param object_byte_array: bytearray
        :return: object
        """
        raise NotImplementedError()


class ObjectPackerJsonError(Exception):
    pass


class ObjectPackerJson:
    def __init__(self, fast_hand_object_packer_objects=None):
        """
        info: Makes a ObjectPackerJson
        :param fast_hand_object_packer_objects: None, tuple, list
        """
        if fast_hand_object_packer_objects is None:
            fast_hand_object_packer_objects = ()

        self._fast_hand_object_packer = fast_hand_object_packer_objects
        self._fast_hand_object_packer_dict = {fhopc.__name__: fhopc for fhopc in fast_hand_object_packer_objects}

    def dumps(self, data):
        """
        info: object to bytes
        :param data: object
        :return: bytes
        """
        fast_object_data = bytearray()
        json_data = bytes(json.dumps(self._dumps(data, fast_object_data)), encoding="utf-8")

        byte_data = save_data(json_data) + fast_object_data
        return byte_data

    def loads(self, data):
        """
        info: bytes to object
        :param data: bytearray, bytes, list, tuple
        :return: object
        """
        if isinstance(data, (bytes, list, tuple)):
            data = bytearray(data)

        json_data = json.loads(str(load_data(data), encoding="utf-8"))
        return self._loads(json_data, data)

    def _dumps(self, data, fast_object_data):
        """
        info: object to json
        :param data: object
        :param fast_object_data: bytearray
        :return: list
        """
        if data is None:
            return ["none", data]
        elif isinstance(data, bool):
            return ["bool", data]
        elif isinstance(data, str):
            return ["str", data]
        elif isinstance(data, int):
            return ["int", data]
        elif isinstance(data, float):
            return ["float", data]
        elif isinstance(data, tuple):
            return ["tuple", [self._dumps(obj, fast_object_data) for obj in data]]
        elif isinstance(data, list):
            return ["list", [self._dumps(obj, fast_object_data) for obj in data]]
        elif isinstance(data, set):
            return ["set", [self._dumps(obj, fast_object_data) for obj in data]]
        elif isinstance(data, dict):
            return ["dict", [[self._dumps(key, fast_object_data), self._dumps(data[key], fast_object_data)] for key in data]]
        elif isinstance(data, bytes):
            fast_object_data.extend(save_data(data))
            return ["bytes"]
        elif isinstance(data, bytearray):
            fast_object_data.extend(save_data(bytes(data)))
            return ["bytearray"]
        elif isinstance(data, FastHandObjectPacker):
            fast_object_data.extend(save_data(data.to_bytes()))
            return ["fast_hand_object_packer", data.__class__.__name__]
        return ObjectPackerJsonError("Can't dump type: {}".format(type(data)))

    def _loads(self, data, fast_object_data):
        """
        info: json to object
        :param data: list
        :param fast_object_data: bytearray
        :return: object
        """
        if data[0] in ("none", "bool", "str", "int", "float"):
            return data[1]
        elif data[0] == "tuple":
            return tuple([self._loads(obj, fast_object_data) for obj in data[1]])
        elif data[0] == "list":
            return [self._loads(obj, fast_object_data) for obj in data[1]]
        elif data[0] == "set":
            return set([self._loads(obj, fast_object_data) for obj in data[1]])
        elif data[0] == "dict":
            return dict([[self._loads(key, fast_object_data), self._loads(obj, fast_object_data)] for key, obj in data[1]])
        elif data[0] == "bytes":
            return bytes(load_data(fast_object_data))
        elif data[0] == "bytearray":
            return bytearray(load_data(fast_object_data))
        elif data[0] == "fast_hand_object_packer":
            return self._fast_hand_object_packer_dict[data[1]].start_from_bytes(load_data(fast_object_data))


DEFAULT_OBJECT_PACKER_JSON = ObjectPackerJson()
