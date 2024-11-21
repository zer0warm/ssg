import unittest

from textnode import TextNode, TextType
from transformers import (
    textnode_to_htmlnode,
    text_to_textnodes,
    markdown_to_blocks
)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_convert_normal_text(self):
        tn = TextNode('A wild text displayed', TextType.NORMAL)
        Ln = textnode_to_htmlnode(tn)
        self.assertIs(Ln.tag, None)
        self.assertIs(Ln.props, None)
        self.assertEqual(Ln.value, 'A wild text displayed')
        self.assertEqual(Ln.to_html(), 'A wild text displayed')

    def test_convert_bold_text(self):
        tn = TextNode('Bold of text to assume success', TextType.BOLD)
        Ln = textnode_to_htmlnode(tn)
        self.assertIs(Ln.props, None)
        self.assertEqual(Ln.tag, 'b')
        self.assertEqual(Ln.value, 'Bold of text to assume success')
        self.assertEqual(Ln.to_html(), '<b>Bold of text to assume success</b>')

    def test_convert_italic_text(self):
        tn = TextNode('Have some Pisa in Italic', TextType.ITALIC)
        Ln = textnode_to_htmlnode(tn)
        self.assertIs(Ln.props, None)
        self.assertEqual(Ln.tag, 'i')
        self.assertEqual(Ln.value, 'Have some Pisa in Italic')
        self.assertEqual(Ln.to_html(), '<i>Have some Pisa in Italic</i>')

    def test_convert_code_text(self):
        tn = TextNode('print("Hello, world!")', TextType.CODE)
        Ln = textnode_to_htmlnode(tn)
        self.assertIs(Ln.props, None)
        self.assertEqual(Ln.tag, 'code')
        self.assertEqual(Ln.value, 'print("Hello, world!")')
        self.assertEqual(Ln.to_html(), '<code>print("Hello, world!")</code>')

    def test_convert_link_text(self):
        tn = TextNode('Link start!', TextType.LINK,
                      'https://www.swordart-online.net/')
        Ln = textnode_to_htmlnode(tn)
        self.assertEqual(Ln.props,
                         {'href': 'https://www.swordart-online.net/'})
        self.assertEqual(Ln.tag, 'a')
        self.assertEqual(Ln.value, 'Link start!')
        html = '<a href="https://www.swordart-online.net/">Link start!</a>'
        self.assertEqual(Ln.to_html(), html)

    def test_convert_image_text_example(self):
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

    @unittest.skip("currently unreachable")
    def test_convert_malfunc_text(self):
        tn = TextNode('Invalid node', 'invalid', 'url://point.to.nowhere')
        self.assertRaisesRegex(ValueError, 'invalid text type "invalid"',
                               textnode_to_htmlnode, tn)

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_nodes_only_non_links(self):
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

    def test_text_to_nodes_only_links(self):
        text = ('Come see this ![picture](https://image.example.com)' +
                ' and remember to follow [me](https://me.bsky.app)')
        expect = [
            TextNode('Come see this ', TextType.NORMAL),
            TextNode('picture', TextType.IMAGE, 'https://image.example.com'),
            TextNode(' and remember to follow ', TextType.NORMAL),
            TextNode('me', TextType.LINK, 'https://me.bsky.app')
        ]
        self.assertEqual(text_to_textnodes(text), expect)

    def test_text_to_nodes_mix(self):
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

    def test_text_to_nodes_random_1(self):
        text = '**Option 1**: [The webi installer](https://webinstall.dev/golang/) is the simplest way for most people. Just run this in your terminal:'
        expect = [
            TextNode('Option 1', TextType.BOLD),
            TextNode(': ', TextType.NORMAL),
            TextNode('The webi installer', TextType.LINK, 'https://webinstall.dev/golang/'),
            TextNode(' is the simplest way for most people. Just run this in your terminal:', TextType.NORMAL)
        ]
        self.assertEqual(text_to_textnodes(text), expect)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_block_empty(self):
        markdown = ''
        expect = []
        self.assertEqual(markdown_to_blocks(markdown), expect)

    def test_markdown_to_block_simple(self):
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

    def test_markdown_to_block_multiple_blank_lines(self):
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

    def test_markdown_to_block_leading_spaces(self):
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

    def test_markdown_to_block_trailing_spaces(self):
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
