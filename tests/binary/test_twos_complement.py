import unittest

from smc.binary import TwosComplement
from bitstring import CreationError

class TestTwosComplement(unittest.TestCase):
  def test_init(self):

    actual = TwosComplement(int=5, bits=32)
    self.assertEqual(actual.bin, '00000000000000000000000000000101')
    self.assertEqual(TwosComplement(actual).int, 5)
    self.assertEqual(TwosComplement(bits=32).int, 0)
    self.assertEqual(TwosComplement('0b1010', bits=32).int, 10)
    self.assertEqual(TwosComplement(5, bits=32).int, 5)

    self.assertRaises(CreationError, TwosComplement, ['exception'])
    self.assertRaises(CreationError, TwosComplement, 'exception')
    self.assertRaises(CreationError, TwosComplement, value=5, bits=32)

  def test_add(self):
    actual = TwosComplement(int=-4, bits=32) + 4
    self.assertEqual(actual.int, 0)

    actual = 4 + TwosComplement(int=-4, bits=16)
    self.assertEqual((actual.int, actual.len), (0, 32))

  def test_minus(self):
    actual = TwosComplement(int=4) - 4
    self.assertEqual(actual.int, 0)

    actual = 4 - TwosComplement(int=4)
    self.assertEqual(actual.int, 0)
    