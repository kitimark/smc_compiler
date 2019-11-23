class Memory(object):
  def __init__(self, statments: list):
    self._memory = statments

  def get_memory(self, address, instance):
    # TODO: throw exception when address is out of index 
    mem = self._memory[address]
    return instance(mem)

  def _allocate_memory(self, space):
    for i in range(space):
      self._memory.append(0)

  def set_memory(self, address, data):
    if address >= len(self._memory):
      space = address - len(self._memory) + 1
      self._allocate_memory(space)
    self._memory[address] = data

  def __iter__(self):
    self.memory_iter = iter(self._memory)
    return self.memory_iter

  def __next__(self):
    return next(self.memory_iter)
