import re

from leafnode import LeafNode
from textnode import TextNode, TextType

def textnode_to_htmlnode(text_node):
    typ = text_node.text_type
    if typ == 'normal':
        return LeafNode(None, text_node.text)
    elif typ == 'bold':
        return LeafNode('b', text_node.text)
    elif typ == 'italic':
        return LeafNode('i', text_node.text)
    elif typ == 'code':
        return LeafNode('code', text_node.text)
    elif typ == 'link':
        return LeafNode('a', text_node.text,
                        props={'href': text_node.url})
    elif typ == 'image':
        return LeafNode('img', None,
                        props={'src': text_node.url,
                               'alt': text_node.text})
    raise ValueError(f'invalid text type {typ}')

def split_nodes_delimiter(nodes, delimiter, text_type):
    splitted = []
    for node in nodes:
        if node.text_type != 'normal':
            splitted.append(node)
            continue
        if node.text.count(delimiter) % 2 == 1:
            raise Exception(f'invalid: unclosed {delimiter} detected')
        if delimiter not in node.text:
            splitted.append(node)
        else:
            for part in node.text.split(delimiter):
                if part == '':
                    continue
                elif part.startswith(' ') or part.endswith(' '):
                    splitted.append(TextNode(part, TextType.NORMAL))
                else:
                    splitted.append(TextNode(part, text_type))
    return splitted

def extract_markdown_links(text):
    regex = r'(?<!!)\[([^]]*?)\]\(([^)]*?)\)'
    links = re.findall(regex, text)
    return links

def extract_markdown_images(text):
    regex = r'!\[([^]]*?)\]\(([^)]*?)\)'
    images = re.findall(regex, text)
    return images
