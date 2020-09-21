# tamcolors libraries
from tamcolors.utils import object_packer


class LastSentCache:
    def __init__(self):
        """
        info: Make a LastSentCache Object
        """
        self._last_data = bytes()

    def __call__(self, data):
        """
        info: Will pack data to be transport
        :param data: bytes
        :return: bytes
        """
        if len(data) == len(self._last_data):
            data_bit_blocks = bytearray((1,))

            start = None
            bit_block = bytearray()
            for spot, bit in enumerate(self._last_data):
                if bit != data[spot]:
                    if start is None:
                        start = spot
                    bit_block.append(data[spot])
                elif start is not None:
                    data_bit_blocks.extend(object_packer.save_int(start))
                    data_bit_blocks.extend(object_packer.save_data(bytes(bit_block)))
                    start = None
                    bit_block.clear()

            if start is not None:
                data_bit_blocks.extend(object_packer.save_int(start))
                data_bit_blocks.extend(object_packer.save_data(bytes(bit_block)))

            if len(data_bit_blocks) < len(data):
                self._last_data = data
                return bytes(data_bit_blocks)

        self._last_data = data
        return bytes((0,)) + data


class LastReceivedCache:
    def __init__(self):
        """
        info: Makes a LastReceivedCache Object
        """
        self._last_data = bytes()

    def __call__(self, data):
        """
        info: Will unpack data from the cache
        :param data: bytes
        :return: bytes
        """
        if data[0] == 0:
            self._last_data = data[1:]
            return self._last_data

        unpacked_data = bytearray(self._last_data)
        bit_blocks = bytearray(data[1:])

        while len(bit_blocks):
            start = object_packer.load_int(bit_blocks)
            bit_block = object_packer.load_data(bit_blocks)
            for spot, bit in enumerate(bit_block):
                unpacked_data[start + spot] = bit

        unpacked_data = bytes(unpacked_data)
        self._last_data = unpacked_data
        return unpacked_data
