from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    # Check for empty block
    if not block:
        return BlockType.PARAGRAPH
    
    # Check for heading
    if block.startswith('#'):
        parts = block.split(' ', 1)
        if len(parts) > 1 and all(c == '#' for c in parts[0]) and 1 <= len(parts[0]) <= 6:
            return BlockType.HEADING
    
    # Check for code block - note how we handle the triple backticks
    if block.startswith('```') and block.rstrip().endswith('```'):
        return BlockType.CODE
    
    # Check for quote
    if block.startswith('>'):
        lines = block.split('\n')
        if all(line.strip().startswith('>') for line in lines):
            return BlockType.QUOTE
    
    # Check for unordered list
    if block.startswith('- '):
        lines = block.split('\n')
        if all(line.strip().startswith('- ') or line.strip() == '' for line in lines):
            return BlockType.UNORDERED_LIST
    
    # Check for ordered list
    lines = block.split('\n')
    if lines and lines[0].startswith('1. '):
        valid_list = True
        expected_number = 1
        for line in lines:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            if not line.startswith(f"{expected_number}. "):
                valid_list = False
                break
            expected_number += 1
        if valid_list:
            return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH
