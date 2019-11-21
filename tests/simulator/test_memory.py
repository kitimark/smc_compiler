import unittest

from smc.simulator.memory import Memory
from smc.binary import TwosComplement, Instruction

class TestMemory(unittest.TestCase):
  def test_get_memory(self):
    instance = Memory([8454151, -5])

    actual = instance.get_memory(0, Instruction)
    self.assertEqual(type(actual), Instruction)

    actual = instance.get_memory(1, TwosComplement)
    self.assertEqual(type(actual), TwosComplement)