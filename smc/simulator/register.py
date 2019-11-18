from ..binary import TwosComplement

class Register:
  def __init__(self):
    self._register = [
      TwosComplement(0, 32),
      TwosComplement(0, 32),
      TwosComplement(0, 32),
      TwosComplement(0, 32),
      TwosComplement(0, 32),
      TwosComplement(0, 32),
      TwosComplement(0, 32),
      TwosComplement(0, 32),
    ]
  
  def get_register(self, reg_no):
    return self._register[reg_no]

  def set_register(self, reg_on, value):
    self._register[reg_on] = TwosComplement(value, 32) if reg_on != 0 else TwosComplement(0, 32)