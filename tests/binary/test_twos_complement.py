import unittest

from smc.binary import TwosComplement
from bitstring import CreationError

class TestTwosComplement(unittest.TestCase):
  def test_init(self):

    actual = TwosComplement(int=5, bits=32)
    self.assertEqual(actual.bin, '00000000000000000000000000000101')

    self.assertRaises(CreationError, TwosComplement, value=5, bits=32)