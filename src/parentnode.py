from .htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        result_html = f"<{self.tag}>"
        for node in self.children:
            result_html +=  node.to_html()
        return result_html + f"</{self.tag}>"
