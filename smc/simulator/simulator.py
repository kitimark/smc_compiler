from .register import Register
from .memory import Memory
from ..binary import TwosComplement, Instruction

class Simulator(object):
  def __init__(self, statements):
    self.pc = 0
    self.register = Register()
    self.memory = Memory(statements)
    self._end = False

  def _execute_binary(self, inst):
    method_name = '_execute_' + inst.command
    visitor = getattr(self, method_name)
    visitor(inst)

  def _next_inst(self):
    self.pc += 1

  def _load_reg(self, field):
    reg = field.int    
    data = self.register.get_register(reg)
    return data

  def _write_reg(self, field, data):
    reg = field.int
    self.register.set_register(reg, data)

  def _execute_add(self, inst):
    rs_data = self._load_reg(inst.field_0)
    rt_data = self._load_reg(inst.field_1)

    data = rs_data + rt_data
    self._write_reg(inst.field_2, data)

    self._next_inst()

  def _execute_nand(self, inst):
    rs_data = self._load_reg(inst.field_0)
    rt_data = self._load_reg(inst.field_1)

    data = ~(rs_data & rt_data)
    self._write_reg(inst.field_2, data)

    self._next_inst()


  def _execute_lw(self, inst):
    rs_data = self._load_reg(inst.field_0)

    offset = inst.field_2

    address = rs_data + offset
    data = self.memory.get_memory(address.int, TwosComplement)
    self._write_reg(inst.field_1, data)

    self._next_inst()

  def _execute_sw(self, inst):
    rs_data = self._load_reg(inst.field_0)
    rt_data = self._load_reg(inst.field_1)
    offset = inst.field_2

    address = offset + rs_data
    self.memory.set_memory(address.int, rt_data.int)

    self._next_inst()

  def _execute_beq(self, inst):
    rs_data = self._load_reg(inst.field_0)
    rt_data = self._load_reg(inst.field_1)

    offset = inst.field_2

    if rs_data == rt_data:
      self.pc += offset.int + 1
    else:
      self._next_inst()

  def _execute_jalr(self, inst):
    rs_data = self._load_reg(inst.field_0)

    data = self.pc + 1
    self._write_reg(inst.field_1, data)

    self.pc = rs_data.int

  def _execute_noop(self, inst):
    """ do nothing """
    self._next_inst()

  def _execute_halt(self, inst):
    self._end = True

  def _init_memory_log(self):
    # TODO: return intialize memory
    return ''

  def _simulation_logs(self):
    # TODO: return mem and reg
    return ''

  def execute(self):
    logs = self._init_memory_log()

    while True:
      inst = self.memory.get_memory(self.pc, Instruction) 
      self._execute_binary(inst)
      logs += self._simulation_logs()
      if self._end: break

    return logs