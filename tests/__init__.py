import sys
import unittest

sys.path.append('../smc')

loader = unittest.TestLoader()
testSuite = loader.discover('tests')
testRunner = unittest.TextTestRunner(verbosity=2)
testRunner.run(testSuite)