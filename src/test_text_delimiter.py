import unittest
from Text_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is a `code` block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" block", TextType.TEXT))

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is an ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This has no delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("This has no delimiter", TextType.TEXT))

    def test_split_nodes_image(self):
        node = TextNode("This is text with an ![alt text](https://example.com/image.png) and another ![alt text 2](https://example.com/image2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0], TextNode("This is text with an ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"))
        self.assertEqual(new_nodes[2], TextNode(" and another ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("alt text 2", TextType.IMAGE, "https://example.com/image2.png"))

    def test_split_nodes_image_no_image(self):
        node = TextNode("This has no image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("This has no image", TextType.TEXT))

    def test_split_nodes_image_only_image(self):
        node = TextNode("![alt text](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"))

    def test_split_nodes_link(self):
        node = TextNode("This is text with a [link](https://example.com) and another [link 2](https://example.com/page)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("link", TextType.LINK, "https://example.com"))
        self.assertEqual(new_nodes[2], TextNode(" and another ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("link 2", TextType.LINK, "https://example.com/page"))

    def test_split_nodes_link_no_link(self):
        node = TextNode("This has no link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("This has no link", TextType.TEXT))

    def test_split_nodes_link_only_link(self):
        node = TextNode("[one link](http://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("one link", TextType.LINK, "http://example.com"))
