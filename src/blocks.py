from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered"
    ORDERED = "ordered"

def markdown_to_blocks(markdown):
    node_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block_strip = block.strip()
        if block_strip == "":
            continue
        node_blocks.append(block_strip)
    return node_blocks

def block_to_block_type(block):
    if block[0] == "#":
        index = 1
        while block[index] == "#":
            index += 1
        if index <= 6:
            return BlockType.HEADING
        
    if block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    
    if block[0] == ">":
        lines = block.split("\n")
        iscode = True
        for line in lines:
            if line[0] != ">":
                iscode = False
        if iscode:
            return BlockType.QUOTE
        
    if block[0] == "-":
        lines = block.split("\n")
        isunord = True
        for line in lines:
            if line[0] != "-":
                isunord = False
        if isunord:
            return BlockType.UNORDERED
        
    if block[0:3] == "1. ":
        lines = block.split("\n")
        isord = True
        num = 1
        for line in lines:
            if line[0:3] != f"{num}. ":
                isord = False
            num += 1
        if isord:
            return BlockType.ORDERED
        
    return BlockType.PARAGRAPH