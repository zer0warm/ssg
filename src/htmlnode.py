class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            return ' '.join(
                [f'{key}="{val}"' for key,val in self.props.items()])
        return ''

    def __repr__(self):
        r_tag = f'tag="{self.tag}"' if self.tag else "tag=None"
        r_value = f'value="{self.value}"' if self.value else "value=None"
        r_children = 'children=' + (repr(self.children) if self.children else '[]')
        r_props = 'props=' + (repr(self.props) if self.props else '{}')
        return f'HTMLNode({r_tag}, {r_value}, {r_children}, {r_props})'
