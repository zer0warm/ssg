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
        text = node.text
        old_delim = ''
        while True:
            left, delim, right = text.partition(delimiter)
            if delim == '' and right == '':
                if left:
                    splitted.append(TextNode(left, TextType.NORMAL))
                break
            if left:
                if not right:
                    splitted.append(TextNode(left, text_type))
                elif old_delim == '' and (delimiter not in right):
                    raise Exception(f'invalid: unclosed {delimiter} detected')
                elif old_delim:
                    old_delim = ''
                    splitted.append(TextNode(left, text_type))
                else:
                    old_delim = delim
                    splitted.append(TextNode(left, TextType.NORMAL))
            else:
                old_delim = delim
            text = right
    return splitted

def extract_markdown_links(text):
    regex = r'(?<!!)\[([^]]*?)\]\(([^)]*?)\)'
    links = re.findall(regex, text)
    return links

def extract_markdown_images(text):
    regex = r'!\[([^]]*?)\]\(([^)]*?)\)'
    images = re.findall(regex, text)
    return images

def split_nodes_image(nodes):
    splitted = []
    for node in nodes:
        if node.text_type != 'normal':
            splitted.append(node)
            continue
        regex = r'!\[[^]]*?\]\([^)]*?\)'
        images = extract_markdown_images(node.text)
        for part in re.split(regex, node.text):
            if part != '':
                splitted.append(TextNode(part, TextType.NORMAL))
            if images:
                alt, src = images.pop(0)
                splitted.append(TextNode(alt, TextType.IMAGE, src))
    return splitted

def split_nodes_link(nodes):
    splitted = []
    for node in nodes:
        if node.text_type != 'normal':
            splitted.append(node)
            continue
        regex = r'(?<!!)\[[^]]*?\]\([^)]*?\)'
        links = extract_markdown_links(node.text)
        for part in re.split(regex, node.text):
            if part != '':
                splitted.append(TextNode(part, TextType.NORMAL))
            if links:
                value, href = links.pop(0)
                splitted.append(TextNode(value, TextType.LINK, href))
    return splitted

def text_to_textnodes(text):
    return split_nodes_image(
        split_nodes_link(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([TextNode(text, TextType.NORMAL)],
                                          '**', TextType.BOLD),
                    '*', TextType.ITALIC),
                '`', TextType.CODE)))

def markdown_to_blocks(markdown):
    blocks = []
    lines = markdown.split('\n')
    # strip leading and trailing spaces of lines
    lines = list(map(str.strip, lines))
    is_new_block = False
    current_block = ''
    for line in lines:
        if line:
            if is_new_block:
                if current_block:
                    blocks.append(current_block)
                is_new_block = False
                current_block = ''
            if current_block:
                current_block = '\n'.join([current_block, line])
            else:
                current_block = line
        else:
            is_new_block = True
    else:
        if current_block:
            blocks.append(current_block)
    return blocks
