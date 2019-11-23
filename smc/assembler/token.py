from enum import Enum

def scope_tt_list(start_token, end_token):
  #scope token start instruction and end instruction
  tt_list = list(TokenType)
  start_index = tt_list.index(start_token)
  end_index = tt_list.index(end_token)
  scope_tt_list = [token_type for token_type in tt_list[start_index: end_index + 1]]
  return scope_tt_list

class TokenType(Enum):
  # block of reserved words
  ## R-Type
  ADD      = 'add'
  NAND     = 'nand'
  ## I-Type
  LW       = 'lw'
  SW       = 'sw'
  BEQ      = 'beq'
  ## J-Type
  JALR     = 'jalr'
  ## O-Type
  HALT     = 'halt'
  NOOP     = 'noop'
  ## Spcial Type
  FILL     = '.fill'  

  # misc
  PLUS     = '+'
  MINUS    = '-'
  INT      = 'INTERGER'
  WORD     = 'WORD'
  SPC      = 'SPECIAL_CHAR'
  EOL      = 'END_OF_LINE'
  EOF      = 'END_OF_FILE'

  @staticmethod
  def R_TYPE():
    return scope_tt_list(TokenType.ADD, TokenType.NAND)

  @staticmethod
  def I_TYPE():
    return scope_tt_list(TokenType.LW, TokenType.BEQ)

  @staticmethod
  def J_TYPE():
    return [TokenType.JALR]

  @staticmethod
  def O_TYPE():
    return scope_tt_list(TokenType.HALT, TokenType.NOOP)

  @staticmethod
  def SPCIAL_TYPE():
    return [TokenType.FILL]
  
  @staticmethod
  def MNEMONIC_LISTS():
    # mnemonic is same reserved keyword
    return scope_tt_list(TokenType.ADD, TokenType.FILL)

class Token(object):
  def __init__(self, type, value, line=None, column=None):
    self.type = type
    self.value = value
    self.line = line
    self.column = column

  def __str__(self):
    return f'Token({self.type}, {self.value}, position: ({self.line}:{self.column}))'
  
  @staticmethod
  def RESERVED_KEYWORDS():
    #check token type 
    tt_list = list(TokenType)
    start_index = tt_list.index(TokenType.ADD)
    end_index = tt_list.index(TokenType.FILL)
    reserved_keywords = {
      token_type.value: token_type for token_type in tt_list[start_index: end_index + 1]
    }
    return reserved_keywords