import unittest
from htmlnode import HTMLNode, LeafNode

class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    
    def test_leaf_node_has_no_children(self):
        node = LeafNode("p", "Hello")
      
        self.assertTrue(node.children is None or len(node.children) == 0)

    def test_leaf_node_value_required(self):
        # Test that creating a LeafNode with None value raises an error
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_leaf_node_no_tag(self):
        # Test raw text node (tag is None)
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_node_with_props(self):
        # Test a node with properties
        node = LeafNode("a", "Click me", {"href": "https://example.com", "class": "link"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" class="link">Click me</a>')
    