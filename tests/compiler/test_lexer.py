import unittest
from smc.compiler import TokenType
from smc.compiler import Lexer

class TestLexer(unittest.TestCase):
  def test_tokens(self):
    records = (
      ('1234', TokenType.INTERGER, 1234),
      ('add', TokenType.ADD, 'add'),
      ('.fill', TokenType.FILL, '.fill'),
      ('mark', TokenType.WORD, 'mark')
    )

    for text, token_type, token_value in records:
      lexer = Lexer(text)
      token = lexer.get_next_token()
      self.assertEqual(token.type, token_type)
      self.assertEqual(token.value, token_value)