import unittest
from extract_text import extract_markdown_images, extract_markdown_link, extract_title
from Text_delimiter import text_to_textnodes
from textnode import TextNode, TextType

class TestExtractText(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![alt text](https://example.com/image.png) and another ![alt text 2](https://example.com/image2.png)"
        self.assertEqual(extract_markdown_images(text), [("alt text", "https://example.com/image.png"), ("alt text 2", "https://example.com/image2.png")])
        text = "No images here"
        self.assertEqual(extract_markdown_images(text), [])
        text = "![one image](http://example.com/one.jpg)"
        self.assertEqual(extract_markdown_images(text), [("one image", "http://example.com/one.jpg")])

    def test_extract_markdown_link(self):
        text = "This is text with a [link](https://example.com) and another [link 2](https://example.com/page)"
        self.assertEqual(extract_markdown_link(text), [("link", "https://example.com"), ("link 2", "https://example.com/page")])
        text = "No links here"
        self.assertEqual(extract_markdown_link(text), [])
        text = "[one link](http://example.com)"
        self.assertEqual(extract_markdown_link(text), [("one link", "http://example.com")])

class TestTextToTextNodes(unittest.TestCase):
    def test_no_markdown(self):
        text = "This is a plain text."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], TextNode("This is a plain text.", TextType.TEXT))

    def test_bold_italic_code(self):
        text = "This is **bold** and _italic_ and `code`."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_images_and_links(self):
        text = "Here is an image ![alt text](https://example.com/image.png) and a link [to Google](https://www.google.com)."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and a link ", TextType.TEXT),
            TextNode("to Google", TextType.LINK, "https://www.google.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_combined_markdown(self):
        text = "**Bold text**, _italic text_, `code block`, ![image](url.jpg), [link](url.com)."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url.jpg"),
            TextNode(", ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected_nodes)

class TestExtractText(unittest.TestCase):
    def test_eq(self):
        title = extract_title("# Denovu will Fall\nThe one of the top most security provider for game will fall as game crackers are going to use AI as their tools")
        self.assertEqual(title , "Denovu will Fall")

    def test_exception(self):
        with self.assertRaises(Exception):
            extract_title("Denovu will Fall\nThe one of the top most security provider for game will fall \nas game crackers are going to use AI as their tools")

    def test_eq(self):
        title = extract_title("The one of the top most security provider for game will fall\n# Denovu will Fall\n as game crackers are going to use AI as their tools")
        self.assertEqual(title , "Denovu will Fall")