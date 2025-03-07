import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_attributes(self):
        node = HTMLNode("h1", "Welcome to this page")
        node2 = HTMLNode("h1", "Welcome to this page")
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)


    def test_props_to_html(self):
        # Create a node with tag "a" and props including href
        node = HTMLNode(
            tag="a", 
            props={"href": "https://www.google.com"}
        )
        # Test that props_to_html returns the expected string
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com"'
        )
        
        # Test with multiple props
        node2 = HTMLNode(
            tag="a",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        # The exact order might vary, so we could check for both substrings
        result = node2.props_to_html()
        self.assertTrue(' href="https://www.google.com"' in result)
        self.assertTrue(' target="_blank"' in result)


    def test_repr(self):
        node = HTMLNode(tag="p", value="hello", props={"class": "intro"})
        repr_string = repr(node)
        # Check that all important attributes are mentioned in the representation
        self.assertIn("p", repr_string)
        self.assertIn("hello", repr_string)
        self.assertIn("class", repr_string)
        self.assertIn("intro", repr_string)


