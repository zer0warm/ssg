import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType
from helpers import (
    split_nodes_delimiter,
    extract_markdown_links, extract_markdown_images,
    split_nodes_image, split_nodes_link,
    block_to_block_type,
    extract_title
)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_bold(self):# {{{
        nodes = [TextNode('Bold of **text** to assume success', TextType.NORMAL)]
        splitted = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        expect = [
            TextNode('Bold of ', TextType.NORMAL),
            TextNode('text', TextType.BOLD),
            TextNode(' to assume success', TextType.NORMAL)
        ]
        self.assertEqual(splitted, expect)
# }}}
    def test_split_bold_start(self):# {{{
        nodes = [TextNode('**Bold** of text to assume success', TextType.NORMAL)]
        splitted = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        expect = [
            TextNode('Bold', TextType.BOLD),
            TextNode(' of text to assume success', TextType.NORMAL)
        ]
        self.assertEqual(splitted, expect)
# }}}
    def test_split_bold_end(self):# {{{
        nodes = [TextNode('Bold of text to assume **success**', TextType.NORMAL)]
        splitted = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        expect = [
            TextNode('Bold of text to assume ', TextType.NORMAL),
            TextNode('success', TextType.BOLD)
        ]
        self.assertEqual(splitted, expect)
# }}}
    def test_split_bold_multi(self):# {{{
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
# }}}
    def test_split_bold_uneven(self):# {{{
        nodes = [TextNode('Bold of **text to assume success', TextType.NORMAL)]
        self.assertRaisesRegex(Exception, 'invalid',
                               split_nodes_delimiter, nodes, '**', TextType.BOLD)
# }}}
    def test_split_italic_multi(self):# {{{
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
# }}}
class TestExtractMarkdownLink(unittest.TestCase):
    def test_extract_links_single(self):# {{{
        text = 'Visit [GitHub](https://github.com).'
        links = extract_markdown_links(text)
        expect = [("GitHub", "https://github.com")]
        self.assertEqual(links, expect)
# }}}
    def test_extract_links_multiple(self):# {{{
        text = '''Platforms hosting Git repositories including
        [GitHub](https://github.com) and [GitLab](https://gitlab.com)'''
        links = extract_markdown_links(text)
        expect = [
            ("GitHub", "https://github.com"),
            ("GitLab", "https://gitlab.com")
        ]
        self.assertEqual(links, expect)
# }}}
    def test_extract_links_in_junction(self):# {{{
        text = '''This is a [line] with a lot of (fix: many) <brackets>. The
        point is to [test](https://linux.die.net/man/1/test) whether the system
        can <<extract>> properly.'''
        expect = [("test", "https://linux.die.net/man/1/test")]
        links = extract_markdown_links(text)
        self.assertEqual(links, expect)
# }}}
    def test_extract_links_among_images(self):# {{{
        text = '''[A link](https://example.com) vs. ![An image](https://image.example.com)'''
        expect = [("A link", "https://example.com")]
        links = extract_markdown_links(text)
        self.assertEqual(links, expect)
# }}}
    def test_extract_links_empty(self):# {{{
        text = 'This is a valid markdown. []() is an empty link'
        expect = [("", "")]
        links = extract_markdown_links(text)
        self.assertEqual(links, expect)
# }}}
class TestExtractMarkdownImage(unittest.TestCase):
    def test_extract_image(self):# {{{
        text = 'Check out: ![an example image](https://example.com/img)'
        imgs = extract_markdown_images(text)
        expect = [("an example image", "https://example.com/img")]
        self.assertEqual(imgs, expect)
# }}}
    def test_extract_image_with_links(self):# {{{
        text = '''[A link](https://example.com) vs. ![An image](https://image.example.com)'''
        expect = [("An image", "https://image.example.com")]
        imgs = extract_markdown_images(text)
        self.assertEqual(imgs, expect)
# }}}
class TestSplitNodesImage(unittest.TestCase):
    def test_split_image_end(self):# {{{
        nodes = [TextNode('An image ![example img](https://image.example.com)', TextType.NORMAL)]
        expect = [
            TextNode('An image ', TextType.NORMAL),
            TextNode('example img', TextType.IMAGE, 'https://image.example.com')
        ]
        self.assertEqual(split_nodes_image(nodes), expect)
# }}}
    def test_split_image_start(self):# {{{
        nodes = [TextNode('![example img](https://image.example.com) as an example', TextType.NORMAL)]
        expect = [
            TextNode('example img', TextType.IMAGE, 'https://image.example.com'),
            TextNode(' as an example', TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_image(nodes), expect)
# }}}
    def test_split_image_standalone(self):# {{{
        nodes = [TextNode('![example img](https://image.example.com)', TextType.NORMAL)]
        expect = [
            TextNode('example img', TextType.IMAGE, 'https://image.example.com')
        ]
        self.assertEqual(split_nodes_image(nodes), expect)
# }}}
    def test_split_image_no_image(self):# {{{
        nodes = [
            TextNode('A line of normal text', TextType.NORMAL),
            TextNode('A line of **bold** text', TextType.NORMAL),
            TextNode('Link', TextType.LINK, 'https://example.com'),
            TextNode('bash', TextType.CODE)
        ]
        expect = nodes.copy()
        self.assertEqual(split_nodes_image(nodes), expect)
# }}}
    def test_split_image_multiple(self):# {{{
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
# }}}
    def test_split_image_among_links(self):# {{{
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
# }}}
class TestSplitNodesLink(unittest.TestCase):
    def test_split_link_single(self):# {{{
        nodes = [TextNode('[link name](http://link.url)', TextType.NORMAL)]
        expect = [
            TextNode('link name', TextType.LINK, 'http://link.url')
        ]
        self.assertEqual(split_nodes_link(nodes), expect)
# }}}
    def test_split_link_multiple_text_single(self):# {{{
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
# }}}
    def test_split_link_multiple_text_multiple(self):# {{{
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
# }}}
    def test_split_link_empty(self):# {{{
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
# }}}
    def test_split_link_no_link(self):# {{{
        nodes = [
            TextNode('A line of normal text', TextType.NORMAL),
            TextNode('A line of **bold** text', TextType.NORMAL),
            TextNode('Link', TextType.LINK, 'https://example.com'),
            TextNode('bash', TextType.CODE)
        ]
        expect = nodes.copy()
        self.assertEqual(split_nodes_link(nodes), expect)
# }}}
    def test_split_link_among_images(self):# {{{
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
# }}}
class TestBlockToBlockType(unittest.TestCase):
    def test_block_type_p(self):# {{{
        block = 'This is a paragraph. Watch out for **bold** or *italic* text. Inline `code` too.'
        self.assertEqual(block_to_block_type(block), 'paragraph')
# }}}
    def test_block_type_p_invalid_heading(self):# {{{
        blocks = [
            '#This is not a heading',
            '################ too many octothorpes',
            '####### This is not a heading',
            '= Heading, but in AsciiDoc',
            '''Same but in RST
===============''',
            '''# Supposed heading
But followed by a line.'''
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), 'paragraph')
# }}}
    def test_block_type_p_invalid_code(self):# {{{
        blocks = [
            """```Code in here
ThenCode
ButNoClosing""",
            """```
Usual code
But no closing, either
""",
            """Normal text runs
Then suddenly a code block
```bash
:(){:|:&}:
```""",
            """Over-deleting the start
of a code block
```"""
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), 'paragraph')
# }}}
    def test_block_type_p_invalid_quote(self):# {{{
        blocks = [
            '''>In a quote
>Like this
But suddenly not quote''',
            '''Not having blank line between this paragraph
>And the quote
>Like this''',
            '''* List then
* List next
> Then quote
> Like this'''
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), 'paragraph')
# }}}
    def test_block_type_p_invalid_unordered_list(self):# {{{
        blocks = [
            '-list item without space',
            '*list item without space',

'''- List item 1
- List item 2
No longer list item
With these two''',

'''en passant
- List item 1
- List item 2''',

'''- List item 1
en passant
- List item 2''',

'''- Mix list item marker
* With asterisk
- Then back to this one''',

'''* List item
en passant
* Another list item''',

"""en passant
* List item 1
* List item 2""",

"""- Dash list item 1
- Dash list item 2
en passant"""
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), 'paragraph')
# }}}
    def test_block_type_p_invalid_ordered_list(self):# {{{
        blocks = [
            '2. Why start with 1?',
            '0. Again, are we not computer scientists?',

"""2. Apple
3. Orange""",

"""1. Fruit
2. Sushi
en passant
3. Alexander""",

"""1. Order #4096
2. Order #16384
en passant""",
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), 'paragraph')
# }}}
    def test_block_type_heading(self):# {{{
        blocks = [
            '# This is a heading',
            '##     This is h2',
            '###   This is h3',
            '#### This is h4',
            '##### This is h5',
            '###### This is h6',
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), 'heading')
# }}}
    def test_block_type_code(self):# {{{
        blocks = [
            """```
This is just a block of code font.
With no actual code.
```""",
            """```py
# python code is only special when there's js
print('Hello, world')
```""",
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), 'code')
# }}}
    def test_block_type_quote(self):# {{{
        blocks = [
            '> Single line quote',
            '>Single line quote without space',
            '''> Double line
> Quote''',
            '''> If it's on the Internet
>It must be true.
>Especially when cited to Albert Einstein.'''
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), 'quote')
# }}}
    def test_block_type_unordered_list(self):# {{{
        blocks = [
            '* List item asterisk',
            '- List item dash',
            '''* List item asterisk 1
* List item asterisk 2
* List item asterisk 3''',
            '''- List item dash 1
- List item dash 2'''
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), 'unordered_list')
# }}}
    def test_block_type_ordered_list(self):# {{{
        blocks = [
            '1. List item single',
            '''1. List item 1
2. List item 2
3. List item 3'''
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), 'ordered_list')
# }}}
class TestExtractTitle(unittest.TestCase):
    def test_extract_title_single(self):# {{{
        markdown = '# Hello world'
        expect = 'Hello world'
        self.assertEqual(extract_title(markdown), expect)
# }}}
    def test_extract_title_document(self):# {{{
        markdown = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.
A single newline should not break it.

* This is the first list item in a list block
* This is a list item
* This is another list item
'''
        expect = 'This is a heading'
        self.assertEqual(extract_title(markdown), expect)
# }}}
    def test_extract_title_leading_spaces(self):# {{{
        markdown = '''#            Title
Lorem ispum. Honestly I'm too lazy to look the full string.

Signature.
        '''
        expect = 'Title'
        self.assertEqual(extract_title(markdown), expect)
# }}}
    def test_extract_title_more_than_one(self):# {{{
        markdown = '''Some heading line
        another
# This is the real title
        and then
# BREAK NEWS: THIS WORKS

# ANOTHER NEWS'''
        expect = 'This is the real title'
        self.assertEqual(extract_title(markdown), expect)
# }}}
    def test_extract_title_no_title(self):# {{{
        markdown = '''
## About

Should be a short text describing what the product is about.

## Contacts

hello@example.com
-Infinity Street.'''
        self.assertRaises(Exception, extract_title, markdown)
# }}}
if __name__ == '__main__':
    unittest.main()
