from ..error import SemanticError, ErrorCode
from ..binary import Instruction

class LabelTable(object):
  def __init__(self):
    self.labels = {}

  def _error(self, token, message):
    raise SemanticError(
      error_code=ErrorCode.DUPLICATE_LABEL,
      token=token,
      message=message
    ) 

  def __getitem__(self, key):
    try:
      return self.labels[key]
    except Exception:
      self._error(None, f'Label "{key}" has not define')

  def insert(self, token, address):
    if token.value in self.labels.keys():
      self._error(token, f'Label "{token.value}" has already define')

    self.labels[token.value] = {
      'address': address
    }

class StatementList(object):
  def __init__(self):
    self.statements = []
  
  def __setitem__(self, address, token):
    # TODO: add statement in statements list
    pass

  def __iter__(self):
    self.statements_iter = iter(self.statements)
    return self.statements_iter

  def __next__(self):
    return next(self.statements_iter)

  def insert(self, statement):
    self.statements.append(statement)

class Program(object):
  def __init__(self, labels: LabelTable, statements: StatementList):
    self.labels = labels
    self.statements = statements
