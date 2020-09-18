from functools import lru_cache
import zlib


@lru_cache(maxsize=5000)
def save_int(number):
    return save_data(number.to_bytes(number.bit_length() // 8 + min(number.bit_length() % 8, 1), byteorder="big"))


def load_int(object_byte_array):
    return int.from_bytes(load_data(object_byte_array), byteorder="big")


@lru_cache(maxsize=5000)
def save_data(data):
    data_size = len(data)
    data_size_in_bytes = data_size.to_bytes(data_size.bit_length() // 8 + min(data_size.bit_length() % 8, 1),
                                            byteorder="big")
    number_size = len(data_size_in_bytes)
    return bytes((number_size, *data_size_in_bytes, *data))


def load_data(object_byte_array):
    number_size = object_byte_array[0]
    data_size = int.from_bytes(object_byte_array[1:number_size+1], byteorder="big")
    data = object_byte_array[number_size+1: number_size+1+data_size]
    del object_byte_array[:number_size+1+data_size]
    return data


class ObjectPacker:
    def __bytes__(self):
        return self.to_bytes()

    def to_bytes(self):
        raise NotImplementedError()

    def start_to_bytes(self, compress=True, compress_level=6):
        data = self.to_bytes()
        if compress:
            return zlib.compress(data, level=compress_level)
        return data

    @classmethod
    def start_from_bytes(cls, object_bytes, decompress=True):
        if decompress:
            object_bytes = zlib.decompress(object_bytes)
        if isinstance(object_bytes, bytes):
            return cls.from_bytes(bytearray(object_bytes))
        return cls.from_bytes(object_bytes)

    @classmethod
    def from_bytes(cls, object_byte_array):
        raise NotImplementedError()
