import unittest

from smc.binary import Binary

class BinaryTest(unittest.TestCase):
  def test_init(self):
    actual = Binary(auto=5, bits=32)
    assert actual.bin == '00000000000000000000000000000101'
