from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError('ParentNode must have a tag')
        if not self.children:
            raise ValueError('ParentNode must have children')
        html = ''
        for child in self.children:
            html += child.to_html()
        return f'<{self.tag}>{html}</{self.tag}>'
