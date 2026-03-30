from textnode import TextNode, TextType
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