from textnode import TextNode, TextType, text_node_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode
import re
from enum import Enum

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
    
        split_nodes = []

        sections = old_node.text.split(delimiter)

        if len(sections) % 2 ==0:
            raise Exception(f"Invalid Markdown syntax: delimiter '{delimiter}' not closed.")
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    alt_url = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_url

def extract_markdown_links(text):
    alt_url = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_url

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        
        for image in images:
            alt_text = image[0]
            url = image[1]

            sections = original_text.split(f"![{alt_text}]({url})", 1)

            if len(sections) != 2:
                raise Exception("Invalid markdown, link section not found")
                
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        
        for link in links:
            alt_text = link[0]
            url = link[1]

            sections = original_text.split(f"[{alt_text}]({url})", 1)

            if len(sections) != 2:
                raise Exception("Invalid markdown, link section not found")
                
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))

            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes

def markdown_to_blocks(markdown):
    blocks = []
    temp_nodes = markdown.split("\n\n")
    for temp_node in temp_nodes:
        cleaned_block = temp_node.strip()
        if cleaned_block != "":
            blocks.append(cleaned_block)
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE ="quote"
    UNOLIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(markdown):
    lines = markdown.split("\n")

    if (markdown.startswith('# ')
        or markdown.startswith('## ')
        or markdown.startswith('### ')
        or markdown.startswith('#### ')
        or markdown.startswith('##### ')
        or markdown.startswith('###### ')):
        return BlockType.HEADING
    if len(lines) > 1 and markdown.startswith('```\n') and markdown.endswith('```'):
        return BlockType.CODE
    if markdown.startswith('>'):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if markdown.startswith('- '):
        for line in lines:
            if not (line.startswith("- ")):
                return BlockType.PARAGRAPH
        return BlockType.UNOLIST
    if markdown.startswith('1. '):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = create_html_node_from_block(block, block_type)
        children.append(html_node)
    return ParentNode("div",children)

def create_html_node_from_block(block, block_type):
    if block_type == BlockType.QUOTE:
        return create_quote_node(block)
    if block_type == BlockType.UNOLIST:
        return create_unolist_node(block)
    if block_type == BlockType.OLIST:
        return create_olist_node(block)
    if block_type == BlockType.CODE:
        return create_code_node(block)
    if block_type == BlockType.HEADING:
        return create_heading_node(block)
    return create_patagraph_node(block)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def create_quote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def create_unolist_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        content = line[2:]
        children = text_to_children(content)
        list_items.append(ParentNode("li",  children))
    return ParentNode("ul", list_items)

def create_olist_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        dot_index = line.find(". ")
        if dot_index == -1:
            content = line
        else:
            content = line[dot_index + 2:]

        children = text_to_children(content)
        list_items.append(ParentNode("li",  children))
    return ParentNode("ol", list_items) 

def create_code_node(block):
    lines = block.split("\n")
    if len(lines) > 2:
        content = "\n".join(lines[1:-1])
    else:
        content = block.strip("`").strip()
    
    if not content.endswith("\n"):
        content += "\n"
        
    code_leaf = LeafNode("code", content)
    return ParentNode("pre", [code_leaf])

def create_heading_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    content = block[level + 1:]
    children = text_to_children(content)
    return ParentNode(f"h{level}", children)

def create_patagraph_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)
