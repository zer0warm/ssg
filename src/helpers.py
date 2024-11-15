from leafnode import LeafNode

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
