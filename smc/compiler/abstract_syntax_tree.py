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
  """Offset node is constructed out of INTEGER token"""
  def __init__(self, token):
    self.token = token
    self.value = token.value

class Opcode(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

class RType(AST):
  def __init__(self, opcode, field0, field1, field2):
    self.opcode = opcode
    self.field0 = field0
    self.field1 = field1
    self.field2 = field2

class IType(AST):
  def __init__(self, opcode, field0, field1, field2):
    self.opcode = opcode
    self.field0 = field0
    self.field1 = field1
    self.field2 = field2

class JType(AST):
  def __init__(self, opcode, field0, field1):
    self.opcode = opcode
    self.field0 = field0
    self.field1 = field1

class OType(AST):
  def __init__(self, opcode):
    self.opcode = opcode

class FillType(AST):
  def __init__(self, opcode, field0):
    self.opcode = opcode
    self.field0 = field0

class Method(AST):
  def __init__(self, label, statements):
    self.label = label
    self.statements = statements