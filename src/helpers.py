import re

from leafnode import LeafNode
from textnode import TextNode, TextType

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

def block_to_block_type(block):
    lines = block.split('\n')
    if len(lines) == 1 and re.match(r'#{1,6} ', lines[0]):
        return 'heading'
    if (all(map(lambda L: L.startswith('- '), lines)) or
        all(map(lambda L: L.startswith('* '), lines))):
        return 'unordered_list'
    if all(map(lambda L: L.startswith('>'), lines)):
        return 'quote'
    if len(lines) >= 2 and (lines[0].startswith('```') and
                            lines[-1] == '```'):
        return 'code'
    numbers = list(map(lambda L: re.match(r'(\d+)\.', L), lines))
    if all(numbers):
        orders = list(map(lambda m: int(m.groups()[0]), numbers))
        if orders == list(range(1, int(orders[-1])+1)):
            return 'ordered_list'
    return 'paragraph'

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if re.match(r'#{1} ', line):
            return line.lstrip('# ')
    raise Exception('No title found')
