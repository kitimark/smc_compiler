import unittest

from smc.binary import TwosComplement
from bitstring import CreationError

class TestTwosComplement(unittest.TestCase):
  def test_init(self):

    actual = TwosComplement(int=5, bits=32)
    self.assertEqual(actual.bin, '00000000000000000000000000000101')
    self.assertEqual(TwosComplement(bits=32).int, 0)
    self.assertEqual(TwosComplement('0b1010', bits=32).int, 10)

    self.assertRaises(CreationError, TwosComplement, ['exception'])
    self.assertRaises(CreationError, TwosComplement, 'exception')
    self.assertRaises(CreationError, TwosComplement, value=5, bits=32)
