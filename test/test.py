import unittest
from shtc.db import DB
from shtc.tagcounter import TagCounter


class TestCounterTests(unittest.TestCase):
    def test_url(self):
        tc = TagCounter()
        # Valid Data
        self.assertTrue(tc.parse_input_url('https://www.test.com'))
        self.assertTrue(tc.parse_input_url('https://test.com'))
        self.assertTrue(tc.parse_input_url('http://test.com'))
        self.assertTrue(tc.parse_input_url('test.com'))
        self.assertTrue(tc.parse_input_url('test'))

        # InValid Data
        self.assertFalse(tc.parse_input_url('https//test.com'))
        self.assertFalse(tc.parse_input_url('http/test.com'))
        self.assertFalse(tc.parse_input_url('no_test'))
        self.assertFalse(tc.parse_input_url(123))
        self.assertFalse(tc.parse_input_url('http/test.c'))
        self.assertFalse(tc.parse_input_url('@.!~123123'))

    def test_db(self):
        db = DB()
        test_name = 'test'
        test_url = 'https://test.test'
        test_inp_data = (test_name, test_url, '01/01/2019 00:00:00', "{'html': 1, 'p': 1}",)
        test_out_data = db.get(test_name, test_url)

        self.assertEqual(test_inp_data, test_out_data)


if __name__ == '__main__':
    unittest.main()
