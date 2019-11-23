from .register import Register
from .memory import Memory
from ..binary import TwosComplement, Instruction

class Simulator(object):
  """
    Simulator of smc binary
  """
  def __init__(self, statements):
    self.pc = 0
    self.register = Register()
    self.memory = Memory(statements)
    self._end = False
    self.count = 0

  def _execute_binary(self, inst):
    method_name = '_execute_' + inst.command
    visitor = getattr(self, method_name)
    visitor(inst)

  def _next_inst(self):
    self.pc += 1

  def _load_reg(self, field):
    """
    Load data in register
    """
    reg = field.int    
    data = self.register.get_register(reg)
    return data

  def _write_reg(self, field, data):
    """
    Write data in register
    """
    reg = field.int
    self.register.set_register(reg, data)
  
  """
    Execute instruction
  """
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
     self._next_inst()
  
  """
    Generate logs
  """

  def _init_memory_log(self):
    """
    Generate logs of intial memory
    """
    list = ''
    for i,val in enumerate(self.memory):
      list += f'memory[{str(i)}]={str(val)}\n'
    return list

  def _simulation_logs(self): 
    """
    Generate logs each state
    show register state and memory state
    """
    # TODO: return mem and reg
    list = f'\n@@@\nstate:\n\t '
    list += f'pc {self.pc}\n'

    list += f'\tmemory:\n'
    for i,val in enumerate(self.memory):
      list += f'\t\tmem[ {str(i)} ] {str(val)}\n'

    list += f'\tregisters:\n'
    for j,val2 in enumerate(self.register):
      list += f'\t\treg[ {str(j)} ] {str(val2.int)}\n'

    list += f'end state\n'
    return list

  def _simulation_conclusion(self):
    """
      Generate colclusion logs (how many execute instruction)
    """
    list = f'machine halted\ntotal of {self.count} instructions executed\nfinal state of machine:\n'

    return list

  def execute(self):
    logs = self._init_memory_log()

    while True:
      inst = self.memory.get_memory(self.pc, Instruction) 
      logs += self._simulation_logs()
      self._execute_binary(inst)
      self.count += 1
      if self._end: break

    logs += self._simulation_conclusion()
    # Generate final state
    logs += self._simulation_logs()
    return logs