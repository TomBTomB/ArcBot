import unittest

from arcbot.command import core as command


class TestCore(unittest.TestCase):
    def test_sample(self):
        self.assertIsNotNone(command)
