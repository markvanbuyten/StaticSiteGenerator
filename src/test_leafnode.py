from leafnode import LeafNode 

def test_leafnode():
    print("--- Start LeafNode Tests ---")

    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    self.assertIsNone(node.children)
    
    node1 = LeafNode("p", "Dit is een paragraaf.")
    self.assertNotEqual(node1.to_html(), "<p>Hello, world!</p>")

    node2 = LeafNode("a", "Klik hier!", {"href": "https://www.google.com", "target": "_blank"})
    self.assertNotEqual(node2.to_html(),node1.to_html())
    self.assertEqual(node1.to_html(), '<a href="https://www.google.com" target="_blank">Klik hier!</a>')
    

if __name__ == "__main__":
    test_leafnode()