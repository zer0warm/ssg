import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_generation(self):
        node = HTMLNode('p', 'A wild paragraph', props={'style': 'color:red'})
        expected_props = 'style="color:red"'
        self.assertEqual(node.props_to_html(), expected_props)

    def test_empty_props(self):
        node = HTMLNode('p', 'A wild paragraph')
        expected_props = ''
        self.assertEqual(node.props_to_html(), expected_props)
    
    def test_children(self):
        node = HTMLNode('ul', children=[
            HTMLNode('li', value='0.5 mL of apple cider'),
            HTMLNode('li', value='1g of pork')])
        self.assertEqual(node.tag, 'ul')
        self.assertEqual(node.value, None)
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[0].tag, 'li')
        self.assertEqual(node.children[0].value, '0.5 mL of apple cider')
        self.assertEqual(node.children[1].tag, 'li')
        self.assertEqual(node.children[1].value, '1g of pork')

    def test_repr(self):
        node = HTMLNode('a', props={'href': 'https://example.com'})
        expected_repr = r'''HTMLNode(tag="a", value=None, children=[], props={'href': 'https://example.com'})'''
        self.assertEqual(repr(node), expected_repr)

    def test_raise_notimplementederror(self):
        node = HTMLNode('p', 'A wild paragraph', props={'style': 'color:red'})
        self.assertRaises(NotImplementedError, node.to_html)

if __name__ == '__main__':
    unittest.main()
