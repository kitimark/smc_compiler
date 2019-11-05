try:
  # cli version
  from cli import main
except ImportError:
  # vs code version
  from .cli import main

main()