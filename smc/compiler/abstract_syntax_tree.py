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