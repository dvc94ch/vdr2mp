from unittest import TestCase
from main.vdr2mp import add


class MainTestCase(TestCase):
    def test_add(self):
        assert add(2, 3) == 5
