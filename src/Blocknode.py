from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



def block_to_block_type(markdown):
    lines = markdown.split("\n")

    # Code block
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE

    # Heading (1-6 # followed by space)
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING

    # Quote (every line starts with >)
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list (every line starts with - )
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list (1. 2. 3. ...)
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            break
        else:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
