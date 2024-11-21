from leafnode import LeafNode
from textnode import TextNode, TextType
from helpers import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link
)

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
