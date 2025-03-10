import os
import sys
import shutil
from generate_pages import generate_pages_recursive, extract_title

def main():
    # Step 1: Parse basepath argument from command line
    if len(sys.argv) > 1:
        basepath = sys.argv[1]  # Get the basepath passed as an argument
    else:
        basepath = "/"  # Default to root path if no argument is provided

    # Step 2: Clean or create the destination directory
    print(f"Checking docs directory, exists: {os.path.exists('docs')}")
    if os.path.exists("docs"):
        print("Cleaning existing docs directory...")
        for item in os.listdir("docs"):
            item_path = os.path.join("docs", item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Removed directory: {item_path}")
            else:
                os.remove(item_path)
                print(f"Removed file: {item_path}")
    else:
        os.makedirs("docs")
    print(f"Created docs directory at: {os.path.abspath('docs')}")
    # Step 3: Copy static files to "docs"
    if os.path.exists("static"):
        for item in os.listdir("static"):
            source = os.path.join("static", item)
            destination = os.path.join("docs", item)
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)

    # Step 4: Generate pages using the basepath
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="docs",
        basepath=basepath  # Pass basepath here!
    )

    print("Site generation complete!")



if __name__ == "__main__":
    main()
