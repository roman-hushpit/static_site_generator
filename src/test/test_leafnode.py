import unittest

from ..leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        props = {"href": "https://www.google.com"}
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", props)
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_error(self):
        with self.assertRaises(ValueError):
            LeafNode(None, None).to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()
