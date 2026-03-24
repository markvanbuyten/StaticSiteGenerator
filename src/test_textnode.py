import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a url", TextType.LINK, "https://www.boot.dev")
        node4 = TextNode("This is a url", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertEqual(node3, node4)
        self.assertNotEqual(node2, node4)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node1 = TextNode("This is a url", TextType.LINK, "https://www.boot.dev")
        html_node1 = text_node_to_html_node(node1)
        self.assertEqual(html_node1.tag, "a")
        self.assertEqual(html_node1.value, "This is a url")
        
        

if __name__ == "__main__":
    unittest.main()