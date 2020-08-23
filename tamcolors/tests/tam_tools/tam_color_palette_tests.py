# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_tools
from tamcolors.tam_io.tam_colors import *


class TAMColorPaletteTests(unittest.TestCase):
    def test_init_color_palette(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        self.assertIsInstance(color_palette, tam_tools.tam_color_palette.TAMColorPalette)

    def test_init_color_palette_2(self):
        rules = {6: tam_tools.tam_color_palette.TAMDefaultColor(5),
                 7: tam_tools.tam_color_palette.TAMCycleColor((1, 2), 5)}
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 5), rules)
        self.assertIsInstance(color_palette, tam_tools.tam_color_palette.TAMColorPalette)

    def test_str(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        self.assertEqual(str(color_palette), str({key: COLORS[key] for key in range(1, 25)}))

    def test_str_2(self):
        rules = {6: tam_tools.tam_color_palette.TAMDefaultColor(AQUA),
                 7: tam_tools.tam_color_palette.TAMCycleColor((WHITE, GREEN), 5)}
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 6), rules)
        color_palette.update()
        self.assertEqual(str(color_palette), str({key: COLORS[key] for key in range(1, 8)}))

    def test_getitem(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        self.assertEqual(color_palette[15], LIGHT_WHITE)

    def test_getitem_2(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        self.assertEqual(color_palette[20], COLOR_20)

    def test_getitem_3(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        self.assertRaises(tam_tools.tam_color_palette.TAMColorPaletteError, color_palette.__getitem__, -1)

    def test_setitem(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        color_palette[11] = RED
        self.assertEqual(color_palette[11], RED)

    def test_setitem_2(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        color_palette[12] = BLUE
        self.assertEqual(color_palette[12], BLUE)

    def test_setitem_3(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        self.assertRaises(tam_tools.tam_color_palette.TAMColorPaletteError, color_palette.__setitem__, {}, 45)

    def test_get_color(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        self.assertEqual(color_palette.get_color(15), LIGHT_WHITE)

    def test_get_color_2(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        self.assertEqual(color_palette.get_color(20), COLOR_20)

    def test_get_color_3(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        self.assertRaises(tam_tools.tam_color_palette.TAMColorPaletteError, color_palette.get_color, -1)

    def test_set_color(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        color_palette.set_color(11, GREEN)
        self.assertEqual(color_palette.get_color(11), GREEN)

    def test_set_color_2(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        color_palette.set_color(12, BLUE)
        self.assertEqual(color_palette.get_color(12), BLUE)

    def test_set_color_3(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        self.assertRaises(tam_tools.tam_color_palette.TAMColorPaletteError, color_palette.set_color, {}, 45)

    def test_key_present(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        self.assertTrue(color_palette.key_present(4))

    def test_key_present_2(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 25))
        self.assertFalse(color_palette.key_present(-123))

    def test_update(self):
        rules = {6: tam_tools.tam_color_palette.TAMDefaultColor(PURPLE),
                 7: tam_tools.tam_color_palette.TAMCycleColor((RED, GREEN), 1)}
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(range(1, 10), rules)
        for key in range(1, 10):
            self.assertEqual(color_palette[key], COLORS[key])
        color_palette.update()
        self.assertEqual(color_palette[6], PURPLE)
        self.assertEqual(color_palette[7], RED)

    def test_set_rule(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette()
        rule = tam_tools.tam_color_palette.TAMDefaultColor(COLOR_66)
        color_palette.set_rule(5, rule)
        color_palette.update()
        self.assertEqual(color_palette[5], COLOR_66)

    def test_set_rule_2(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette()
        rule = tam_tools.tam_color_palette.TAMDefaultColor(COLOR_66)
        self.assertRaises(tam_tools.tam_color_palette.TAMColorPaletteError, color_palette.set_rule, {}, rule)

    def test_get_rule(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette()
        rule = tam_tools.tam_color_palette.TAMDefaultColor(COLOR_66)
        color_palette.set_rule(5, rule)
        self.assertIs(color_palette.get_rule(5), rule)

    def test_get_rule_2(self):
        color_palette = tam_tools.tam_color_palette.TAMColorPalette()
        self.assertIs(color_palette.get_rule(5), None)


class TAMDefaultColorTests(unittest.TestCase):
    def test_init_default_color(self):
        default_color = tam_tools.tam_color_palette.TAMDefaultColor(COLOR_45)
        self.assertIsInstance(default_color, tam_tools.tam_color_palette.TAMColorPaletteRule)
        self.assertIsInstance(default_color, tam_tools.tam_color_palette.TAMDefaultColor)

    def test_get_color(self):
        default_color = tam_tools.tam_color_palette.TAMDefaultColor(COLOR_45)
        self.assertEqual(default_color.get_color(), COLOR_45)

    def test_set_color(self):
        default_color = tam_tools.tam_color_palette.TAMDefaultColor(COLOR_45)
        default_color.set_color(COLOR_23)
        self.assertEqual(default_color.get_color(), COLOR_23)

    def test_update(self):
        default_color = tam_tools.tam_color_palette.TAMDefaultColor(COLOR_45)
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(color_rules={12: default_color})
        color_palette.update()
        self.assertEqual(color_palette[12], COLOR_45)


class TAMCycleColorTests(unittest.TestCase):
    def test_init_cycle_color(self):
        cycle_color = tam_tools.tam_color_palette.TAMCycleColor((RED, GREEN, YELLOW, BLUE), clock=1)
        self.assertIsInstance(cycle_color, tam_tools.tam_color_palette.TAMColorPaletteRule)
        self.assertIsInstance(cycle_color, tam_tools.tam_color_palette.TAMCycleColor)

    def test_set_colors(self):
        cycle_color = tam_tools.tam_color_palette.TAMCycleColor((BLUE, YELLOW, GREEN, RED), clock=1)
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(color_rules={4: cycle_color})
        color_palette.update()
        self.assertEqual(color_palette[4], BLUE)
        cycle_color.set_colors((RED, GREEN, YELLOW, BLUE))
        color_palette.update()
        self.assertEqual(color_palette[1], RED)

    def test_get_clock(self):
        cycle_color = tam_tools.tam_color_palette.TAMCycleColor((RED, BLUE), clock=2)
        self.assertEqual(cycle_color.get_clock(), 2)

    def test_set_clock(self):
        cycle_color = tam_tools.tam_color_palette.TAMCycleColor((RED, BLUE), clock=2)
        cycle_color.set_clock(45)
        self.assertEqual(cycle_color.get_clock(), 45)

    def test_update(self):
        cycle_color = tam_tools.tam_color_palette.TAMCycleColor((RED, GREEN, YELLOW, BLUE), clock=1)
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(color_rules={4: cycle_color})
        for color in (RED, GREEN, YELLOW, BLUE, RED, GREEN, YELLOW, BLUE):
            color_palette.update()
            self.assertEqual(color_palette[4], color)

    def test_update_2(self):
        cycle_color = tam_tools.tam_color_palette.TAMCycleColor((RED, BLUE), clock=2)
        color_palette = tam_tools.tam_color_palette.TAMColorPalette(color_rules={4: cycle_color})
        for color in (RED, RED, BLUE, BLUE, RED, RED, BLUE):
            color_palette.update()
            self.assertEqual(color_palette[4], color)
