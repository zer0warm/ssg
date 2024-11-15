from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    # Source: https://developer.mozilla.org/en-US/docs/Glossary/Void_element
    void_elements = ('br', 'hr', 'img')

    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    # TODO: Escape HTML entities in values
    # TODO: Check if tag is valid HTML element
    def to_html(self):
        if not self.tag:
            return f'{self.value}'
        if self.tag in LeafNode.void_elements:
            if not self.props:
                return f'<{self.tag}>'
            return f'<{self.tag} {self.props_to_html()}>'
        if not self.value:
            raise ValueError('LeafNode object must have a value')
        if not self.props:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        return f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>'
