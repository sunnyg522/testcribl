import unittest
import os.path


class suiteTest(unittest.TestCase):
   a = 50
   b = 40
   
   def test_target_logs(self):
      """function to validate agent logs"""
      output_file = os.path.isfile("target.log")
      self.assertTrue(output_file)

   def test_splitter_logs(self):
      """validate splitter logs"""
      output_file = os.path.isfile("splitter.log")
      self.assertTrue(output_file)

   def test_validate_test_output(self):
      """validate test output"""
      num_lines = sum(1 for line in open('events.log'))
      output_file = os.path.isfile("splitter.log")
      self.assertTrue(output_file)
      print(num_lines)
      self.assertEqual(num_lines, 1000000)

if __name__ == '__main__':
   unittest.main()