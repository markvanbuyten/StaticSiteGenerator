from static_to_public import *

def main():
    dir_static = "./static"
    dir_public = "./public"

    print("Cleaning public directory...")
    clean_directory(dir_public)

    print("Copying static files...")
    copy_files_recusive(dir_static, dir_public)

if __name__ == "__main__":
    main()