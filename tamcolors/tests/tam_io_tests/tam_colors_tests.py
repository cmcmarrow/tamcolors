# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors.tam_io import tam_colors


class TAMColorTests(unittest.TestCase):
    def test_colors(self):
        for color in tam_colors.COLORS:
            self.assertIsInstance(color, tam_colors.Color)


class ColorTests(unittest.TestCase):
    def test_color_init(self):
        color = tam_colors.Color(3, 4, tam_colors.RGBA(255, 0, 0))
        self.assertIsInstance(color, tam_colors.Color)

    def test_color_init_2(self):
        color = tam_colors.Color(-2, 4, tam_colors.RGBA(255, 0, 0, 200), 5)
        self.assertIsInstance(color, tam_colors.Color)

    def test_color_eq(self):
        self.assertTrue(tam_colors.Color(3, 4, tam_colors.RGBA(255, 0, 0)) ==
                        tam_colors.Color(3, 4, tam_colors.RGBA(255, 0, 0)))

    def test_color_eq_2(self):
        self.assertFalse(tam_colors.Color(3, 4, tam_colors.RGBA(255, 0, 0)) ==
                         tam_colors.Color(-2, 4, tam_colors.RGBA(255, 0, 0, 200), 5))

    def test_color_eq_3(self):
        self.assertFalse(tam_colors.Color(3, 4, tam_colors.RGBA(255, 0, 0)) == "COLORS")

    def test_color_ne(self):
        self.assertTrue(tam_colors.Color(3, 4, tam_colors.RGBA(255, 0, 0)) !=
                        tam_colors.Color(3, 4, tam_colors.RGBA(255, 0, 1)))

    def test_color_ne_2(self):
        self.assertFalse(tam_colors.Color(3, 4, tam_colors.RGBA(255, 0, 0)) !=
                         tam_colors.Color(3, 4, tam_colors.RGBA(255, 0, 0)))

    def test_get_property(self):
        color = tam_colors.Color(3, 4, tam_colors.RGBA(255, 0, 0))
        self.assertEqual(color.mode_2, 3)
        self.assertEqual(color.mode_16, 3)
        self.assertEqual(color.mode_256, 4)
        self.assertEqual(color.mode_rgb, tam_colors.RGBA(255, 0, 0))

    def test_get_property_2(self):
        color = tam_colors.Color(-2, 4, tam_colors.RGBA(255, 0, 0, 200), 5)
        self.assertEqual(color.mode_2, 5)
        self.assertEqual(color.mode_16, -2)
        self.assertEqual(color.mode_256, 4)
        self.assertEqual(color.mode_rgb, tam_colors.RGBA(255, 0, 0, 200))


class RGBATests(unittest.TestCase):
    def test_rgba_init(self):
        rgb = tam_colors.RGBA(55, 66, 77)
        self.assertIsInstance(rgb, tam_colors.RGBA)

    def test_rgba_init_2(self):
        rgb = tam_colors.RGBA(55, 66, 77, 56, False)
        self.assertIsInstance(rgb, tam_colors.RGBA)

    def test_rgba_eq(self):
        rgb = tam_colors.RGBA(55, 66, 77)
        self.assertTrue(rgb == tam_colors.RGBA(55, 66, 77))

    def test_rgba_eq_2(self):
        rgb = tam_colors.RGBA(55, 66, 77)
        self.assertFalse(rgb == tam_colors.RGBA(55, 66, 77, 88))

    def test_rgba_eq_3(self):
        rgb = tam_colors.RGBA(55, 66, 77)
        self.assertFalse(rgb == "RGBA")

    def test_rgba_ne(self):
        rgb = tam_colors.RGBA(55, 66, 77)
        self.assertTrue(rgb != tam_colors.RGBA(55, 66, 77, 88))

    def test_rgba_ne_2(self):
        rgb = tam_colors.RGBA(55, 66, 77)
        self.assertFalse(rgb != tam_colors.RGBA(55, 66, 77))

    def test_get_property(self):
        rgb = tam_colors.RGBA(55, 66, 77)
        self.assertEqual(rgb.r, 55)
        self.assertEqual(rgb.g, 66)
        self.assertEqual(rgb.b, 77)
        self.assertEqual(rgb.a, 255)
        self.assertEqual(rgb.is_default, False)

    def test_get_property_2(self):
        rgb = tam_colors.RGBA(54, 65, 75, 0, True)
        self.assertEqual(rgb.r, 54)
        self.assertEqual(rgb.g, 65)
        self.assertEqual(rgb.b, 75)
        self.assertEqual(rgb.a, 0)
        self.assertEqual(rgb.is_default, True)
