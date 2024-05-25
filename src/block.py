import re

from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.markdown import markdown_to_blocks
from src.parentnode import ParentNode
from src.textnode import text_to_textnodes, text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def block_to_block_type(markdown_block: str):
    if re.search(r"^#{1,6} ", markdown_block):
        return block_type_heading
    if re.search(r"^```", markdown_block) and re.search(r"```$", markdown_block):
        return block_type_code
    lines = markdown_block.splitlines()
    start_char = lines[0][0]
    if len(list((filter(lambda line: line.startswith(start_char), lines)))) == len(lines):
        if start_char == ">":
            return block_type_quote
        if start_char == "*" or start_char == "-":
            return block_type_unordered_list
    if check_ordered_list(lines):
        return block_type_ordered_list
    return block_type_paragraph


def create_paragraph_html_node(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return ParentNode("p", html_nodes)


def create_heading_html_node(block: str) -> HTMLNode:
    heading_level = count_hashes_at_start(block)
    text = block.lstrip("#").strip()
    text_nodes = text_to_textnodes(text)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return ParentNode(f"h{heading_level}", html_nodes)


def create_code_html_node(block: str) -> HTMLNode:
    child = LeafNode("code", block.strip("```"))
    return ParentNode("pre", [child])


def create_quote_html_node(block: str) -> HTMLNode:
    block_lines = block.split("\n")
    children = []
    for block_line in block_lines:
        block_type = block_to_block_type(block_line[1:])
        children.append(convert_to_html(block_line, block_type))
    return ParentNode("blockquote", children)


def create_ordered_list_html_node(block) -> HTMLNode:
    lines = block.splitlines()
    child_nodes = []
    for line in lines:
        text_nodes = text_to_textnodes(line[2:])
        html_nodes = list(map(text_node_to_html_node, text_nodes))
        child_nodes.append(ParentNode("li", html_nodes))
    return ParentNode("ol", child_nodes)


def create_unordered_list_html_node(block) -> HTMLNode:
    lines = block.splitlines()
    child_nodes = []
    for line in lines:
        text_nodes = text_to_textnodes(line[1:])
        html_nodes = list(map(text_node_to_html_node, text_nodes))
        child_nodes.append(ParentNode("li", html_nodes))
    return ParentNode("ul", child_nodes)


def convert_to_html(block, block_type) -> HTMLNode:
    if block_type == block_type_paragraph:
        return create_paragraph_html_node(block)
    if block_type == block_type_heading:
        return create_heading_html_node(block)
    if block_type == block_type_code:
        return create_code_html_node(block)
    if block_type == block_type_quote:
        return create_quote_html_node(block)
    if block_type == block_type_ordered_list:
        return create_ordered_list_html_node(block)
    if block_type == block_type_unordered_list:
        return create_unordered_list_html_node(block)
    raise ValueError(f"Unknown block type {block_type}")


def markdown_to_html_node(markdown)-> HTMLNode:
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        html_block = convert_to_html(block, block_type)
        nodes.append(html_block)
    return ParentNode("div", nodes)


def check_ordered_list(lines: list[str]):
    line_number = 1
    for line in lines:
        if not line.startswith(f"{line_number}."):
            return False
        line_number += 1
    return True


def count_hashes_at_start(s):
    match = re.match(r'^#*', s)
    if match:
        return len(match.group(0))
    return 0
