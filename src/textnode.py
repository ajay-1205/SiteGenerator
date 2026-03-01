from enum import Enum
from htmlnode import LeafNode
import textwrap
from Blocknode import BlockType, block_to_block_type
from htmlnode import *
from Text_delimiter import *
from models import *

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception("Unknown text type")




def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []

    for block in blocks:
        # Remove common indentation
        dedented = textwrap.dedent(block).strip()

        if dedented != "":
            cleaned_blocks.append(dedented)

    return cleaned_blocks

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    lines = block.split("\n")

    # PARAGRAPH
    if block_type == BlockType.PARAGRAPH:
        return ParentNode(
            "p",
            text_to_children(block.replace("\n", " "))
        )

    # HEADING
    if block_type == BlockType.HEADING:
        level = len(block.split(" ")[0])
        text = block[level + 1:]
        return ParentNode(
            f"h{level}",
            text_to_children(text)
        )

    # CODE
    if block_type == BlockType.CODE:
        # remove ``` wrapper
        content = block[3:-3].strip("\n")
        code_node = LeafNode("code", content)
        return ParentNode("pre", [code_node])

    # QUOTE
    if block_type == BlockType.QUOTE:
        cleaned = "\n".join(line[1:].strip() for line in lines)
        return ParentNode(
            "blockquote",
            text_to_children(cleaned)
        )

    # UNORDERED LIST
    if block_type == BlockType.UNORDERED_LIST:
        items = []
        for line in lines:
            text = line[2:]
            items.append(
                ParentNode("li", text_to_children(text))
            )
        return ParentNode("ul", items)

    # ORDERED LIST
    if block_type == BlockType.ORDERED_LIST:
        items = []
        for line in lines:
            text = line.split(". ", 1)[1]
            items.append(
                ParentNode("li", text_to_children(text))
            )
        return ParentNode("ol", items)


