import unittest
from textnode import TextNode, TextType
from parserfunction import *

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode("an ![img](url) next", TextType.TEXT)
        new_nodes = split_nodes_image([node])
    
        expected = [
            TextNode("an ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" next", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    def test_split_image_at_start(self):
        node = TextNode("![alt](https://url.com/img.png) starts the sentence", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("alt", TextType.IMAGE, "https://url.com/img.png"),
            TextNode(" starts the sentence", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_no_images(self):
        node = TextNode("Just some plain text here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("Just some plain text here.", TextType.TEXT)]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_links_multiple(self):
        node = TextNode(
            "Check [Google](https://google.com) and [BootDev](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("BootDev", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_at_end(self):
        node = TextNode("Visit our site [here](https://site.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Visit our site ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://site.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_only_links(self):
        node = TextNode("[one](url1)[two](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("one", TextType.LINK, "url1"),
            TextNode("two", TextType.LINK, "url2"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_simple(self):
        text = "This is `code` and **bold**"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_complex(self):
        text = "Combined: **bold***italic*`code`![img](url)[link](url)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Combined: ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertListEqual(expected, nodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        # Test met veel extra enters tussen blokken en witruimte rondom
        markdown = """
This is block 1.


      
This is block 2 after many spaces and enters.

"""
        blocks = markdown_to_blocks(markdown)
        expected = [
            "This is block 1.",
            "This is block 2 after many spaces and enters."
        ]
        self.assertListEqual(expected, blocks)

    def test_markdown_to_blocks_structure(self):
        markdown = """# Heading

This is a paragraph.

* Item 1
* Item 2
* Item 3"""
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# Heading",
            "This is a paragraph.",
            "* Item 1\n* Item 2\n* Item 3"
        ]
        self.assertListEqual(expected, blocks)
        self.assertEqual(len(blocks), 3)


    def test_block_to_block_types(self):
        self.assertEqual(block_to_block_type("# header"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        
        quote_block = "> line 1\n> line 2"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)
        
        bad_olist = "1. first\n3. third"
        self.assertEqual(block_to_block_type(bad_olist), BlockType.PARAGRAPH)

    def test_block_to_block_paragraph(self):
        self.assertEqual(block_to_block_type("Just a normal paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
         )
    
    def test_lists(self):
        md = """
- This is a list item with **bold**
- This is another item with a [link](https://boot.dev)

1. First ordered item
2. Second ordered item"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<ul>"
            "<li>This is a list item with <b>bold</b></li>"
            "<li>This is another item with a <a href=\"https://boot.dev\">link</a></li>"
            "</ul>"
            "<ol>"
            "<li>First ordered item</li>"
            "<li>Second ordered item</li>"
            "</ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_headings_and_quotes(self):
        md = """
# Main Heading

> This is a quote
> that spans multiple lines

### Sub Heading"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<h1>Main Heading</h1>"
            "<blockquote>This is a quote that spans multiple lines</blockquote>"
            "<h3>Sub Heading</h3>"
            "</div>"
        )
        self.assertEqual(html, expected)

if __name__ == "__main__":
    unittest.main()