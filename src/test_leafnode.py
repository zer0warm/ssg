import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_creation(self):
        node = LeafNode('a', 'GitHub', props={'href': 'https://github.com'})
        self.assertEqual(node.tag, 'a')
        self.assertEqual(node.value, 'GitHub')
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {'href': 'https://github.com'})

    def test_to_html(self):
        node = LeafNode('a', 'GitHub', props={'href': 'https://github.com'})
        expected = '<a href="https://github.com">GitHub</a>'
        self.assertEqual(node.to_html(), expected)

    def test_raise_valueerror(self):
        node = LeafNode('a', None, props={'href': 'https://github.com'})
        self.assertRaises(ValueError, node.to_html)

    def test_no_tag(self):
        node = LeafNode(None, 'GitHub', props={'href': 'https://github.com'})
        expected = 'GitHub'
        self.assertEqual(node.to_html(), expected)

if __name__ == '__main__':
    unittest.main()
