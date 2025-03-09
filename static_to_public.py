import os
import shutil
from generate_pages import generate_pages_recursive, extract_title

def main():
    # Step 1: Clean the public directory
    if os.path.exists("public"):
        # Remove everything in public directory
        for item in os.listdir("public"):
            item_path = os.path.join("public", item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    else:
        # Create public directory if it doesn't exist
        os.makedirs("public")
    
    # Step 2: Copy static files to public
    if os.path.exists("static"):
        for item in os.listdir("static"):
            source = os.path.join("static", item)
            destination = os.path.join("public", item)
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
    

    generate_pages_recursive(
    dir_path_content="content",
    template_path="template.html",
    dest_dir_path="public"
    )

    print("Site generation complete!")

if __name__ == "__main__":
    main()
