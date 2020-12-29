# built in libraries
import unittest

# tamcolors libraries
from tamcolors.tam_io import tam_surface, tam_colors
from tamcolors.utils import transport_optimizer


class TransportOptimizerTests(unittest.TestCase):
    def test_same_data(self):
        last_sent_cache = transport_optimizer.LastSentCache()
        last_received_cache = transport_optimizer.LastReceivedCache()

        data = bytes([i for i in range(256)])

        packed_data_1 = last_sent_cache(data)
        self.assertEqual(last_received_cache(packed_data_1), data)
        packed_data_2 = last_sent_cache(data)
        self.assertEqual(last_received_cache(packed_data_2), data)
        packed_data_3 = last_sent_cache(data)
        self.assertEqual(last_received_cache(packed_data_3), data)

        self.assertNotEqual(packed_data_1, packed_data_2)
        self.assertGreater(len(packed_data_1), len(packed_data_2))
        self.assertEqual(packed_data_2, packed_data_3)

        for _ in range(50):
            self.assertEqual(last_received_cache(last_sent_cache(data)), data)

    def test_simple_data(self):
        last_sent_cache = transport_optimizer.LastSentCache()
        last_received_cache = transport_optimizer.LastReceivedCache()

        self._pack_and_check(last_sent_cache, last_received_cache, bytes())
        self._pack_and_check(last_sent_cache, last_received_cache, bytes([1]))
        self._pack_and_check(last_sent_cache, last_received_cache, bytes([0, 4, 5, 6, 2, 33, 44, 44]))
        self._pack_and_check(last_sent_cache, last_received_cache, bytes([10, 4, 5, 66, 2, 33, 44, 44]))
        self._pack_and_check(last_sent_cache, last_received_cache, bytes([10, 4, 5, 66, 2, 33, 44, 44, 77]))
        self._pack_and_check(last_sent_cache, last_received_cache, bytes([10, 4, 5, 66]))
        self._pack_and_check(last_sent_cache, last_received_cache, bytes())

    def test_large_data(self):
        last_sent_cache = transport_optimizer.LastSentCache()
        last_received_cache = transport_optimizer.LastReceivedCache()

        data_1 = bytearray(1000)
        data_1[998] = 22

        for _ in range(5):
            self._pack_and_check(last_sent_cache, last_received_cache, data_1)

        data_2 = bytearray(1000)

        for _ in range(5):
            self._pack_and_check(last_sent_cache, last_received_cache, data_2)

        data_3 = bytearray(7000)
        data_3[998] = 22
        data_3[3998] = 55

        for _ in range(5):
            self._pack_and_check(last_sent_cache, last_received_cache, data_3)

    def test_large_tam_surface_data(self):
        last_sent_cache = transport_optimizer.LastSentCache()
        last_received_cache = transport_optimizer.LastReceivedCache()

        surface_1 = tam_surface.TAMSurface(100, 90, "C", tam_colors.RED, tam_colors.ALPHA)
        surface_1.set_spot(33, 44, "D", tam_colors.BLACK, tam_colors.GREEN)

        surface_1_ret = tam_surface.TAMSurface.start_from_bytes(last_received_cache(last_sent_cache(bytes(surface_1))))
        self.assertEqual(surface_1, surface_1_ret)

        surface_2_ret = tam_surface.TAMSurface.start_from_bytes(last_received_cache(last_sent_cache(bytes(surface_1))))
        self.assertEqual(surface_1, surface_2_ret)

        surface_3_ret = tam_surface.TAMSurface.start_from_bytes(last_received_cache(last_sent_cache(bytes(surface_1))))
        self.assertEqual(surface_1, surface_3_ret)

        surface_2 = tam_surface.TAMSurface(100, 90, "Q", tam_colors.LIGHT_WHITE, tam_colors.PURPLE)
        surface_2.set_spot(44, 45, "D", tam_colors.BLACK, tam_colors.GREEN)
        surface_2.set_spot(44, 45, "U", tam_colors.DEFAULT, tam_colors.RED)

        surface_4_ret = tam_surface.TAMSurface.start_from_bytes(last_received_cache(last_sent_cache(bytes(surface_2))))
        self.assertEqual(surface_2, surface_4_ret)

        surface_5_ret = tam_surface.TAMSurface.start_from_bytes(last_received_cache(last_sent_cache(bytes(surface_2))))
        self.assertEqual(surface_2, surface_5_ret)

    def _pack_and_check(self, sent, received, data):
        self.assertEqual(received(sent(data)), data)
