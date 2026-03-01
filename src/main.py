import os
from copy_files import copy_static_to_public
from textnode import markdown_to_blocks, block_to_html_node
from extract_text import extract_title

def main():
    copy_static_to_public("static", "public")
    generate_pages_recursive("content", "template.html", "public")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        context = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    html = ""
    blocks = markdown_to_blocks(context)
    for block in blocks:
        nodes = block_to_html_node(block)
        html += nodes.to_html()

    title = extract_title(context)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    with open(dest_path, 'w') as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path) and from_path.endswith(".md"):
            dest_path = dest_path[:-3] + ".html"
            generate_page(from_path, template_path, dest_path)
        elif os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
    