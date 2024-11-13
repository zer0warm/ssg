import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_error_no_tag(self):
        node = ParentNode(None, [
            LeafNode(None, 'Check out '),
            LeafNode('a', 'this site', props={'href': 'https://github.com'}),
            LeafNode(None, ', it is awesome!')
        ])
        self.assertRaisesRegex(ValueError, 'ParentNode must have a tag', node.to_html)

    def test_error_no_children(self):
        node = ParentNode('p', [])
        self.assertRaisesRegex(ValueError, 'ParentNode must have children', node.to_html)

    def test_to_html(self):
        node = ParentNode('p', [
            LeafNode(None, 'Check out '),
            LeafNode('a', 'this site', props={'href': 'https://github.com'}),
            LeafNode(None, ', it is awesome!')
        ])
        expected_html = '''<p>Check out <a href="https://github.com">this site</a>, it is awesome!</p>'''
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_nested_parents(self):
        node = ParentNode('p', [
            LeafNode(None, 'List of food:'),
            ParentNode('ul', [
                LeafNode('li', 'Apple salad', props={'style': 'color:red'}),
                LeafNode('li', 'Orange juice', props={'style': 'color:orange'})
            ]),
            LeafNode(None, 'Check out '),
            LeafNode('a', 'this site', props={'href': 'https://github.com'}),
            LeafNode(None, ', it is awesome!')
        ])
        expected_html = ''.join([
            '<p>List of food:',
            '<ul>',
            '<li style="color:red">Apple salad</li>',
            '<li style="color:orange">Orange juice</li>',
            '</ul>',
            'Check out ',
            '<a href="https://github.com">this site</a>',
            ', it is awesome!</p>'
        ])
        self.assertEqual(node.to_html(), expected_html)

    def test_is_parentnode(self):
        node = ParentNode('head', [LeafNode('title', 'Awesome title')])
        self.assertIs(type(node), ParentNode)


if __name__ == '__main__':
    unittest.main()
