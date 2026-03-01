import unittest
from Blocknode import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        markdown = "This is a paragraph."
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_heading(self):
        markdown = "# This is a heading."
        self.assertEqual(block_to_block_type(markdown), BlockType.HEADING)
        markdown = "## This is another heading."
        self.assertEqual(block_to_block_type(markdown), BlockType.HEADING)
        markdown = "###### This is a sixth level heading."
        self.assertEqual(block_to_block_type(markdown), BlockType.HEADING)

    def test_code(self):
        markdown = "```print('Hello, World!')```"
        self.assertEqual(block_to_block_type(markdown), BlockType.CODE)
        markdown = "```python\nprint(\'Hello, World!\')\n```"
        self.assertEqual(block_to_block_type(markdown), BlockType.CODE)

    def test_quote(self):
        markdown = "> This is a quote.\n> Second line of quote."
        self.assertEqual(block_to_block_type(markdown), BlockType.QUOTE)
        markdown = "> Single line quote."
        self.assertEqual(block_to_block_type(markdown), BlockType.QUOTE)

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(markdown), BlockType.UNORDERED_LIST)
        markdown = "- Single item"
        self.assertEqual(block_to_block_type(markdown), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(markdown), BlockType.ORDERED_LIST)
        markdown = "1. Single item"
        self.assertEqual(block_to_block_type(markdown), BlockType.ORDERED_LIST)

    def test_mixed_content_paragraph(self):
        markdown = "This is a paragraph with some **bold** and *italic* text."
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)
        markdown = "  This is a paragraph with leading spaces."
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)
        markdown = "Not a heading# with a hash in middle"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_invalid_heading(self):
        markdown = "####### Not a heading"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)
        markdown = "#Not a heading"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_invalid_quote(self):
        markdown = "> Line 1\nNot a quote line 2"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_invalid_unordered_list(self):
        markdown = "- Item 1\n  Not a list item"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)
        markdown = "* Item 1" # Unordered list with * is not supported by current implementation
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_invalid_ordered_list(self):
        markdown = "1. Item 1\n3. Item 3"
        self.assertNotEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)
        markdown = "A. Item 1"
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

if __name__ == '__main__':
    unittest.main()
