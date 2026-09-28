import unittest
from calculator_core import evaluate,format_number
class Tests(unittest.TestCase):
 def test_precedence(self): self.assertEqual(evaluate('2+3×4'),14)
 def test_parentheses(self): self.assertEqual(evaluate('(2+3)×4'),20)
 def test_percent(self): self.assertEqual(evaluate('200+10%'),220); self.assertEqual(evaluate('200×10%'),20)
 def test_negative(self): self.assertEqual(evaluate('−8÷2'),-4)
 def test_zero_division(self):
  with self.assertRaises(ZeroDivisionError): evaluate('1÷0')
 def test_safe_parser(self):
  with self.assertRaises(ValueError): evaluate("__import__('os').system('whoami')")
 def test_format(self): self.assertEqual(format_number(1000.0),'1 000')
if __name__=='__main__': unittest.main()
