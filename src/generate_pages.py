import os
import shutil
from pathlib import Path
from blocktype import markdown_to_html_node
from htmlnode import *

def extract_title(markdown):
    """Extract the title (h1) from markdown content."""
    print(f"Extracting title from markdown with length: {len(markdown)}")
    for line in markdown.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
            print(f"Found title: {title}")
            return title
    error_msg = "No h1 header found in markdown"
    print(f"ERROR: {error_msg}")
    raise Exception(error_msg)

def generate_page(from_path, template_path, dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)


    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')


    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)  # Pass basepath here
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)  # Recursive call with basepath
    
