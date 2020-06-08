import unittest
from myblog.models import slugify
from myblog.blogs.utils import get_tags


class TestUtils(unittest.TestCase):

    def test_slugify(self):

        self.assertEqual(slugify('This is my title'), 'this-is-my-title')
        self.assertEqual(slugify('Today is a good day'), 'today-is-a-good-day')

    def test_get_tags(self):
        self.assertEqual(get_tags('Python'), ['Python'])
        self.assertEqual(get_tags(''), [])
        self.assertEqual(get_tags('Python, Flask'), ['Python', 'Flask'])
        self.assertEqual(get_tags('Python,   Flask,'), ['Python', 'Flask'])
        self.assertEqual(get_tags(','), [])




if __name__ == "__main__":
    unittest.main()

