class Binary(object):
  def __init__(self, value: any, bits: int) -> None:
    self.value = value
    self.bits = bits
  
  def __str__(self) -> str:
    return f'{self.value:0{self.bits}b}'
