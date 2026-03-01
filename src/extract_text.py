import re

def extract_markdown_images(text):
    images = re.findall(r'!\[(.*?)\]\((.*?)\)', text)
    return images

def extract_markdown_link(text):
    images = re.findall(r'(?<!!)\[(.*?)\]\((.*?)\)', text)
    return images

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()

    raise Exception("No H1 title found")



