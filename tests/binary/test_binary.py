import unittest

from smc.binary import Binary

class BinaryTest(unittest.TestCase):
  def test_init(self):
    actual = Binary(5, 32)
    assert actual.__str__() == '00000000000000000000000000000101'
