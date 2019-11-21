from bitstring import Bits, ByteStore, CreationError
from .binary import Binary
from .twos_complement import TwosComplement
from ..error import InstructionError, ErrorCode

class Instruction(object):
  def __init__(self, command, *argv):
    self.command = command
    try:
      self.visitor('_set_', command)(command, *argv)
    except KeyError:
      try:
        bin = Binary(auto=command, bits=32)
        self.init_with_bin(bin)
      except CreationError:
        raise InstructionError(
          error_code=ErrorCode.UNEXPECTED_COMMAND,
          message=f'command "{command}" not found'
        )

    except IndexError:
      raise InstructionError(
        error_code=ErrorCode.UNEXPECTED_ARGUMENTS,
        message=f'arguments not support "{command}" command'
      )
  
  def visitor(self, main_method, command):
    type = type_with_command[command]
    method_name = main_method + type
    visitor = getattr(self, method_name)
    return visitor

  def init_with_bin(self, bin):
    self.opcode = bin[7:10]
    self.command = command_with_opcode[self.opcode]
    self.visitor('_extract_bin_', self.command)(bin)

  def _extract_bin_r_type(self, bin):
    self.field_0 = Binary(auto=bin[10:13])
    self.field_1 = Binary(auto=bin[13:16])
    self.field_2 = Binary(auto=bin[29:32])

  def _extract_bin_i_type(self, bin):
    self.field_0 = Binary(auto=bin[10:13])
    self.field_1 = Binary(auto=bin[13:16])
    self.field_2 = TwosComplement(auto=bin[16:32], bits=16)

  def _extract_bin_j_type(self, bin):
    self.field_0 = Binary(auto=bin[10:13])
    self.field_1 = Binary(auto=bin[13:16])

  def _extract_bin_o_type(self, bin):
    pass

  def binary(self):
    return self.visitor('_bin_', self.command)()

  @property
  def bin(self):
    return self.binary().bin

  @property
  def int(self):
    return self.binary().int

  @property
  def hex(self):
    return self.binary().hex

  def _bin_r_type(self):
    return Binary(
      '0b0000000' + 
      self.opcode.bin + 
      self.field_0.bin + 
      self.field_1.bin + 
      '0000000000000' + 
      self.field_2.bin
    )

  def _bin_i_type(self):
    return Binary(
      '0b0000000' + 
      self.opcode.bin + 
      self.field_0.bin + 
      self.field_1.bin + 
      self.field_2.bin
    )

  def _bin_j_type(self):
    return Binary(
      '0b0000000' + 
      self.opcode.bin + 
      self.field_0.bin + 
      self.field_1.bin + 
      '0000000000000000'
    )

  def _bin_o_type(self):
    return Binary(
      '0b0000000' +
      self.opcode.bin + 
      '0000000000000000000000'
    )

  def _bin_fill_type(self):
    return Binary(f'0b{self.field_0.bin}')

  def _set_r_type(self, command, *params):
    self.opcode = opcode_with_command[command]
    self.type = type_with_command[command]

    self.field_0 = Binary(params[0], 3)
    self.field_1 = Binary(params[1], 3)
    self.field_2 = Binary(params[2], 3)

  def _set_i_type(self, command, *params):
    self.opcode = opcode_with_command[command]
    self.type = type_with_command[command]

    self.field_0 = Binary(params[0], 3)
    self.field_1 = Binary(params[1], 3)
    self.field_2 = TwosComplement(params[2], 16)
  
  def _set_j_type(self, command, *params):
    self.opcode = opcode_with_command[command]
    self.type = type_with_command[command]

    self.field_0 = Binary(params[0], 3)
    self.field_1 = Binary(params[1], 3)

  def _set_o_type(self, command, *params):
    self.opcode = opcode_with_command[command]
    self.type = type_with_command[command]

  def _set_fill_type(self, command, *params):
    self.type = type_with_command[command]
    self.field_0 = TwosComplement(params[0], 32)

command_with_opcode = {
  Binary('0b000', 3) : 'add',
  Binary('0b001', 3) : 'nand',
  Binary('0b010', 3) : 'lw',
  Binary('0b011', 3) : 'sw',
  Binary('0b100', 3) : 'beq',
  Binary('0b101', 3) : 'jalr',
  Binary('0b110', 3) : 'halt',
  Binary('0b111', 3) : 'noop'
}

opcode_with_command = {
  'add'  : Binary(0b000, 3),
  'nand' : Binary(0b001, 3),
  'lw'   : Binary(0b010, 3),
  'sw'   : Binary(0b011, 3),
  'beq'  : Binary(0b100, 3),
  'jalr' : Binary(0b101, 3),
  'halt' : Binary(0b110, 3),
  'noop' : Binary(0b111, 3),
  '.fill': None
}

type_with_command = {
  'add'  : 'r_type',
  'nand' : 'r_type',
  'lw'   : 'i_type',
  'sw'   : 'i_type',
  'beq'  : 'i_type',
  'jalr' : 'j_type',
  'halt' : 'o_type',
  'noop' : 'o_type',
  '.fill': 'fill_type'
}
