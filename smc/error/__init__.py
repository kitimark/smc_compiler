from enum import Enum

class Error(Exception):
  def __init__(self, error_code=None, token=None, message=None):
    message = f'{self.__class__.__name__}: {message}'
    super().__init__(message)
    self.error_code = error_code
    self.token = token
    self.message = message

class LexerError(Error):
  pass

class ParserError(Error):
  pass

class InstructionError(Error):
  pass

class SemanticError(Error):
  pass

class ErrorCode(Enum):
  UNEXPECTED_COMMAND = 'Unexpected command'
  UNEXPECTED_ARGUMENTS = 'Unexpected arguments'
  DUPLICATE_LABEL = 'Label has already been declared'
  UNEXPECTED_TOKEN = 'Unexpected token'  
  EMPTY_STATEMENT_LIST = 'Statement list is empty'
