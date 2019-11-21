import argparse
from ..compiler import Lexer, Parser, SemanticAnalyzer, Interpreter
from ..simulator import Simulator

def main():
  parser = argparse.ArgumentParser(description='SMC Simulator')
  parser.add_argument('inputfile', help='SMC source file')

  args = parser.parse_args()

  text = open(args.inputfile, 'r').read()
  
  # TODO: compile and simulator input file
  lexer = Lexer(text)
  parser = Parser(lexer)
  tree = parser.parse() 
  semanitic_analyzer = SemanticAnalyzer(tree)
  program = semanitic_analyzer.analyze()
  interpreter = Interpreter(program)
  binary = interpreter.interpret()

  simulator = Simulator(binary)
  logs = simulator.execute()
  
  file = open('result.txt', 'w')
  file.write(logs)
  file.close()
