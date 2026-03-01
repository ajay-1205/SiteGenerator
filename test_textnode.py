import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_type_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        expected_html_node = LeafNode(None, "This is a text node")
        self.assertEqual(text_node_to_html_node(node), expected_html_node)

    def test_text_type_bold(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        expected_html_node = LeafNode("b", "This is a bold text")
        self.assertEqual(text_node_to_html_node(node), expected_html_node)

    def test_text_type_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        expected_html_node = LeafNode("i", "This is italic text")
        self.assertEqual(text_node_to_html_node(node), expected_html_node)

    def test_text_type_code(self):
        node = TextNode("This is code", TextType.CODE)
        expected_html_node = LeafNode("code", "This is code")
        self.assertEqual(text_node_to_html_node(node), expected_html_node)

    def test_text_type_link(self):
        node = TextNode("Go to Google", TextType.LINK, "https://www.google.com")
        expected_html_node = LeafNode("a", "Go to Google", {"href": "https://www.google.com"})
        self.assertEqual(text_node_to_html_node(node), expected_html_node)

    def test_text_type_image(self):
        node = TextNode("An image", TextType.IMAGE, "image.jpg")
        expected_html_node = LeafNode("img", "", {"src": "image.jpg", "alt": "An image"})
        self.assertEqual(text_node_to_html_node(node), expected_html_node)

    def test_unknown_text_type(self):
        node = TextNode("Unknown type", "unknown")
        with self.assertRaises(Exception) as cm:
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "Unknown text type")

if __name__ == '__main__':
    unittest.main()
