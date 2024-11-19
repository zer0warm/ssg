import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType
from helpers import textnode_to_htmlnode as t2h, split_nodes_delimiter as sn_delim

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_convert_normal_text(self):
        tn = TextNode('A wild text displayed', TextType.NORMAL)
        Ln = t2h(tn)
        self.assertIs(Ln.tag, None)
        self.assertIs(Ln.props, None)
        self.assertEqual(Ln.value, 'A wild text displayed')
        self.assertEqual(Ln.to_html(), 'A wild text displayed')

    def test_convert_bold_text(self):
        tn = TextNode('Bold of text to assume success', TextType.BOLD)
        Ln = t2h(tn)
        self.assertIs(Ln.props, None)
        self.assertEqual(Ln.tag, 'b')
        self.assertEqual(Ln.value, 'Bold of text to assume success')
        self.assertEqual(Ln.to_html(), '<b>Bold of text to assume success</b>')

    def test_convert_italic_text(self):
        tn = TextNode('Have some Pisa in Italic', TextType.ITALIC)
        Ln = t2h(tn)
        self.assertIs(Ln.props, None)
        self.assertEqual(Ln.tag, 'i')
        self.assertEqual(Ln.value, 'Have some Pisa in Italic')
        self.assertEqual(Ln.to_html(), '<i>Have some Pisa in Italic</i>')

    def test_convert_code_text(self):
        tn = TextNode('print("Hello, world!")', TextType.CODE)
        Ln = t2h(tn)
        self.assertIs(Ln.props, None)
        self.assertEqual(Ln.tag, 'code')
        self.assertEqual(Ln.value, 'print("Hello, world!")')
        self.assertEqual(Ln.to_html(), '<code>print("Hello, world!")</code>')

    def test_convert_link_text(self):
        tn = TextNode('Link start!', TextType.LINK,
                      'https://www.swordart-online.net/')
        Ln = t2h(tn)
        self.assertEqual(Ln.props,
                         {'href': 'https://www.swordart-online.net/'})
        self.assertEqual(Ln.tag, 'a')
        self.assertEqual(Ln.value, 'Link start!')
        html = '<a href="https://www.swordart-online.net/">Link start!</a>'
        self.assertEqual(Ln.to_html(), html)

    def test_convert_image_text_example(self):
        tn = TextNode('An example image', TextType.IMAGE,
                      'https://example.com')
        Ln = t2h(tn)
        self.assertEqual(Ln.props,
                         {'src': 'https://example.com',
                          'alt': 'An example image'})
        self.assertEqual(Ln.tag, 'img')
        self.assertEqual(Ln.value, None)
        html = '<img src="https://example.com" alt="An example image">'
        self.assertEqual(Ln.to_html(), html)

    @unittest.skip("currently unreachable")
    def test_convert_malfunc_text(self):
        tn = TextNode('Invalid node', 'invalid', 'url://point.to.nowhere')
        self.assertRaisesRegex(ValueError, 'invalid text type "invalid"', t2h, tn)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_bold(self):
        nodes = [TextNode('Bold of **text** to assume success', TextType.NORMAL)]
        splitted = sn_delim(nodes, '**', TextType.BOLD)
        expect = [
            TextNode('Bold of ', TextType.NORMAL),
            TextNode('text', TextType.BOLD),
            TextNode(' to assume success', TextType.NORMAL)
        ]
        self.assertEqual(splitted, expect)

    def test_split_bold_start(self):
        nodes = [TextNode('**Bold** of text to assume success', TextType.NORMAL)]
        splitted = sn_delim(nodes, '**', TextType.BOLD)
        expect = [
            TextNode('Bold', TextType.BOLD),
            TextNode(' of text to assume success', TextType.NORMAL)
        ]
        self.assertEqual(splitted, expect)

    def test_split_bold_end(self):
        nodes = [TextNode('Bold of text to assume **success**', TextType.NORMAL)]
        splitted = sn_delim(nodes, '**', TextType.BOLD)
        expect = [
            TextNode('Bold of text to assume ', TextType.NORMAL),
            TextNode('success', TextType.BOLD)
        ]
        self.assertEqual(splitted, expect)

    def test_split_bold_multi(self):
        nodes = [
            TextNode('**Bold** of `text` to *assume success*',
                     TextType.NORMAL),
            TextNode('Bold in Markdown is just <strong>', TextType.NORMAL),
            TextNode('Bold text is <strong>', TextType.BOLD)
        ]
        splitted = sn_delim(nodes, '**', TextType.BOLD)
        expect = [
            TextNode('Bold', TextType.BOLD),
            TextNode(' of `text` to *assume success*', TextType.NORMAL),
            TextNode('Bold in Markdown is just <strong>', TextType.NORMAL),
            TextNode('Bold text is <strong>', TextType.BOLD)
        ]
        self.assertEqual(splitted, expect)

    def test_split_bold_uneven(self):
        nodes = [TextNode('Bold of **text to assume success', TextType.NORMAL)]
        self.assertRaisesRegex(Exception, 'invalid',
                               sn_delim, nodes, '**', TextType.BOLD)

    def test_split_italic_multi(self):
        nodes = [
            TextNode('Have *a Pisa* in `Italic`? You meant `Bold`?',
                     TextType.NORMAL),
            TextNode('should not convert this part', TextType.NORMAL),
            TextNode('should still be bold', TextType.BOLD),
            TextNode('Italic', TextType.CODE)
        ]
        splitted = sn_delim(nodes, '*', TextType.ITALIC)
        expect = [
            TextNode('Have ', TextType.NORMAL),
            TextNode('a Pisa', TextType.ITALIC),
            TextNode(' in `Italic`? You meant `Bold`?', TextType.NORMAL),
            TextNode('should not convert this part', TextType.NORMAL),
            TextNode('should still be bold', TextType.BOLD),
            TextNode('Italic', TextType.CODE)
        ]
        self.assertEqual(splitted, expect)

if __name__ == '__main__':
    unittest.main()
