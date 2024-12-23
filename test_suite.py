import unittest
from tests.test_single_index_quarterly import TestSingleIndexQuarterly

def suite():
    suite = unittest.TestSuite()
    suite.addTests([TestSingleIndexQuarterly(method_name) for method_name in dir(TestSingleIndexQuarterly) if method_name.startswith("test_")])
    return suite

runner = unittest.TextTestRunner()
runner.run(suite())