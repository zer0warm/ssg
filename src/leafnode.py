from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    # TODO: Add support for void elements
    # TODO: Escape HTML entities in values
    # TODO: Check if tag is valid HTML element
    def to_html(self):
        if not self.value:
            raise ValueError('LeafNode object must have a value')
        if not self.tag:
            return f'{self.value}'
        return f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>'
