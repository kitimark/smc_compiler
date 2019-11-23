from bitstring import Bits, ByteStore, CreationError

class Binary(Bits):
  """
    Binary is unsiged integer in bits
  """
  def __init__(self, auto=None, bits=32, **kwargs) -> None:
    if not isinstance(self._datastore, ByteStore):
      self._ensureinmemory()

  def __new__(cls, auto=None, bits=32, **kwargs):
    x = super(Binary, cls).__new__(cls)
    x._check_kwargs(**kwargs)
    y = Binary._initialise_object(auto, length=bits, **kwargs)
    x._datastore = ByteStore(y._datastore._rawarray[:],
                              y._datastore.bitlength,
                              y._datastore.offset)
    return x

  @classmethod
  def _initialise_object(cls, auto, length, **kwargs):
    try:
      if isinstance(auto, Binary):
        return auto
      if isinstance(auto, int):
        return Bits.__new__(cls, length=length, uint=auto)
      if isinstance(auto, str):
        integer = int(auto, 0)
        return Bits.__new__(cls, length=length, uint=integer)
      if auto is not None:
        raise ValueError
    except ValueError:
      raise CreationError(f"Unreconginised keyword '{auto}' used to initialise.")

    return Bits.__new__(cls, length=length, **kwargs)

  def _check_kwargs(self, **kwargs):
    if not kwargs: 
      return 

    k, v = kwargs.popitem()
    try:
      self.keys.index(k)
    except ValueError:
      raise CreationError(f"Cannot use {k} with this initialiser")

  def __add__(self, bn):
    raise TypeError("unorderable type: {0}".format(type(self).__name__))

  def __radd__(self, bn):
    raise TypeError("unorderable type: {0}".format(type(self).__name__))

  def __sub__(self, bn):
    raise TypeError("unorderable type: {0}".format(type(self).__name__))

  def __rsub__(self, bn):
    raise TypeError("unorderable type: {0}".format(type(self).__name__))

  keys = ['bin', 'hex', 'oct', 'uint']