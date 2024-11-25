from leafnode import LeafNode
from textnode import TextNode, TextType
from parentnode import ParentNode
from helpers import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    block_to_block_type
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

def markdown_to_htmlnode(markdown):
    block_type_transformers = {
        'paragraph':      block_to_paragraph,
        'heading':        block_to_heading,
        'quote':          block_to_quote,
        'unordered_list': block_to_unordered_list,
        'ordered_list':   block_to_ordered_list,
        'code':           block_to_code
    }
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        typ = block_to_block_type(block)
        transformer = block_type_transformers[typ]
        children.append(transformer(block))
    return ParentNode('div', children)

def text_to_children(text):
    textnodes = text_to_textnodes(text.lstrip())
    children = list(map(lambda n: textnode_to_htmlnode(n), textnodes))
    return children

def block_to_paragraph(block):
    lines = block.split('\n')
    children = []
    for line in lines:
        children.extend(text_to_children(line))
    return ParentNode('p', text_to_children(block))

def block_to_heading(block):
    marker, *rest = block.split(' ')
    level = len(marker)
    return ParentNode(f'h{level}', text_to_children(' '.join(rest)))

def block_to_quote(block):
    block = '\n'.join([line.lstrip('> ') for line in block.split('\n')])
    return ParentNode('blockquote', [
        ParentNode('p', text_to_children(block))
    ])

def block_to_list_item(block):
    # slice the list item marker away
    item_text = ' '.join(block.split(' ')[1:])
    return ParentNode('li', text_to_children(item_text))

def block_to_unordered_list(block):
    children = []
    items = block.split('\n')
    for item_block in items:
        children.append(block_to_list_item(item_block))
    return ParentNode('ul', children)

def block_to_ordered_list(block):
    children = []
    items = block.split('\n')
    for item_block in items:
        children.append(block_to_list_item(item_block))
    return ParentNode('ol', children)

def block_to_code(block):
    # remove the first backticks line and last backticks line
    code_block = '\n'.join(block.split('\n')[1:-1])
    node = ParentNode('pre', [
        ParentNode('code', [LeafNode(None, code_block)])
    ])
    return node
