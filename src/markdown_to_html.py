from htmlnode import ParentNode
from blocks import BlockType,markdown_to_blocks,block_to_block_type
from textnode import TextNode,TextType,text_node_to_html_node
from splitnodes import text_to_textnodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block,block_to_block_type(block))
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block,btype):
    match btype:
        case BlockType.PARAGRAPH:
            return para_to_htmlnode(block)
        case BlockType.HEADING:
            return head_to_htmlnode(block)
        case BlockType.CODE:
            return code_to_htmlnode(block)
        case BlockType.UNORDERED:
            return unord_to_htmlnode(block)
        case BlockType.ORDERED:
            return ord_to_htmlnode(block)
        case BlockType.QUOTE:
            return quote_to_htmlnode(block)
        

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def para_to_htmlnode(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def head_to_htmlnode(block):
    count = 0
    while block[count] == "#":
        count += 1
    contents = block[count+1:]
    children = text_to_children(contents)
    return ParentNode(f"h{count}",children)

def code_to_htmlnode(block):
    contents = block[4:-3]
    tnode = TextNode(contents,TextType.TEXT)
    child = text_node_to_html_node(tnode)
    code = ParentNode("code",[child])
    return ParentNode("pre",[code])

def ord_to_htmlnode(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def unord_to_htmlnode(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_htmlnode(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)