from textnode import TextType, TextNode
from markdown_parser import extract_markdown_links, extract_markdown_images

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Get the text and look for delimiters
        text = old_node.text
        remaining_text = text
        
        # While there are still delimiters in the text
        while delimiter in remaining_text:
            # Find the first pair of delimiters
            start_index = remaining_text.find(delimiter)
            if start_index == -1:
                break
                
            end_index = remaining_text.find(delimiter, start_index + len(delimiter))
            if end_index == -1:
                raise Exception(f"No closing delimiter found for {delimiter}")
                
            # Extract the three parts
            before_text = remaining_text[:start_index]
            between_text = remaining_text[start_index + len(delimiter):end_index]
            after_text = remaining_text[end_index + len(delimiter):]
            
            # Add the parts to new_nodes
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            
            new_nodes.append(TextNode(between_text, text_type))
            remaining_text = after_text
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes





def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Use the extract_images function to find all images in this node
        images = extract_markdown_images(old_node.text)
        
        # If no images found, keep the original node
        if not images:
            new_nodes.append(old_node)
            continue
            
        remaining_text = old_node.text
        
        # Process each image
        for image_alt, image_url in images:
            # Create the markdown pattern for this specific image
            image_markdown = f"![{image_alt}]({image_url})"
            
            # Split the remaining text at this image (only split once)
            sections = remaining_text.split(image_markdown, 1)
            
            # The text before the image becomes a text node (if not empty)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            # Create a node for the image itself
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # If there's text after the image, update remaining_text
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
                
        # Don't forget any remaining text after all images are processed
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Use the extract_links function to find all links in this node
        links = extract_markdown_links(old_node.text)
        
        # If no links found, keep the original node
        if not links:
            new_nodes.append(old_node)
            continue
            
        remaining_text = old_node.text
        
        # Process each link
        for link_text, link_url in links:
            # Create the markdown pattern for this specific link
            link_markdown = f"[{link_text}]({link_url})"
            
            # Split the remaining text at this link (only split once)
            sections = remaining_text.split(link_markdown, 1)
            
            # The text before the link becomes a text node (if not empty)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            # Create a node for the link itself
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            # If there's text after the link, update remaining_text
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
                
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes
