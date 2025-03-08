import unittest
from blocktype import BlockType, block_to_block_type  # Replace 'your_module' with your actual module name

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a simple paragraph with no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Edge case: empty string
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        
    def test_heading(self):
        # Valid headings
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Invalid headings - should be paragraphs
        self.assertEqual(block_to_block_type("####### Too many hashtags"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        
    def test_code(self):
        # Valid code blocks
        self.assertEqual(block_to_block_type("```\nprint('hello')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python\nprint('hello')\n```"), BlockType.CODE)
        
        # Invalid code blocks
        self.assertEqual(block_to_block_type("```print('hello')"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("print('hello')```"), BlockType.PARAGRAPH)
        
    def test_quote(self):
        # Valid quotes
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)
