import re
from textnode import TextNode,TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
        else:
            text_split = node.text.split(delimiter)
            if len(text_split) % 2 == 0:
                raise Exception(f"Invalid markdown syntax:{node.text}")
            
            for section in range(len(text_split)):
                if text_split[section] == "":
                    continue
                if section % 2 == 0:
                    new_list.append(TextNode(text_split[section], TextType.TEXT))
                else:
                    new_list.append(TextNode(text_split[section], text_type))


    return new_list


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        text = node.text
        info = extract_markdown_images(text)
        if len(info) == 0:
            new_list.append(node)
            continue
        for image in info:
            sections = text.split(f"![{image[0]}]({image[1]})",1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_list.append(TextNode(sections[0],TextType.TEXT))
            new_list.append(
               TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1]
                )
            )
            text = sections[1]
        if text != "":
            new_list.append(TextNode(text, TextType.TEXT))
    return new_list

def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        text = node.text
        info = extract_markdown_links(text)
        if len(info) == 0:
            new_list.append(node)
            continue
        for link in info:
            sections = text.split(f"[{link[0]}]({link[1]})",1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_list.append(TextNode(sections[0],TextType.TEXT))
            new_list.append(TextNode(link[0],TextType.LINK,link[1]))
            text = sections[1]
        if text != "":
            new_list.append(TextNode(text, TextType.TEXT))
    return new_list

def text_to_textnodes(text):
    node = TextNode(text,TextType.TEXT)
    node_list = [node]
    node_list = split_nodes_delimiter(node_list,"**",TextType.BOLD)
    node_list = split_nodes_delimiter(node_list,"_",TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list,"`",TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)

    return node_list
