import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "bold text"),
                LeafNode(None, " normal text"),
                LeafNode("i", " cursive text"),
            ],
        )
        expected = "<p><b>bold text</b> normal text<i> cursive text</i></p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        
        expected = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_no_tag_raises_error(self):
        # We testen of de juiste error wordt gegooid
        node = ParentNode(None, [LeafNode("b", "text")])
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "ParentNode must have a tag")

    def test_to_html_no_children_raises_error(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "ParentNode must have children")

if __name__ == "__main__":
    unittest.main()