import unittest

from smc.binary import Instruction
from smc.error import Error, InstructionError

class TestInstruction(unittest.TestCase):
  def test_init(self):
    actual = Instruction(0, 'add', '1', '2', '3')
    self.assertEqual(actual.type, 'r_type')

    actual = Instruction(1, 'halt')
    self.assertEqual(actual.type, 'o_type')

    actual = Instruction(2, 8454151)
    
    with self.assertRaises(InstructionError):
      Instruction(0, 'abc', '5', '5', '5')