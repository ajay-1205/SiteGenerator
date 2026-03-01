from models import TextNode, TextType
from extract_text import extract_markdown_images, extract_markdown_link

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split = old_node.text.split(delimiter)
        if len(split) % 2 == 0:
            raise Exception("Invalid markdown: unmatched delimiter")

        for i, part in enumerate(split):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(old_node)
            continue
        remaining_text = text
        for alt, url in images:
            image_markdown = f"![{alt}]({url})"
            parts = remaining_text.split(image_markdown, 1)
            # Text before image
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            # Image node
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            # Update remaining text
            remaining_text = parts[1]
        # Text after last image
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        links = extract_markdown_link(text)

        if not links:
            new_nodes.append(old_node)
            continue
        remaining_text = text
        for alt, url in links:
            link_markdown = f"[{alt}]({url})"
            parts = remaining_text.split(link_markdown, 1)
            # Text before image
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            # Image node
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            # Update remaining text
            remaining_text = parts[1]
        # Text after last image
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    # Order matters
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes   




                
                     

    
        