import unittest
from smc.simulator.register import Register

class TestRegister(unittest.TestCase):
  def test_init(self):
    reg = Register()
    self.assertEqual(reg.__class__, Register)
  
  def test_set(self):
    reg = Register()
    reg.set_register(2, 15)
    self.assertEqual(reg._register[2].bin, '00000000000000000000000000001111')

    reg.set_register(0, 0)
    self.assertEqual(reg._register[0].bin, '00000000000000000000000000000000')

  def test_get(self):
    reg = Register()
    self.assertEqual(reg.get_register(2).int, 0)
