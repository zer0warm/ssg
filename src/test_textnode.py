import unittest

from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase):
    def test_url_eq(self):
        first = TextNode('A wild Link has appeared', TextType.LINK, 'https://github.com/zer0warm/ssg')
        second = TextNode('A wild Link has appeared', TextType.LINK, 'https://github.com/zer0warm/ssg')
        self.assertEqual(first, second)

    def test_texttype_eq(self):
        first = TextNode('This is an awesome image', TextType.IMAGE, 'https://example.com')
        second = TextNode('This is an awesome image', TextType.IMAGE, 'https://example.com')
        self.assertEqual(first, second)

    def test_url_none_eq(self):
        first = TextNode('This is an awesome image', TextType.IMAGE)
        second = TextNode('This is an awesome image', TextType.IMAGE)
        self.assertEqual(first, second)

    def test_texttype_ne(self):
        first = TextNode('inline text block', TextType.NORMAL)
        second = TextNode('inline text block', TextType.CODE)
        self.assertNotEqual(first, second)

    def test_url_ne(self):
        first = TextNode('A wild Link has appeared', TextType.LINK, 'https://gitlab.com/zer0warm/ssg')
        second = TextNode('A wild Link has appeared', TextType.LINK, 'https://github.com/zer0warm/ssg')
        self.assertNotEqual(first, second)

    def test_all_ne(self):
        first = TextNode('One two three', TextType.BOLD)
        second = TextNode('four five siX', TextType.LINK, 'https://something')
        self.assertNotEqual(first, second)


if __name__ == '__main__':
    unittest.main()
