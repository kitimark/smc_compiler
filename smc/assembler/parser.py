from ..error import ParserError, ErrorCode
from .token import TokenType
from .abstract_syntax_tree import (
  Label,
  Register,
  Offset,
  Unary,
  Number,
  RType,
  IType,
  JType,
  OType,
  FillType,
  Method,
  Initial,
  ParsedTree
)

class Parser(object):
  def __init__(self, lexer):
    self.lexer = lexer
    self.address = 0
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
      message=f'{error_code.value} -> {token}'
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
    self._eat(TokenType.INT)
    return node

  def unary(self):
    node = None
    if self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
      node = Unary(self.current_token)
      self._eat()
    return node

  def number(self):
    node = Number(self.current_token)
    self._eat(TokenType.INT)
    return node

  def offset(self):
    """
    offset: (PLUS | MINUS)? INTEGER
    """
    unary_node = self.unary()
    number_node = self.number()
    node = Offset(unary_node, number_node)
    return node

  def field(self):
    """
    field: offset
         | label
    """
    if self.current_token.type in (TokenType.INT, TokenType.PLUS, TokenType.MINUS):
      node = self.offset()
    else:
      node = self.label()

    return node

  def opcode(self):
    node = self.current_token
    self._eat(TokenType.MNEMONIC_LISTS())
    return node

  def _address(self):
    node = self.address
    self.address += 1
    return node

  def r_type(self):
    address_node = self._address()
    opcode_node = self.opcode()
    field0_node = self.register()
    field1_node = self.register()
    field2_node = self.register()
    return RType(address_node, opcode_node, field0_node, field1_node, field2_node)

  def i_type(self):
    address_node = self._address()
    opcode_node = self.opcode()
    field0_node = self.register()
    field1_node = self.register()
    field2_node = self.field()
    return IType(address_node, opcode_node, field0_node, field1_node, field2_node)

  def j_type(self):
    address_node = self._address()
    opcode_node = self.opcode()
    field0_node = self.register()
    field1_node = self.register()
    return JType(address_node, opcode_node, field0_node, field1_node)

  def o_type(self):
    address_node = self._address()
    opcode_node = self.opcode()
    return OType(address_node, opcode_node)

  def fill_type(self):
    address_node = self._address()
    opcode_node = self.opcode()
    field_node = self.field()
    return FillType(address_node, opcode_node, field_node)

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
    if self.current_token.type is TokenType.EOL:
      self._skip_empty_line()
    return inst_node

  def statement_list(self):
    """
    statement_list: statement+
    """
    statements = []
    while self.current_token.type in TokenType.MNEMONIC_LISTS():
      statements.append(self.statement())

    # throw exception when statement lists is empty
    if not statements:
      self._error(ErrorCode.UNEXPECTED_COMMAND, self.current_token)

    return statements

  def method(self):
    """
    method: label statement_list
    """
    label_node = self.label() 
    statements_node = self.statement_list()
    return Method(label_node, statements_node)

  def initial(self):
    """
    initial: statement_list
    """
    return Initial(self.statement_list())

  def program(self):
    """
    program: initial? method*
    """
    initial_node = None
    if self.current_token.type in TokenType.MNEMONIC_LISTS():
      initial_node = self.initial()

    methods = []
    if self.current_token.type is TokenType.WORD:
      while self.current_token.type is TokenType.WORD:
        methods.append(self.method())

    return ParsedTree(initial_node, methods)

  def parse(self):
    node = self.program()
    if self.current_token.type is not TokenType.EOF:
      # Handle error
      self._error(
        error_code=ErrorCode.UNEXPECTED_TOKEN,
        token=self.current_token
      )
    
    return node
