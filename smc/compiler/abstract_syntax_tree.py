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

class Command(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

class Instruction(AST):
  def __init__(self, address, command):
    self.address = address
    self.command = command

class RType(Instruction):
  def __init__(self, address, command, field0, field1, field2):
    super().__init__(address, command)
    self.field0 = field0
    self.field1 = field1
    self.field2 = field2

class IType(Instruction):
  def __init__(self, address, command, field0, field1, field2):
    super().__init__(address, command)
    self.field0 = field0
    self.field1 = field1
    self.field2 = field2

class JType(Instruction):
  def __init__(self, address, command, field0, field1):
    super().__init__(address, command)
    self.field0 = field0
    self.field1 = field1

class OType(Instruction):
  def __init__(self, address, command):
    super().__init__(address, command)

class FillType(Instruction):
  def __init__(self, address, command, field0):
    super().__init__(address, command)
    self.field0 = field0

class Method(AST):
  def __init__(self, label, statements):
    self.label = label
    self.statements = statements

  @property
  def address(self):
    return self.statements[0].address

class Initial(AST):
  def __init__(self, statements):
    self.statements = statements

class ParsedTree(AST):
  def __init__(self, initial, methods):
    self.initial = initial
    if methods:
      self.methods = methods
    else:
      self.methods = None
