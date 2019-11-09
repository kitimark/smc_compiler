import unittest

from smc.compiler import(
  Parser, 
  ParserError, 
  Lexer, 
  TokenType
)

from smc.compiler.abstract_syntax_tree import (
  Label,
  Offset,
  Register,
  RType,
  IType,
  JType,
  OType,
  FillType,
  Initial
)

class TestParser(unittest.TestCase):

  def _init_parser(self, text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    return parser

  def assertEquals(self, records):
    for actual, expect in records:
      if type(expect) in (list, tuple):
        self.assertIn(actual, expect)
      else:
        self.assertEqual(actual, expect)

  def test_label(self):
    parser = self._init_parser('text')
    result = parser.label()
    records = (
      (result.token.type, TokenType.WORD),
      (result.value, 'text')
    )
    self.assertEquals(records)

    with self.assertRaises(ParserError):
      parser = self._init_parser('add') 
      parser.label()

  def test_register(self):
    parser = self._init_parser('2')
    result = parser.register()
    records = (
      (result.token.type, TokenType.INT),
      (result.value, 2)
    )
    self.assertEquals(records)

    with self.assertRaises(ParserError):
      parser = self._init_parser('add') 
      parser.register()

  def test_field(self):
    parser = self._init_parser('2')
    actual = parser.field()
    self.assertEqual(actual.token.type, TokenType.INT)

    parser = self._init_parser('test')
    actual = parser.field()
    self.assertEqual(actual.token.type, TokenType.WORD)

    with self.assertRaises(ParserError):
      parser = self._init_parser('add') 
      parser.field()

  def r_type_records(self, text):
    parser = self._init_parser(text)
    result = parser.statement()
    records = (
      (result.__class__, RType),
      (result.field0.__class__, Register),
      (result.field1.__class__, Register),
      (result.field2.__class__, Register),
    )
    return records

  def i_type_records(self, text):
    parser = self._init_parser(text)
    result = parser.statement()
    records = (
      (result.__class__, IType),
      (result.field0.__class__, Register),
      (result.field1.__class__, Register),
      (result.field2.__class__, (Offset, Label)),
    )
    return records

  def j_type_records(self, text):
    parser = self._init_parser(text)
    result = parser.statement()
    records = (
      (result.__class__, JType),
      (result.field0.__class__, Register),
      (result.field1.__class__, Register)
    )
    return records

  def o_type_records(self, text):
    parser = self._init_parser(text)
    result = parser.statement()
    records = [
      (result.__class__, OType)
    ]
    return records

  def fill_type_records(self, text):
    parser = self._init_parser(text)
    result = parser.statement()
    records = (
      (result.__class__, FillType),
      (result.field0.__class__, (Offset, Label))
    )
    return records

  def test_statement(self):
    records = self.r_type_records('add 1 2 3')
    self.assertEquals(records)

    records = self.r_type_records('add 3 2 1 comment test')
    self.assertEquals(records)

    with self.assertRaises(ParserError):
      parser = self._init_parser('add 1 2')
      parser.statement()

    records = self.i_type_records('beq 1 2 3')
    self.assertEquals(records)

    records = self.i_type_records('beq 1 2 3 comment beq')
    self.assertEquals(records)

    records = self.i_type_records('beq 1 2 label comment beq')
    self.assertEquals(records)

    with self.assertRaises(ParserError):
      parser = self._init_parser('beq 1 2')
      parser.statement()

    records = self.j_type_records('jalr 2 3')
    self.assertEquals(records)
    
    with self.assertRaises(ParserError):
      parser = self._init_parser('jalr 1 test')
      parser.statement()

    records = self.o_type_records('halt comment test')
    self.assertEquals(records)

    records = self.fill_type_records('.fill 12')
    self.assertEquals(records)

    records = self.fill_type_records('.fill start')
    self.assertEquals(records)

    with self.assertRaises(ParserError):
      parser = self._init_parser('.fill add')
      parser.statement()

  def test_statement_list(self):
    code = """\
    add   2 3 4
    beq   1 2 test
    halt
    """
    parser = self._init_parser(code)
    result = parser.statement_list()
    records = (
      (result[0].__class__, RType),
      (result[1].__class__, IType),
      (result[2].__class__, OType),
    )
    self.assertEquals(records)

    code = """
    add   2 3 4

    beq   1 2 test
    halt
    """
    parser = self._init_parser(code)
    result = parser.statement_list()
    records = (
      (result[0].__class__, RType),
      (result[1].__class__, IType),
      (result[2].__class__, OType),
    )
    self.assertEquals(records)

    code = """
    add   2 3 4     comment

    beq   1 2 test  comment 



    halt            stop program
    """
    parser = self._init_parser(code)
    result = parser.statement_list()
    records = (
      (result[0].__class__, RType),
      (result[1].__class__, IType),
      (result[2].__class__, OType),
    )
    self.assertEquals(records)

    with self.assertRaises(ParserError):
      parser = self._init_parser(' ')
      result = parser.statement_list()

  def test_method(self):
    code = """
      start add   1 2 3      comment test
            beq   5 5 start

            halt
    """
    parser = self._init_parser(code)
    result = parser.method()
    records = (
      (result.label.__class__, Label),
      (result.label.value, 'start'),
      (result.statements.__class__, list)
    )
    self.assertEquals(records)
    
    with self.assertRaises(ParserError):
      parser = self._init_parser('add 2 3 4')
      parser.method()

  def test_initial(self):
    code = """
    add   1 2 3
    jalr  5 4

    halt
    """
    parser = self._init_parser(code)
    actual = parser.initial()
    self.assertEqual(type(actual), Initial)

    with self.assertRaises(ParserError):
      code = """
      main add   1 2 3
           jalr  5 4

           halt
      """
      parser = self._init_parser(code)
      parser.initial()

  def test_program(self):
    code = """
          add  3 2 1
          beq  2 2 2

    main  add  3 2 2 
          jalr 3 2
    """
    parser = self._init_parser(code)
    result = parser.program()
    records = (
      (result.initial.__class__, Initial),
      (type(result.methods), list)
    )
    self.assertEquals(records)

    code = """
    main  add  3 2 2 
          jalr 3 2
    """
    parser = self._init_parser(code)
    result = parser.program()
    records = (
      (result.initial, None),
      (type(result.methods), list)
    )
    self.assertEquals(records)

    code = """
    add  3 2 2 
    jalr 3 2
    """
    parser = self._init_parser(code)
    result = parser.program()
    records = (
      (result.initial.__class__, Initial),
      (result.methods, None)
    )
    self.assertEquals(records)

  def test_parse(self):
    code = """
          add  3 2 1
          beq  2 2 2

    main  add  3 2 2 
          jalr 3 2
    """
    parser = self._init_parser(code)
    result = parser.parse()
    records = (
      (result.initial.__class__, Initial),
      (type(result.methods), list)
    )
    self.assertEquals(records)

    parser = self._init_parser(' ')
    result = parser.parse()
    records = (
      (result.initial, None),
      (result.methods, None)
    )
    self.assertEquals(records)
