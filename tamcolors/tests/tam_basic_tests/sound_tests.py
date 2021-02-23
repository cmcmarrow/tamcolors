# built in libraries
import unittest.mock
from os.path import dirname, join
from time import sleep

# tamcolors libraries
import tamcolors
from tamcolors.tam_basic import sound
from tamcolors.tests.test_utils import slow_test


def _get_audio_file():
    return join(dirname(tamcolors.examples.basic_sound.__file__), "silence.wav")


class BasicSoundTests(unittest.TestCase):
    def test_sound_init(self):
        self.assertIsInstance(sound.Sound(_get_audio_file()), sound.Sound)

    def test_with_block(self):
        with sound.Sound(_get_audio_file()) as s:
            self.assertTrue(s.is_open())

    def test_close(self):
        s = sound.Sound(_get_audio_file())
        self.assertTrue(s.is_open())
        for _ in range(2):
            s.close()
            for _ in range(5):
                self.assertFalse(s.is_open())

    @staticmethod
    def test_play():
        s = sound.Sound(_get_audio_file())
        s.play()
        s.close()

    @slow_test
    def test_position(self):
        s = sound.Sound(_get_audio_file())
        self.assertEqual(s.get_position(), 0)
        s.play()
        sleep(2)
        self.assertNotEquals(s.get_position(), 0)
        s.pause()
        s.set_position(2)
        self.assertEqual(s.get_position(), 2)
        self.assertEqual(s.get_length(), 31168)

    def test_rest(self):
        s = sound.Sound(_get_audio_file())
        s.rest()
        s.set_position(2)
        s.play(False)
        self.assertTrue(s.is_playing())
        s.rest()
        self.assertFalse(s.is_playing())
        self.assertEqual(s.get_position(), 0)

    @slow_test
    def test_full_play(self):
        s = sound.Sound(_get_audio_file())
        for _ in range(2):
            s.play()
            self.assertTrue(s.is_playing())
            sleep(35)
            self.assertFalse(s.is_playing())

