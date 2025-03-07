from textnode import TextType, TextNode

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
