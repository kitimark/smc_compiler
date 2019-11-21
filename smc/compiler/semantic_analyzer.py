from .program import Program, LabelTable, StatementList

class SemanticAnalyzer(object):
  def __init__(self, tree):
    self.tree = tree
    self.labels = LabelTable()
    self.statements = StatementList()

  def visit(self, node):
    method_name = 'visit_' + type(node).__name__
    visitor = getattr(self, method_name, self.generic_visit)
    return visitor(node)

  def generic_visit(self, node):
    raise Exception(f'No visit_{type(node)} method')

  def visit_ParsedTree(self, node):
    self.visit(node.initial)
    self._methods(node.methods)

  def visit_Initial(self, node):
    self._statements(node.statements)

  def _methods(self, methods):
    for method in methods:
      self.labels.insert(method.label, method.address)
      self._statements(method.statements)

  def _statements(self, statements):
    for statement in statements:
      self.statements.insert(statement)

  def analyze(self):
    tree = self.tree
    if tree is None:
      # TODO: return empty instruction
      return 
    self.visit(tree)
    return Program(self.labels, self.statements)
