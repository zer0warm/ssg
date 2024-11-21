import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType
from helpers import (
    textnode_to_htmlnode,
    split_nodes_delimiter,
    extract_markdown_links, extract_markdown_images,
    split_nodes_image, split_nodes_link,
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

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_bold(self):
        nodes = [TextNode('Bold of **text** to assume success', TextType.NORMAL)]
        splitted = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        expect = [
            TextNode('Bold of ', TextType.NORMAL),
            TextNode('text', TextType.BOLD),
            TextNode(' to assume success', TextType.NORMAL)
        ]
        self.assertEqual(splitted, expect)

    def test_split_bold_start(self):
        nodes = [TextNode('**Bold** of text to assume success', TextType.NORMAL)]
        splitted = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        expect = [
            TextNode('Bold', TextType.BOLD),
            TextNode(' of text to assume success', TextType.NORMAL)
        ]
        self.assertEqual(splitted, expect)

    def test_split_bold_end(self):
        nodes = [TextNode('Bold of text to assume **success**', TextType.NORMAL)]
        splitted = split_nodes_delimiter(nodes, '**', TextType.BOLD)
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
        splitted = split_nodes_delimiter(nodes, '**', TextType.BOLD)
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
                               split_nodes_delimiter, nodes, '**', TextType.BOLD)

    def test_split_italic_multi(self):
        nodes = [
            TextNode('Have *a Pisa* in `Italic`? You meant `Bold`?',
                     TextType.NORMAL),
            TextNode('should not convert this part', TextType.NORMAL),
            TextNode('should still be bold', TextType.BOLD),
            TextNode('Italic', TextType.CODE)
        ]
        splitted = split_nodes_delimiter(nodes, '*', TextType.ITALIC)
        expect = [
            TextNode('Have ', TextType.NORMAL),
            TextNode('a Pisa', TextType.ITALIC),
            TextNode(' in `Italic`? You meant `Bold`?', TextType.NORMAL),
            TextNode('should not convert this part', TextType.NORMAL),
            TextNode('should still be bold', TextType.BOLD),
            TextNode('Italic', TextType.CODE)
        ]
        self.assertEqual(splitted, expect)

class TestExtractMarkdownLink(unittest.TestCase):
    def test_extract_links_single(self):
        text = 'Visit [GitHub](https://github.com).'
        links = extract_markdown_links(text)
        expect = [("GitHub", "https://github.com")]
        self.assertEqual(links, expect)

    def test_extract_links_multiple(self):
        text = '''Platforms hosting Git repositories including
        [GitHub](https://github.com) and [GitLab](https://gitlab.com)'''
        links = extract_markdown_links(text)
        expect = [
            ("GitHub", "https://github.com"),
            ("GitLab", "https://gitlab.com")
        ]
        self.assertEqual(links, expect)

    def test_extract_links_in_junction(self):
        text = '''This is a [line] with a lot of (fix: many) <brackets>. The
        point is to [test](https://linux.die.net/man/1/test) whether the system
        can <<extract>> properly.'''
        expect = [("test", "https://linux.die.net/man/1/test")]
        links = extract_markdown_links(text)
        self.assertEqual(links, expect)

    def test_extract_links_among_images(self):
        text = '''[A link](https://example.com) vs. ![An image](https://image.example.com)'''
        expect = [("A link", "https://example.com")]
        links = extract_markdown_links(text)
        self.assertEqual(links, expect)

    def test_extract_links_empty(self):
        text = 'This is a valid markdown. []() is an empty link'
        expect = [("", "")]
        links = extract_markdown_links(text)
        self.assertEqual(links, expect)

class TestExtractMarkdownImage(unittest.TestCase):
    def test_extract_image(self):
        text = 'Check out: ![an example image](https://example.com/img)'
        imgs = extract_markdown_images(text)
        expect = [("an example image", "https://example.com/img")]
        self.assertEqual(imgs, expect)

    def test_extract_image_with_links(self):
        text = '''[A link](https://example.com) vs. ![An image](https://image.example.com)'''
        expect = [("An image", "https://image.example.com")]
        imgs = extract_markdown_images(text)
        self.assertEqual(imgs, expect)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_image_end(self):
        nodes = [TextNode('An image ![example img](https://image.example.com)', TextType.NORMAL)]
        expect = [
            TextNode('An image ', TextType.NORMAL),
            TextNode('example img', TextType.IMAGE, 'https://image.example.com')
        ]
        self.assertEqual(split_nodes_image(nodes), expect)

    def test_split_image_start(self):
        nodes = [TextNode('![example img](https://image.example.com) as an example', TextType.NORMAL)]
        expect = [
            TextNode('example img', TextType.IMAGE, 'https://image.example.com'),
            TextNode(' as an example', TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_image(nodes), expect)

    def test_split_image_standalone(self):
        nodes = [TextNode('![example img](https://image.example.com)', TextType.NORMAL)]
        expect = [
            TextNode('example img', TextType.IMAGE, 'https://image.example.com')
        ]
        self.assertEqual(split_nodes_image(nodes), expect)

    def test_split_image_no_image(self):
        nodes = [
            TextNode('A line of normal text', TextType.NORMAL),
            TextNode('A line of **bold** text', TextType.NORMAL),
            TextNode('Link', TextType.LINK, 'https://example.com'),
            TextNode('bash', TextType.CODE)
        ]
        expect = nodes.copy()
        self.assertEqual(split_nodes_image(nodes), expect)

    def test_split_image_multiple(self):
        nodes = [
            TextNode('Here is an image of a cat', TextType.NORMAL),
            TextNode('![orange cat](https://orange-cat.example.com)', TextType.NORMAL),
            TextNode('Here is mine ![black cat](https://bc.example.com)', TextType.NORMAL)
        ]
        expect = [
            TextNode('Here is an image of a cat', TextType.NORMAL),
            TextNode('orange cat', TextType.IMAGE, 'https://orange-cat.example.com'),
            TextNode('Here is mine ', TextType.NORMAL),
            TextNode('black cat', TextType.IMAGE, 'https://bc.example.com')
        ]
        self.assertEqual(split_nodes_image(nodes), expect)

    def test_split_image_among_links(self):
        nodes = [
            TextNode('![image one](https://i1.example.com) and' +
                     ' [GitHub](https://github.com).' +
                     ' ![image two](https://i2.example.com),' +
                     ' ![image three](https://i3.example.com).' +
                     ' [Sourcehut](https://sourcehut.org) is preferred.' +
                     ' ![image four](https://i4.example.com)', TextType.NORMAL)
        ]
        expect = [
            TextNode('image one', TextType.IMAGE, 'https://i1.example.com'),
            TextNode(' and [GitHub](https://github.com). ', TextType.NORMAL),
            TextNode('image two', TextType.IMAGE, 'https://i2.example.com'),
            TextNode(', ', TextType.NORMAL),
            TextNode('image three', TextType.IMAGE, 'https://i3.example.com'),
            TextNode('. [Sourcehut](https://sourcehut.org) is preferred. ', TextType.NORMAL),
            TextNode('image four', TextType.IMAGE, 'https://i4.example.com')
        ]
        self.maxDiff = None
        self.assertEqual(split_nodes_image(nodes), expect)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_link_single(self):
        nodes = [TextNode('[link name](http://link.url)', TextType.NORMAL)]
        expect = [
            TextNode('link name', TextType.LINK, 'http://link.url')
        ]
        self.assertEqual(split_nodes_link(nodes), expect)

    def test_split_link_multiple_text_single(self):
        nodes = [
            TextNode('[link 1](https://1.link.url) and ' +
                     '[link 2](https://2.link.url). ' +
                     '[link 3](https://3.link.url)', TextType.NORMAL)
        ]
        expect = [
            TextNode('link 1', TextType.LINK, 'https://1.link.url'),
            TextNode(' and ', TextType.NORMAL),
            TextNode('link 2', TextType.LINK, 'https://2.link.url'),
            TextNode('. ', TextType.NORMAL),
            TextNode('link 3', TextType.LINK, 'https://3.link.url'),
        ]
        self.assertEqual(split_nodes_link(nodes), expect)

    def test_split_link_multiple_text_multiple(self):
        nodes = [
            TextNode('First, a single line.', TextType.NORMAL),
            TextNode('Then a link [example](https://example.com)', TextType.NORMAL),
            TextNode('This sentence is in bold', TextType.BOLD),
            TextNode('I heard you like [skribbl](https://skribbl.io)?', TextType.NORMAL),
            TextNode('Bootdotdev', TextType.LINK, 'https://linkedin.com/bootdotdev'),
            TextNode('Finally, a dot.', TextType.NORMAL)
        ]
        expect = [
            TextNode('First, a single line.', TextType.NORMAL),
            TextNode('Then a link ', TextType.NORMAL),
            TextNode('example', TextType.LINK, 'https://example.com'),
            TextNode('This sentence is in bold', TextType.BOLD),
            TextNode('I heard you like ', TextType.NORMAL),
            TextNode('skribbl', TextType.LINK, 'https://skribbl.io'),
            TextNode('?', TextType.NORMAL),
            TextNode('Bootdotdev', TextType.LINK, 'https://linkedin.com/bootdotdev'),
            TextNode('Finally, a dot.', TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_link(nodes), expect)

    def test_split_link_empty(self):
        nodes = [
            TextNode('[]()', TextType.NORMAL),
            TextNode('[without link]()', TextType.NORMAL),
            TextNode('[](without name)', TextType.NORMAL)
        ]
        expect = [
            TextNode('', TextType.LINK, ''),
            TextNode('without link', TextType.LINK, ''),
            TextNode('', TextType.LINK, 'without name')
        ]
        self.assertEqual(split_nodes_link(nodes), expect)

    def test_split_link_no_link(self):
        nodes = [
            TextNode('A line of normal text', TextType.NORMAL),
            TextNode('A line of **bold** text', TextType.NORMAL),
            TextNode('Link', TextType.LINK, 'https://example.com'),
            TextNode('bash', TextType.CODE)
        ]
        expect = nodes.copy()
        self.assertEqual(split_nodes_link(nodes), expect)

    def test_split_link_among_images(self):
        nodes = [
            TextNode('[Hello](mailto:hello@boot.dev), you\'ve stumbled' +
                     ' upon ![pokemon image](http://po.ke.mon)' +
                     ' and witness ![orange cat](http://random.cat).' +
                     ' Remember to feed back in our' +
                     ' [repo](github.com/zer0warm/jibberish)',
                     TextType.NORMAL)
        ]
        expect = [
            TextNode('Hello', TextType.LINK, 'mailto:hello@boot.dev'),
            TextNode(', you\'ve stumbled upon' +
                     ' ![pokemon image](http://po.ke.mon) and witness' +
                     ' ![orange cat](http://random.cat). Remember to' +
                     ' feed back in our ', TextType.NORMAL),
            TextNode('repo', TextType.LINK, 'github.com/zer0warm/jibberish')
        ]
        self.assertEqual(split_nodes_link(nodes), expect)

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

if __name__ == '__main__':
    unittest.main()
