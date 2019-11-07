import unittest

from smc.compiler import(
  Parser, 
  ParserError, 
  Lexer, 
  TokenType
)

from smc.compiler.abstract_syntax_tree import (
  Label
)

class TestParser(unittest.TestCase):

  def _init_parser(self, text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    return parser

  def test_label(self):
    parser = self._init_parser('text')
    actual = parser.label()
    
    self.assertEqual(actual.token.type, TokenType.WORD)

    with self.assertRaises(ParserError):
      parser = self._init_parser('add') 
      parser.label()