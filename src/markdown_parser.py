from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType
from blocktype import block_to_block_type
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


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        new = block.strip()
        if new != "":
            # Process each line in the block to remove indentation
            lines = new.split("\n")
            cleaned_lines = [line.strip() for line in lines]
            cleaned_block = "\n".join(cleaned_lines)
            clean_blocks.append(cleaned_block)
    return clean_blocks







def text_to_children(text):
    """Convert a text string with inline markdown to a list of HTMLNode objects"""
    # First, parse the text into TextNode objects
    from split_nodes import text_to_textnodes
    text_nodes = text_to_textnodes(text)  # This should be a function you built earlier
    
    # Convert each TextNode to an HTMLNode
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)  # Another function you built earlier
        html_nodes.append(html_node)
    
    return html_nodes




def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    parent_node = HTMLNode("div", None, [], None)

    for block in markdown_blocks:
        block_type = block_to_block_type(block)

        if block_type == "paragraph":
            # Create a paragraph node
            block_node = HTMLNode("p", None, [], None)
            
            # Process the text in the block to create child nodes
            children = text_to_children(block)
            block_node.children = children
            parent_node.children.append(block_node)
            
        elif block_type == "code":
            # Strip the triple backticks and extract code content
            code_lines = block.split("\n")
            # Skip the first and last lines (which may contain the ```)
            code_content = "\n".join(code_lines[1:-1])
            
            # Create a simple TextNode (no parsing) for the code content
            text_node = TextNode(code_content, "text")
            code_node = text_node_to_html_node(text_node)
            
            # Wrap code in pre tag
            block_node = HTMLNode("pre", None, [code_node], None)
            parent_node.children.append(block_node)

        elif block_type == "heading":
            # Count hashtags to determine heading level
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            
            # Create heading node (h1-h6)
            block_node = HTMLNode(f"h{level}", None, [], None)
            
            # Process text without the hashtags
            text = block[level:].strip()
            children = text_to_children(text)
            block_node.children = children
            parent_node.children.append(block_node)

        elif block_type == "unordered_list":
            # Create unordered list node (ul)
            block_node = HTMLNode("ul", None, [], None)
            
            # Split the list items by line
            items = block.split("\n")
            for item in items:
                if item.strip().startswith("- "):
                    # Remove the "- " prefix
                    item_text = item.strip()[2:]
                    # Create li node for each list item
                    li_node = HTMLNode("li", None, [], None)
                    # Process item text for inline markdown
                    li_node.children = text_to_children(item_text)
                    block_node.children.append(li_node)
            parent_node.children.append(block_node)

        elif block_type == "ordered_list":
            block_node = HTMLNode("ol", None, [], None)
            items = block.split("\n")
            for item in items:
                # Check if the item starts with a digit followed by a period
                if item.strip() and any(item.strip().startswith(f"{i}.") for i in range(10)):
                    # Find the first dot after the number
                    dot_index = item.find(".")
                    if dot_index != -1:
                        # Extract the text after the number and period
                        item_text = item[dot_index+1:].strip()
                        # Create li node for each list item
                        li_node = HTMLNode("li", None, [], None)
                        # Process item text for inline markdown
                        li_node.children = text_to_children(item_text)
                        block_node.children.append(li_node)
            parent_node.children.append(block_node)


        elif block_type == "quote":
            block_node = HTMLNode("blockquote", None, [], None)
            # Remove the '>' symbols at the beginning of each line
            lines = block.split("\n")
            quote_content = ""
            for line in lines:
                if line.strip().startswith(">"):
                    # Remove the '>' and any space that might follow it
                    cleaned_line = line.strip()[1:].strip()
                    quote_content += cleaned_line + " "
                else:
                    # If a line doesn't start with '>', still include it in the quote
                    quote_content += line.strip() + " "
            
            # Process the quote content for inline markdown
            block_node.children = text_to_children(quote_content.strip())
            parent_node.children.append(block_node)

    return parent_node


        
                                        

                        



        