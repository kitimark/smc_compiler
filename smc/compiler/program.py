from ..error import SemanticError, ErrorCode
from ..binary import Instruction

class LabelTable(object):
  def __init__(self):
    self.labels = {}

  def _error(self, token):
    raise SemanticError(
      error_code=ErrorCode.DUPLICATE_LABEL,
      token=token,
      message=f'Label "{token.value}" has already define'
    ) 

  def insert(self, token, address):
    if token.value in self.labels.keys():
      self._error(token)

    self.labels[token.value] = {
      'address': address
    }

class StatementList(object):
  def __init__(self):
    self.statements = []
  
  def __setitem__(self, address, token):
    # TODO: add statement in statements list
    pass

  def insert(self, statement):
    self.statements.append(statement)

class Program(object):
  def __init__(self, labels: LabelTable, statements: StatementList):
    self.labels = labels
    self.statements = statements
