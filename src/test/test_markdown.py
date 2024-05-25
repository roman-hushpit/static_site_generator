import unittest

from ..markdown import markdown_to_blocks

TEST_TEXT = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        result = markdown_to_blocks(TEST_TEXT)
        expcted = [
            """This is **bolded** paragraph""",
            """This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line""",
            """* This is a list\n* with items"""
        ]
        self.assertEqual(expcted, result)
