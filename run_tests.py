import unittest

# Add lament to path
from os import getcwd
from sys import path
from os.path import join
path.append(join(getcwd(), 'lament'))

# Test Suite
suite = unittest.TestLoader().discover('./tests/')
unittest.TextTestRunner(verbosity=2).run(suite)
