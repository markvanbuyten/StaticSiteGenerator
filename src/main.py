from static_to_public import *
from generate_page import generate_pages_recursive

def main():
    dir_static = "./static"
    dir_public = "./public"
    dir_content ="./content"
    template_path = "./template.html"

    print("Cleaning public directory...")
    clean_directory(dir_public)

    print("Copying static files...")
    copy_files_recusive(dir_static, dir_public)

    generate_pages_recursive(dir_content, template_path, dir_public)

if __name__ == "__main__":
    main()