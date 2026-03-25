import unittest
from textnode import TextNode, TextType
from parserfunction import split_nodes_delimiter

class TestParser(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold** and **more bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("Words in *italic* style", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        
        expected = [
            TextNode("Words in ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" style", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_exception(self):
        node = TextNode("This is *invalid italic", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(str(cm.exception), "Invalid Markdown syntax: delimiter '*' not closed.")

    def test_multiple_nodes(self):
        nodes = [
            TextNode("Node one `code`", TextType.TEXT),
            TextNode("Node two already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        expected = [
            TextNode("Node one ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("Node two already bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

if __name__ == "__main__":
    unittest.main()