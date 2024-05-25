import unittest

from ..htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "This is header", [], {"bold": True, "ton": "green"})

        self.assertEqual(node.props_to_html(), ' bold="True" ton="green"')
        self.assertEqual(node.children, [])

    def test_error(self):
        node = HTMLNode("h1", "This is header", [], {"bold": True, "ton": "green"})

        with self.assertRaises(NotImplementedError) as cm:
            node.to_html()
        message = cm.exception.args[0]
        self.assertEqual(message, "to_html method not implemented")

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

if __name__ == "__main__":
    unittest.main()
