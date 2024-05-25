import re

from .leafnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text: str, text_type: str, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.url == other.url
                and self.text == other.text
                and self.text_type == other.text_type
                )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


map = {
    text_type_text: lambda textNode: LeafNode(None, textNode.text),
    text_type_bold: lambda textNode: LeafNode("b", textNode.text),
    text_type_italic: lambda textNode: LeafNode("i", textNode.text),
    text_type_image: lambda textNode: LeafNode("img", "", {"src": textNode.url, "alt": textNode.text}),
    text_type_code: lambda textNode: LeafNode("code", textNode.text, {"href": textNode.url}),
    text_type_link: lambda textNode: LeafNode("a", textNode.text),
}


def text_node_to_html_node(textNode: TextNode) -> LeafNode:
    if textNode.text_type in map:
        return map[textNode.text_type](textNode)


bold_delimiter = '**'
italic_delimiter = '*'
code_delimiter = '`'
text_type_nodes = [text_type_text, text_type_bold, text_type_italic, text_type_code]
delimiter_to_text_type = {
    bold_delimiter: text_type_bold,
    italic_delimiter: text_type_italic,
    code_delimiter: text_type_code
}


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]):
    return split_with_helper_function(old_nodes, text_type_image, extract_markdown_images, "!")


def split_nodes_link(old_nodes):
    return split_with_helper_function(old_nodes, text_type_link, extract_markdown_links)


def text_to_textnodes(text: str):
    node = TextNode(text.strip(), text_type_text)
    nodes = split_nodes_delimiter([node], bold_delimiter, text_type_bold)
    nodes = split_nodes_delimiter(nodes, italic_delimiter, text_type_italic)
    nodes = split_nodes_delimiter(nodes, code_delimiter, text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_with_helper_function(old_nodes: list[TextNode], text_type, splitting_function, spicial_symbod=""):
    new_nodes = []
    for node in old_nodes:
        images = splitting_function(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        text_for_processing = node.text
        for image_tup in images:
            splitted = text_for_processing.split(f"{spicial_symbod}[{image_tup[0]}]({image_tup[1]})", 1)
            if splitted[0] == "":
                new_nodes.append(TextNode(image_tup[0], text_type, image_tup[1]))
                new_nodes.append(TextNode(splitted[1], text_type_text))
                continue
            if splitted[1] == "":
                new_nodes.append(TextNode(splitted[0], text_type_text))
                new_nodes.append(TextNode(image_tup[0], text_type, image_tup[1]))
                continue
            if len(splitting_function(splitted[1])) > 0:
                new_nodes.append(TextNode(splitted[0], text_type_text))
                new_nodes.append(TextNode(image_tup[0], text_type, image_tup[1]))
                text_for_processing = splitted[1]
            else:
                new_nodes.append(TextNode(splitted[0], text_type_text))
                new_nodes.append(TextNode(image_tup[0], text_type, image_tup[1]))
                new_nodes.append(TextNode(splitted[1], text_type_text))
    return new_nodes
