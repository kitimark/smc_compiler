from enum import Enum

class Error(Exception):
  def __init__(self, error_code=None, token=None, message=None):
    self.error_code = error_code
    self.token = token
    self.message = f'{self.__class__.__name__}: {message}'
    pass

class LexerError(Error):
  pass

class ParserError(Error):
  pass

class ErrorCode(Enum):
  UNEXPECTED_TOKEN = 'Unexpected token'  
  EMPTY_STATEMENT_LIST = 'Statement list is empty'
