from enum import Enum

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
  INITIAL  = 'INITIAL'
  INTERGER = 'INTERGER'
  WORD     = 'WORD'
  EOL      = 'EOL' # End of line
  EOF      = 'EOF' # End of file

  @staticmethod
  def MNEMONIC_LISTS():
    # mnemonic is same reserved keyword
    tt_list = list(TokenType)
    start_index = tt_list.index(TokenType.ADD)
    end_index = tt_list.index(TokenType.FILL)
    mnemonic_lists = [token_type for token_type in tt_list[start_index: end_index -1]]

    return mnemonic_lists

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
    tt_list = list(TokenType)
    start_index = tt_list.index(TokenType.ADD)
    end_index = tt_list.index(TokenType.FILL)
    reserved_keywords = {
      token_type.value: token_type for token_type in tt_list[start_index: end_index + 1]
    }
    return reserved_keywords