import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from transformers import (
    textnode_to_htmlnode,
    text_to_textnodes,
    markdown_to_blocks,
    markdown_to_htmlnode
)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_convert_normal_text(self):# {{{
        tn = TextNode('A wild text displayed', TextType.NORMAL)
        Ln = textnode_to_htmlnode(tn)
        self.assertIs(Ln.tag, None)
        self.assertIs(Ln.props, None)
        self.assertEqual(Ln.value, 'A wild text displayed')
        self.assertEqual(Ln.to_html(), 'A wild text displayed')
# }}}
    def test_convert_bold_text(self):# {{{
        tn = TextNode('Bold of text to assume success', TextType.BOLD)
        Ln = textnode_to_htmlnode(tn)
        self.assertIs(Ln.props, None)
        self.assertEqual(Ln.tag, 'b')
        self.assertEqual(Ln.value, 'Bold of text to assume success')
        self.assertEqual(Ln.to_html(), '<b>Bold of text to assume success</b>')
# }}}
    def test_convert_italic_text(self):# {{{
        tn = TextNode('Have some Pisa in Italic', TextType.ITALIC)
        Ln = textnode_to_htmlnode(tn)
        self.assertIs(Ln.props, None)
        self.assertEqual(Ln.tag, 'i')
        self.assertEqual(Ln.value, 'Have some Pisa in Italic')
        self.assertEqual(Ln.to_html(), '<i>Have some Pisa in Italic</i>')
# }}}
    def test_convert_code_text(self):# {{{
        tn = TextNode('print("Hello, world!")', TextType.CODE)
        Ln = textnode_to_htmlnode(tn)
        self.assertIs(Ln.props, None)
        self.assertEqual(Ln.tag, 'code')
        self.assertEqual(Ln.value, 'print("Hello, world!")')
        self.assertEqual(Ln.to_html(), '<code>print("Hello, world!")</code>')
# }}}
    def test_convert_link_text(self):# {{{
        tn = TextNode('Link start!', TextType.LINK,
                      'https://www.swordart-online.net/')
        Ln = textnode_to_htmlnode(tn)
        self.assertEqual(Ln.props,
                         {'href': 'https://www.swordart-online.net/'})
        self.assertEqual(Ln.tag, 'a')
        self.assertEqual(Ln.value, 'Link start!')
        html = '<a href="https://www.swordart-online.net/">Link start!</a>'
        self.assertEqual(Ln.to_html(), html)
# }}}
    def test_convert_image_text_example(self):# {{{
        tn = TextNode('An example image', TextType.IMAGE,
                      'https://example.com')
        Ln = textnode_to_htmlnode(tn)
        self.assertEqual(Ln.props,
                         {'src': 'https://example.com',
                          'alt': 'An example image'})
        self.assertEqual(Ln.tag, 'img')
        self.assertEqual(Ln.value, None)
        html = '<img src="https://example.com" alt="An example image">'
        self.assertEqual(Ln.to_html(), html)
# }}}
    @unittest.skip("currently unreachable")
    def test_convert_malfunc_text(self):# {{{
        tn = TextNode('Invalid node', 'invalid', 'url://point.to.nowhere')
        self.assertRaisesRegex(ValueError, 'invalid text type "invalid"',
                               textnode_to_htmlnode, tn)
# }}}
class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_nodes_only_non_links(self):# {{{
        text = 'Run `bash` and *tell* me **what you see**'
        expect = [
            TextNode('Run ', TextType.NORMAL),
            TextNode('bash', TextType.CODE),
            TextNode(' and ', TextType.NORMAL),
            TextNode('tell', TextType.ITALIC),
            TextNode(' me ', TextType.NORMAL),
            TextNode('what you see', TextType.BOLD)
        ]
        self.assertEqual(text_to_textnodes(text), expect)
# }}}
    def test_text_to_nodes_only_links(self):# {{{
        text = ('Come see this ![picture](https://image.example.com)' +
                ' and remember to follow [me](https://me.bsky.app)')
        expect = [
            TextNode('Come see this ', TextType.NORMAL),
            TextNode('picture', TextType.IMAGE, 'https://image.example.com'),
            TextNode(' and remember to follow ', TextType.NORMAL),
            TextNode('me', TextType.LINK, 'https://me.bsky.app')
        ]
        self.assertEqual(text_to_textnodes(text), expect)
# }}}
    def test_text_to_nodes_mix(self):# {{{
        text = '''A [link](https://example.com) shows an image: ![alt text](https://image.example.com). Run [this code](https://notepad.app/sh) with `bash` or `zsh`: `echo "Hello World" > ~/.hello`'''
        expect = [
            TextNode('A ', TextType.NORMAL),
            TextNode('link', TextType.LINK, 'https://example.com'),
            TextNode(' shows an image: ', TextType.NORMAL),
            TextNode('alt text', TextType.IMAGE, 'https://image.example.com'),
            TextNode('. Run ', TextType.NORMAL),
            TextNode('this code', TextType.LINK, 'https://notepad.app/sh'),
            TextNode(' with ', TextType.NORMAL),
            TextNode('bash', TextType.CODE),
            TextNode(' or ', TextType.NORMAL),
            TextNode('zsh', TextType.CODE),
            TextNode(': ', TextType.NORMAL),
            TextNode('echo "Hello World" > ~/.hello', TextType.CODE)
        ]
        self.assertEqual(text_to_textnodes(text), expect)
# }}}
    def test_text_to_nodes_random_1(self):# {{{
        text = '**Option 1**: [The webi installer](https://webinstall.dev/golang/) is the simplest way for most people. Just run this in your terminal:'
        expect = [
            TextNode('Option 1', TextType.BOLD),
            TextNode(': ', TextType.NORMAL),
            TextNode('The webi installer', TextType.LINK, 'https://webinstall.dev/golang/'),
            TextNode(' is the simplest way for most people. Just run this in your terminal:', TextType.NORMAL)
        ]
        self.assertEqual(text_to_textnodes(text), expect)
# }}}
class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_block_empty(self):# {{{
        markdown = ''
        expect = []
        self.assertEqual(markdown_to_blocks(markdown), expect)
# }}}
    def test_markdown_to_block_simple(self):# {{{
        markdown = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
'''
        expect = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '''* This is the first list item in a list block
* This is a list item
* This is another list item'''
        ]
        #print(markdown_to_blocks(markdown))
        self.assertEqual(markdown_to_blocks(markdown), expect)
# }}}
    def test_markdown_to_block_multiple_blank_lines(self):# {{{
        markdown = '''

# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.



* This is the first list item in a list block
* This is a list item
* This is another list item


'''
        expect = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '''* This is the first list item in a list block
* This is a list item
* This is another list item'''
        ]
        self.assertEqual(markdown_to_blocks(markdown), expect)
# }}}
    def test_markdown_to_block_leading_spaces(self):# {{{
        markdown = '''# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        '''
        expect = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '''* This is the first list item in a list block
* This is a list item
* This is another list item'''
        ]
        self.assertEqual(markdown_to_blocks(markdown), expect)
# }}}
    def test_markdown_to_block_trailing_spaces(self):# {{{
        markdown = '''# This is a heading
         
This is a paragraph of text. It has some **bold** and *italic* words inside of it.       
  
* This is the first list item in a list block          
* This is a list item  
* This is another list item   
        '''
        expect = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '''* This is the first list item in a list block
* This is a list item
* This is another list item'''
        ]
        self.assertEqual(markdown_to_blocks(markdown), expect)
# }}}
class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_htmlnode_simple(self):# {{{
        markdown = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.
A single newline should not break it.

* This is the first list item in a list block
* This is a list item
* This is another list item
'''
        expect = ParentNode('div', [
            ParentNode('h1', [
                LeafNode(None, 'This is a heading'),
            ]),
            ParentNode('p', [
                LeafNode(None, "This is a paragraph of text. It has some "),
                LeafNode('b', "bold"),
                LeafNode(None, " and "),
                LeafNode('i', "italic"),
                LeafNode(None, """ words inside of it.
A single newline should not break it."""),
            ]),
            ParentNode('ul', [
                ParentNode('li', [LeafNode(None, 'This is the first list item in a list block')]),
                ParentNode('li', [LeafNode(None, 'This is a list item')]),
                ParentNode('li', [LeafNode(None, 'This is another list item')]),
            ]),
        ])
        self.assertEqual(repr(markdown_to_htmlnode(markdown)), repr(expect))
# }}}
    def test_markdown_to_htmlnode_ordered_list(self):# {{{
        markdown = '''## Shopping list

1. Eggs
2. Cabbages
3. **Milk**
4. Whisky

## Shopping sites

1. Prism
2. K-supermarket
        '''
        expect = ParentNode('div', [
            ParentNode('h2', [
                LeafNode(None, 'Shopping list'),
            ]),
            ParentNode('ol', [
                ParentNode('li', [LeafNode(None, 'Eggs')]),
                ParentNode('li', [LeafNode(None, 'Cabbages')]),
                ParentNode('li', [LeafNode('b', 'Milk')]),
                ParentNode('li', [LeafNode(None, 'Whisky')]),
            ]),
            ParentNode('h2', [
                LeafNode(None, 'Shopping sites'),
            ]),
            ParentNode('ol', [
                ParentNode('li', [LeafNode(None, 'Prism')]),
                ParentNode('li', [LeafNode(None, 'K-supermarket')]),
            ]),
        ])
        self.assertEqual(repr(markdown_to_htmlnode(markdown)), repr(expect))
# }}}
    def test_markdown_to_htmlnode_code_blocks(self):# {{{
        markdown = '''
```bash
[[ $INSANE ]] && true || false
```

```py
def count_to_100():
    for i in range(100):
        print(i)
```

```
Just some line that is space-preserved
    With things like steps
        Or more
            More indented
        Back out
    Back, again
Make it a curve
```
        '''
        expect = ParentNode('div', [
            ParentNode('pre', [
                ParentNode('code', [
                    LeafNode(None, '[[ $INSANE ]] && true || false'),
                ]),
            ]),
            ParentNode('pre', [
                ParentNode('code', [
                    LeafNode(None, '''def count_to_100():
for i in range(100):
print(i)'''),
                ]),
            ]),
            ParentNode('pre', [
                ParentNode('code', [
                    LeafNode(None, '''Just some line that is space-preserved
With things like steps
Or more
More indented
Back out
Back, again
Make it a curve'''),
                ]),
            ]),
        ])
        self.assertEqual(repr(markdown_to_htmlnode(markdown)), repr(expect))
# }}}
    def test_markdown_to_htmlnode_blockquotes(self):# {{{
        markdown = '''
> A wall of quote
> Written in English
> Supposed to be in these lines, really

> Single line quote

>> More than a level
> Should be normal
'''
        expect = ParentNode('div', [
            ParentNode('blockquote', [
                ParentNode('p', [
                    LeafNode(None, '''A wall of quote
Written in English
Supposed to be in these lines, really'''),
                ]),
            ]),
            ParentNode('blockquote', [
                ParentNode('p', [
                    LeafNode(None, 'Single line quote')
                ]),
            ]),
            ParentNode('blockquote', [
                ParentNode('p', [
                    LeafNode(None, '''More than a level
Should be normal''')
                ]),
            ]),
        ])
        self.assertEqual(repr(markdown_to_htmlnode(markdown)), repr(expect))
# }}}
    def test_markdown_to_htmlnode_invalid_blocks(self):# {{{
        markdown = '''
# No longer a heading
Because there's a line under it.

- No longer a list
en passant
- Because a line ran over

        '''
        expect = ParentNode('div', [
            ParentNode('p', [
                LeafNode(None, """# No longer a heading
Because there's a line under it."""),
            ]),
            ParentNode('p', [
                LeafNode(None, """- No longer a list
en passant
- Because a line ran over"""),
            ]),
        ])
        self.assertEqual(repr(markdown_to_htmlnode(markdown)), repr(expect))
# }}}
    def test_markdown_to_htmlnode_headings(self):# {{{
        markdown = '''
#                        Should still be h1

## level 2

###### level 6
        '''
        expect = ParentNode('div', [
            ParentNode('h1', [LeafNode(None, 'Should still be h1')]),
            ParentNode('h2', [LeafNode(None, 'level 2')]),
            ParentNode('h6', [LeafNode(None, 'level 6')]),
        ])
        self.assertEqual(repr(markdown_to_htmlnode(markdown)), repr(expect))
# }}}
    def test_markdown_to_htmlnode_unordered_list(self):# {{{
        markdown = '''
* Single list item

- Single list item

* List item 1
* List item 2
* List item 3

- List item 1
- List item 2
- List item 3
        '''
        expect = ParentNode('div', [
            ParentNode('ul', [
                ParentNode('li', [LeafNode(None, 'Single list item')]),
            ]),
            ParentNode('ul', [
                ParentNode('li', [LeafNode(None, 'Single list item')]),
            ]),
            ParentNode('ul', [
                ParentNode('li', [LeafNode(None, 'List item 1')]),
                ParentNode('li', [LeafNode(None, 'List item 2')]),
                ParentNode('li', [LeafNode(None, 'List item 3')]),
            ]),
            ParentNode('ul', [
                ParentNode('li', [LeafNode(None, 'List item 1')]),
                ParentNode('li', [LeafNode(None, 'List item 2')]),
                ParentNode('li', [LeafNode(None, 'List item 3')]),
            ]),
        ])
        self.assertEqual(repr(markdown_to_htmlnode(markdown)), repr(expect))# }}}
