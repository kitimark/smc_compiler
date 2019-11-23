import unittest

from smc.binary import Binary

class BinaryTest(unittest.TestCase):
  def test_init(self):
    actual = Binary(auto=5, bits=32)
    self.assertEqual(actual.bin, '00000000000000000000000000000101')

    actual = Binary(auto=8454151, bits=32)
    self.assertEqual(actual.bin, '00000000100000010000000000000111')

    actual = Binary(auto='0b0000000000000000000000000101', bits=32)
    self.assertEqual(actual.bin, '00000000000000000000000000000101')
