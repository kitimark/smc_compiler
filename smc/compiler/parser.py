from .error import ParserError, ErrorCode
from .token import TokenType
from .abstract_syntax_tree import (
  Label
)

class Parser(object):
  def __init__(self, lexer):
    self.lexer = lexer
    self.current_token = self._get_next_token()

  def _get_next_token(self):
    return self.lexer.get_next_token()

  def _error(self, error_code, token):
    raise ParserError(
      error_code=error_code,
      token=token,
      message=f'{error_code} -> {token}'
    )

  def _eat(self, token_type):
    if self.current_token.type == token_type:
      self.current_token = self._get_next_token()
    else:
      self._error(
        error_code=ErrorCode.UNEXPECTED_TOKEN,
        token=self.current_token
      )

  def label(self):
    """
    label: WORD
    """
    node = Label(self.current_token)
    self._eat(TokenType.WORD)
    return node