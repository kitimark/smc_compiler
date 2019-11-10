from typing import List

class AST(object):
  """
  Abstract Syntax Tree
  """
  pass

class Label(AST):
  """Label node is constructed out of WORD token"""
  def __init__(self, token):
    self.token = token
    self.value = token.value

class Register(AST):
  """Register node is constructed out of INTEGER token"""
  def __init__(self, token):
    self.token = token
    self.value = token.value

class Offset(AST):
  def __init__(self, unary, integer):
    self.unary = unary
    self.integer = integer

class Unary(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

class Number(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

class Opcode(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

class Instruction(AST):
  def __init__(self, address, opcode):
    self.address = address
    self.opcode = opcode

class RType(Instruction):
  def __init__(self, address, opcode, field0, field1, field2):
    super().__init__(address, opcode)
    self.field0 = field0
    self.field1 = field1
    self.field2 = field2

class IType(Instruction):
  def __init__(self, address, opcode, field0, field1, field2):
    super().__init__(address, opcode)
    self.field0 = field0
    self.field1 = field1
    self.field2 = field2

class JType(Instruction):
  def __init__(self, address, opcode, field0, field1):
    super().__init__(address, opcode)
    self.field0 = field0
    self.field1 = field1

class OType(Instruction):
  def __init__(self, address, opcode):
    super().__init__(address, opcode)

class FillType(Instruction):
  def __init__(self, address, opcode, field0):
    super().__init__(address, opcode)
    self.field0 = field0

class Method(AST):
  def __init__(self, label, statements):
    self.label = label
    self.statements = statements

  def address(self):
    return self.statements[0].address

class Initial(AST):
  def __init__(self, statements):
    self.statements = statements

class Program(AST):
  def __init__(self, initial, methods):
    self.initial = initial
    if methods:
      self.methods = methods
    else:
      self.methods = None
