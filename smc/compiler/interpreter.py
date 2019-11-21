from .token import TokenType, Token
from .abstract_syntax_tree import Label
from ..binary import Instruction

class Interpreter(object):
  def __init__(self, program):
    self.program = program

  def visitor(self, stmt):
    method_name = '_init_' + type(stmt).__name__
    visitor = getattr(self, method_name)
    return visitor(stmt)

  def _instruct_stmt(self, stmt):
    return self.visitor(stmt)

  def _get_addr_with_label(self, label):
    return self.program.labels[label]['address']

  def _init_RType(self, stmt):
    return Instruction(
      stmt.address,
      stmt.command,
      stmt.field0,
      stmt.field1,
      stmt.field2
    )

  def _init_IType(self, stmt):
    if type(stmt._field2) is Label:
      label = stmt.field2
      address = self._get_addr_with_label(label)
      if stmt._command.type is TokenType.BEQ:
        """ address = pc + 1 + offsetfield """
        field2 = address - stmt.address - 1
        pass
      else:
        field2 = address
    else:
      field2 = stmt.field2

    return Instruction(
      stmt.address,
      stmt.command,
      stmt.field0,
      stmt.field1,
      field2
    )

  def _init_JType(self, stmt):
    return Instruction(
      stmt.address,
      stmt.command,
      stmt.field0,
      stmt.field1
    )

  def _init_OType(self, stmt):
    return Instruction(
      stmt.address,
      stmt.command
    )

  def _init_FillType(self, stmt):
    if type(stmt._field0) is Label:
      label = stmt.field0
      field0 = self._get_addr_with_label(label)
    else:
      field0 = stmt.field0

    return Instruction(
      stmt.address,
      stmt.command,
      field0
    )

  def interpret(self):
    """
      compile assembly to binary
    """
    machine_lang = []
    for statement in self.program.statements:
      if len(machine_lang) != statement.address:
        raise Exception(message="Error address is wrong")

      machine_code = self._instruct_stmt(statement).int
      machine_lang.append(machine_code)

    return machine_lang
