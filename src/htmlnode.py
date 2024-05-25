class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag: str = tag
        self.value: str = value
        self.children: list[HTMLNode] = children
        self.props: dict = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        attributes = []
        for key, value in self.props.items():
            attributes.append(f'{key}="{value}"')
        return " " + " ".join(attributes)

    def __repr__(self):
        return f"HTMLNode: tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}"


