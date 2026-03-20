import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # Test 1: Controleert of attributen correct worden omgezet naar een string
        node = HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_values(self):
        # Test 2: Controleert of de velden (tag, value) correct worden opgeslagen
        node = HTMLNode(tag="p", value="Hallo wereld")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hallo wereld")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_error(self):
        # Test 3: Controleert of de NotImplementedError correct wordt getriggerd
        node = HTMLNode(tag="h1", value="Titel")
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()