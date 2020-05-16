import unittest
from myblog.myutils import *


class TestMyUtils(unittest.TestCase):

    def test_get_url_slug(self):

        self.assertEqual(get_url_slug('This is my title'), 'this-is-my-title')
        self.assertEqual(get_url_slug('Today is a good day'), 'today-is-a-good-day')



if __name__ == "__main__":
    unittest.main()

