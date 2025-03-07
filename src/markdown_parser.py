from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType
import re


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError(f"text_node must be an instance of TextNode, got {text_node})")
        
        
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid TextType: {text_node.text_type}")
    



def extract_markdown_images(text):
    image_match = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_match


def extract_markdown_links(text):
    link_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_matches

