from .error import ParserError, ErrorCode
from .token import TokenType
from .abstract_syntax_tree import (
  Label,
  Register,
  Offset,
  RType,
  IType,
  JType,
  OType,
  FillType
)

class Parser(object):
  def __init__(self, lexer):
    self.lexer = lexer
    self._skip_empty_line()

  def _get_next_token(self):
    return self.lexer.get_next_token()

  def _skip_empty_line(self):
    self.current_token = self._get_next_token()
    while(self.current_token.type is TokenType.EOL):
      self.current_token = self._get_next_token()

  def _error(self, error_code, token):
    raise ParserError(
      error_code=error_code,
      token=token,
      message=f'{error_code} -> {token}'
    )

  def _eat(self, token_type=None):
    # token type can be single, list or tuple
    if (token_type is None or
      self.current_token.type == token_type 
      or type(token_type) in (list, tuple)
      and self.current_token.type in token_type
    ):
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

  def register(self):
    """
    register: INTEGER
    """
    node = Register(self.current_token)
    self._eat(TokenType.INTERGER)
    return node

  def offset(self):
    """
    offset: INTEGER
    """
    node = Offset(self.current_token)
    self._eat(TokenType.INTERGER)
    return node

  def field(self):
    """
    field: register
         | label
    """
    if self.current_token.type is TokenType.INTERGER:
      node = self.offset()
    else:
      node = self.label()

    return node

  def opcode(self):
    node = self.current_token
    self._eat(TokenType.MNEMONIC_LISTS())
    return node

  def r_type(self):
    opcode_node = self.opcode()
    field0_node = self.register()
    field1_node = self.register()
    field2_node = self.register()
    return RType(opcode_node, field0_node, field1_node, field2_node)

  def i_type(self):
    opcode_node = self.opcode()
    field0_node = self.register()
    field1_node = self.register()
    field2_node = self.field()
    return IType(opcode_node, field0_node, field1_node, field2_node)

  def j_type(self):
    opcode_node = self.opcode()
    field0_node = self.register()
    field1_node = self.register()
    return JType(opcode_node, field0_node, field1_node)

  def o_type(self):
    opcode_node = self.opcode()
    return OType(opcode_node)

  def fill_type(self):
    opcode_node = self.opcode()
    field_node = self.field()
    return FillType(opcode_node, field_node)

  def instruction(self):
    if self.current_token.type in TokenType.R_TYPE():
      return self.r_type()

    if self.current_token.type in TokenType.I_TYPE():
      return self.i_type()

    if self.current_token.type in TokenType.J_TYPE():
      return self.j_type()

    if self.current_token.type in TokenType.O_TYPE():
      return self.o_type()

    if self.current_token.type is TokenType.FILL:
      return self.fill_type()
  
    self._error(
      error_code=ErrorCode.UNEXPECTED_TOKEN,
      token=self.current_token
    )

  def _skip_comment(self):
    while self.current_token.type not in (TokenType.EOL, TokenType.EOF):
      self._eat()

  def statement(self):
    """
    statement: instuction EOF \n
    it will be skip comment each line
    """
    inst_node = self.instruction()
    self._skip_comment()
    if self.current_token.type is not TokenType.EOF:
      self._skip_empty_line()
    return inst_node

  def statement_list(self):
    """
    statement_list: statement+
    """
    statements = []
    while self.current_token.type in TokenType.MNEMONIC_LISTS():
      statements.append(self.statement())

    return statements
