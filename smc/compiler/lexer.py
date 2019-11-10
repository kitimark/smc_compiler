from .token import Token, TokenType
from ..error import LexerError

class Lexer(object):
  def __init__(self, text):
    if text:
      self.text = text
    else:
      # CASE: text is empty string
      self.text = ' '

    self.pos = 0
    self.current_char = self.text[self.pos]
    # position of token
    self.line = 1
    self.column = 1

  def _advance(self):
    """
      Advance the `pos` pointer and set the `current_char`
    """
    if self.current_char == '\n':
      self.line += 1
      self.column = 0
    
    self.pos += 1
    if self.pos > len(self.text) - 1:
      self.current_char = None # end of text
    else:
      self.current_char = self.text[self.pos]
      self.column += 1

  def _skip_whitespace(self):
    while self.current_char is not None and self.current_char is ' ':
      self._advance()

  def _word(self):
    """Handle words and reserved keywords"""
    token = Token(type=None, value=None, line=self.line, column=self.column)

    # CASE: dot at first character
    value = self.current_char 
    self._advance()

    while self.current_char is not None and self.current_char.isalnum():
      value += self.current_char
      self._advance()
    
    token_type = Token.RESERVED_KEYWORDS().get(value)
    if token_type is None:
      token.type = TokenType.WORD
      token.value = value
    else:
      # reserved keyword
      token.type = token_type
      token.value = value

    return token
    
  def _number(self):
    token = Token(type=None, value=None, line=self.line, column=self.column)

    value = ''
    while self.current_char is not None and self.current_char.isdigit():
      value += self.current_char
      self._advance()

    token.type = TokenType.INT 
    token.value = int(value)

    return token

  def _special_chareacter(self):
    token = Token(
      type=TokenType.SPC, 
      value=self.current_char, 
      line=self.line, 
      column=self.column
    )
    self._advance()
    return token

  def _new_line(self):
    token = Token(type=TokenType.EOL, value=None, line=self.line, column=self.column)
    self._advance()
    return token

  def _error(self):
    s = f"Lexer error on {self.current_char} ({self.line}:{self.column})"
    raise LexerError(message=s)

  def get_next_token(self):
    """
    Lexical analyzer
    """
    while self.current_char is not None:
      if self.current_char == '\n':
        return self._new_line()

      if self.current_char is ' ':
        self._skip_whitespace()
        continue

      if self.current_char.isalpha() or self.current_char == '.':
        return self._word()

      if self.current_char.isdigit():
        return self._number()

      try:
        token_type = TokenType(self.current_char)
        self._advance()
      except ValueError:
        return self._special_chareacter()
      else: 
        return Token(
          type=token_type,
          value=token_type.value,
          line=self.line,
          column=self.column
        )

    # End of file
    return Token(type=TokenType.EOF, value=None)
      