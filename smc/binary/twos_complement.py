from bitstring import Bits, ByteStore, CreationError

class TwosComplement(Bits):
  def __init__(self, auto=None, bits=None, **kwargs):
    if not isinstance(self._datastore, ByteStore):
      self._ensureinmemory()
      
  def __new__(cls, auto=None, bits=None, **kwargs):
    """
      Scope of **kwargs with keys:
      bin -- binary string representation, e.g. '0b001010'.
      hex -- hexadecimal string representation, e.g. '0x2ef'
      oct -- octal string representation, e.g. '0o777'.
      int -- a signed integer.
    """
    x = super(TwosComplement, cls).__new__(cls)
    x._check_kwargs(**kwargs)
    # y = Bits.__new__(TwosComplement, length=bits, **kwargs)
    y = TwosComplement._initialise_object(auto, length=bits, **kwargs)
    x._datastore = ByteStore(y._datastore._rawarray[:],
                              y._datastore.bitlength,
                              y._datastore.offset)
    return x
  
  @classmethod
  def _initialise_object(cls, auto, length, **kwargs):
    try :
      if isinstance(auto, int):
        return Bits.__new__(cls, length=length, int=auto)
      if isinstance(auto, str):
        integer = int(auto, 0)
        return Bits.__new__(cls, length=length, int=integer)
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

  keys = ['bin', 'hex', 'oct', 'int']